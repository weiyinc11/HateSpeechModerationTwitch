import pandas as pd
import json
import ast
import logging
import re
import os
import argparse

def get_prediction_from_model_response(model_response):
    try:
        prediction = json.loads(model_response)[
            'label']
    except:
        try:
            prediction = ast.literal_eval(
                model_response)['label']
        except:
            try:
                prediction = re.search(r'"label"\s*:\s*"([^"]+)"', str(model_response)).group(2)
            except Exception as e:
                logging.debug(f"Regex did not match: \n{model_response}")
                content = str(model_response)
                if ': \"hate\"' in content.lower() or ': hate' in content.lower() or ': \'hate\'' in content.lower():
                    prediction = "hate"
                elif ': \"nothate\"' in content.lower() or ': nothate' in content.lower() or ': \'nothate\'' in content.lower():
                    prediction = "nothate"
                else:
                    logging.debug(
                        f"Cannot extract label: \n{model_response}")
                    prediction = None
    return prediction


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--log_dir', default='./logs/', type=str)
    parser.add_argument('--log_file_name', default='llama3_1_8b_log.log')
    parser.add_argument('--output_file', default='./results/model_outputs/Llama3_18B.csv')
    parser.add_argument('--save_dir', default='./results/outputs_with_labels/')
    parser.add_argument('--save_file', default='Llama3_1_8B_final.csv')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    os.makedirs(args.log_dir, exist_ok=True)
    os.makedirs(args.save_dir, exist_ok=True)

    logging.basicConfig(filename=os.path.join(args.log_dir, args.log_file_name), level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    df = pd.read_csv(args.output_file)

    df['model_label'] = df['model_response'].apply(lambda x: get_prediction_from_model_response(x))

    df['model_label'] = df['model_label'].apply(lambda x: 1 if x == 'hate' else (0 if x == 'nothate' else None))
    print(len(df.loc[df['model_label'].isna()]))
    df.to_csv(os.path.join(args.save_dir, args.save_file))


