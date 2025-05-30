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
    parser.add_argument("--model", type=str, default='Llama3.3_70b', help="Model name")
    parser.add_argument("--model_p", type=str, default='/assets/models/meta-llama-3.3-instruct-70b/', help="Model path")
    parser.add_argument('--max_model_len', type=int, default=None)
    parser.add_argument('--max_new_tokens', type=int, default=1024)
    parser.add_argument("--prompt_type", type=str, default='zero_shot', help="Prompt type")
    parser.add_argument("--user_prompt_only", action="store_true", help="Pass if the prompt type only has user prompt")
    parser.add_argument("--test_file", type=str, default='./data/test_set.csv', help="Path to the test set CSV file")
    parser.add_argument("--error_type", choices=['fp', 'fn'], help='Whether to pass false positives to the model or false negatives')
    parser.add_argument('--dataset', choices=['dynahate', 'sbic', 'toxigen', 'all'], default='all', help='dataset to be used')
    parser.add_argument("--save_file", type=str, default='Llama3.1_8b_with_cot.csv', help="Output file name")
    parser.add_argument("--save_dir", type=str, default='./results/model_outputs/', help='Save Dir')
    # parser.add_argument('--log_dir', type=str, default ='./logs/')
    parser.add_argument('-u','--unique_run_ID', type=str, default=None, help='Unique ID for each instance of this experiment')
    parser.add_argument("-g", "--gpus", help="List of GPU IDs to use (comma-separated)", default="0")
    parser.add_argument('--use_sw', action="store_true", help='Use rows with has_swear_words = True')
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
    if args.error_type == 'fp':
        df = df[(df['label'] == 0) & (df['moderation'] == 1)]
    else:
        df = df[(df['label'] == 1) & (df['moderation'] == 0)]
    if not args.dataset == 'all':
        df = df[df['dataset'] == args.dataset]
    if args.use_sw:
        df = df[df['has_swear_words'] == True]
    if args.user_prompt_only:
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
    