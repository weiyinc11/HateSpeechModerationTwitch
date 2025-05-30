import argparse
import yaml
import os
import pandas as pd
import torch
import vllm
import transformers
from time import time, strftime
from utils import get_tokenizer, make_prompt

os.environ['VLLM_LOGGING_LEVEL'] = 'DEBUG'
os.environ['NCCL_P2P_DISABLE'] = '1'

PROMPT_FILE = './prompts.yaml'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per_gpu_utilization", type=float, default=0.9, help="GPU memory utilization per GPU")
    # parser.add_argument("--num_gpu_utilization", type=int, default=1, help="Number of GPUs to use")
    parser.add_argument("--model", type=str, default='Llama3.1_8b', help="Model name")
    parser.add_argument("--model_p", type=str, default='/assets/models/meta-llama-3.1-instruct-8b/', help="Model path")
    parser.add_argument('--max_model_len', type=int, default=None)
    parser.add_argument('--max_new_tokens', type=int, default=1024)
    parser.add_argument("--prompt_type", type=str, default='zero_shot', help="Prompt type")
    parser.add_argument("--test_file", type=str, default='./data/test_set.csv', help="Path to the test set CSV file")
    parser.add_argument("--save_file", type=str, default='Llama3_3_70b.csv', help="Output file name")
    parser.add_argument("--save_dir", type=str, default='./results/model_outputs/', help='Save Dir')
    # parser.add_argument('--log_dir', type=str, default ='./logs/')
    parser.add_argument('-u','--unique_run_ID', type=str, default=None, help='Unique ID for each instance of this experiment')
    parser.add_argument("-g", "--gpus", help="List of GPU IDs to use (comma-separated)", default="0")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    avl_gpus = list(args.gpus.split(','))
    os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str(x) for x in avl_gpus)
    print("CUDA_VISIBLE_DEVICES set to:", os.environ['CUDA_VISIBLE_DEVICES'])
    num_gpu_utilization = len(avl_gpus)

    with open(PROMPT_FILE, 'r') as file:
        prompts = yaml.load(file, Loader=yaml.FullLoader)

    tokenizer = get_tokenizer(args.model_p)
    config = transformers.AutoConfig.from_pretrained(args.model_p)
    context_window = min(
        getattr(config, 'sliding_window', None) or config.max_position_embeddings, config.max_position_embeddings, 106192
    )
    engine_params = {
        'model': args.model_p,
        'trust_remote_code' : True,
        'dtype' : 'bfloat16',
        'gpu_memory_utilization': args.per_gpu_utilization,
        'tensor_parallel_size': num_gpu_utilization,
        'max_model_len': context_window
    }
    # if 'gemma' in args.model.lower():
    #     engine_params['dtype'] = 'bfloat16'
    if args.max_model_len:
        engine_params['max_model_len'] = args.max_model_len
    model = vllm.LLM(**engine_params)

    sys_prompt = prompts[args.prompt_type].get('system', None)
    user_prompt = prompts[args.prompt_type]['user']    
    df = pd.read_csv(args.test_file)
    if args.prompt_type == 'zero_shot_without_system':
        prompts = [make_prompt(sys_prompt, user_prompt+comment, user_only=True) for comment in df['msg_sent']]
    else:
        prompts = [make_prompt(sys_prompt, user_prompt+comment) for comment in df['msg_sent']]
    strings = tokenizer.apply_chat_template(prompts, tokenize=False, add_generation_prompt=True)
    _tokens = tokenizer(strings, add_special_tokens=False, padding="longest", return_tensors="pt")
    max_input_len = _tokens.input_ids.shape[-1]
    tokens = [tokenizer(string, add_special_tokens=False).input_ids for string in strings]
    tokens  = [vllm.TokensPrompt(prompt_token_ids=tok_ids) for tok_ids in tokens]

    gen_kwargs = vllm.SamplingParams(
        temperature=0,
        top_p=1.0,
        max_tokens=args.max_new_tokens + max_input_len
    )
    
    s2 = time()
    outputs = model.generate(tokens, sampling_params=gen_kwargs, use_tqdm=True)
    time_taken = time() - s2
    out_strings = [output.outputs[0].text for output in outputs]

    df['model_response'] = out_strings
    os.makedirs(args.save_dir, exist_ok=True)
    file_name = os.path.join(args.save_dir,args.save_file)
    df.to_csv(file_name)
    
    print(f"Inference time (in s): {time_taken}")

    # Log runtime data
    runtime_file = os.path.join(args.save_dir, "runtimes.csv")
    timestamp = strftime("%Y-%m-%d %H:%M:%S")
    runtime_data = pd.DataFrame([[timestamp, args.unique_run_ID, args.model, time_taken, len(prompts) ,args.prompt_type]],
                                 columns=["Timestamp", "Unique ID", "Model", "Time Taken", "num_examples","Prompt Type"])
    if os.path.exists(runtime_file):
        runtime_data.to_csv(runtime_file, mode='a', header=False, index=False)
    else:
        runtime_data.to_csv(runtime_file, mode='w', header=True, index=False)
