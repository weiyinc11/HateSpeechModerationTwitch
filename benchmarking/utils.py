from torch.utils.data import Dataset, DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import re
def get_tokenizer(model_name:str)->AutoTokenizer:
    tokenizer_args = {}

    if "gemma" in model_name:
        print(f"MODEL NAME: {model_name}. RIGHT PADDING ENABLED!")
        tokenizer_args["padding_side"] = "right"
    else:
        tokenizer_args["padding_side"] = "left"

    tokenizer = AutoTokenizer.from_pretrained(model_name, **tokenizer_args)
    if getattr(tokenizer, 'pad_token', None) is None:
        tokenizer.pad_token = tokenizer.eos_token or tokenizer.unk_token
    return tokenizer

def get_model_forEval(model_n:str)->AutoModelForCausalLM:
    model = AutoModelForCausalLM.from_pretrained(model_n, device_map ="auto",torch_dtype="bfloat16")
    model.eval()
    return model

def make_prompt(sys_prompt:str, user_prompt:str, user_only:bool = False)->list[dict]:
    if not user_only:
        return [
        {'role': 'system', 'content': sys_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    else:
        return [
            {'role': 'user', 'content': user_prompt}
        ]


