import pandas as pd
import json
import ast
# import logging
import re
import os
import argparse

import re

def extract_sw_label(model_output:str):
    has_swear_words_match = re.search(r'"has_swear_words"\s*:\s*"(true|false)"', model_output, re.IGNORECASE)
    has_swear_words = has_swear_words_match.group(1).lower() == "true" if has_swear_words_match else None

    return has_swear_words

def extract_hateful_intent(model_output: str):    
    hateful_intent_match = re.search(r'"hateful_intent"\s*:\s*(?:"(true|false)"|(true|false))', model_output, re.IGNORECASE)
    
    if hateful_intent_match:
        return (hateful_intent_match.group(1) or hateful_intent_match.group(2)).lower()
    
    return None


def parse_args():
    parser = argparse.ArgumentParser()

    # parser.add_argument('--log_dir', default='./logs/', type=str)
    # parser.add_argument('--log_file_name', default='llama3_1_8b_log.log')
    parser.add_argument('--output_file', default='./results/model_outputs/Llama3_18B.csv')
    parser.add_argument('--save_dir', default='./results/outputs_with_labels_bf16/')
    parser.add_argument('--save_file', default='Llama3_1_8B_final.csv')
    parser.add_argument('--label_type', choices=['swear_word_id', 'hateful_intent'])

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # os.makedirs(args.log_dir, exist_ok=True)
    os.makedirs(args.save_dir, exist_ok=True)

    # logging.basicConfig(filename=os.path.join(args.log_dir, args.log_file_name), level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    df = pd.read_csv(args.output_file)

    if args.label_type == 'swear_word_id':
        df['has_swear_words'] = df['model_response'].apply(lambda x: extract_sw_label(x))
        print(len(df.loc[df['has_swear_words'].isna()]))
    else:
        df['hateful_intent'] = df['model_response'].apply(lambda x: extract_hateful_intent(x))
        print(len(df.loc[df['hateful_intent'].isna()]))
    
    df.to_csv(os.path.join(args.save_dir, args.save_file))


