import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, confusion_matrix
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result_file', default='./results/outputs_with_labels/Llama3_1_8B_final.csv')
    parser.add_argument('--save_file', default='./results/final_results.csv')
    parser.add_argument('--model_name', default='Llama3.1_8b')

    return parser.parse_args()

def get_report(file, return_dict:bool=False):
    df = pd.read_csv(file)
    df.dropna(subset='model_label', inplace=True)
    f1 = f1_score(df['label'], df['model_label'])
    precision = precision_score(df['label'], df['model_label'])
    recall = recall_score(df['label'], df['model_label'])
    accuracy = accuracy_score(df['label'], df['model_label'])

    cm = confusion_matrix(df['label'], df['model_label'])
    tnr = cm[0,0]/(cm[0,0]+cm[0,1])
    f1_tnr_tpr = 2*(recall*tnr)/(recall+tnr)
    
    if not return_dict:
        print(f"Recall: {recall}\n Precision: {precision}\n F1: {f1}\n Accuracy: {accuracy}\n TNR: {tnr}\n f1_tnr_tpr: {f1_tnr_tpr}")
    else:
        report = {
            "Recall": recall,
            "Precision": precision,
            "F1": f1,
            "Accuracy": accuracy,
            "TNR": tnr,
            "f1_tnr_tpr": f1_tnr_tpr
        }
        return report

if __name__ == "__main__":
    args = parse_args()

    report = get_report(args.result_file, return_dict=True)
    report['model'] = args.model_name
    report_df = pd.DataFrame([report])
    if os.path.exists(args.save_file):
        report_df.to_csv(args.save_file, mode='a', header=False, index=False)
    else:
        report_df.to_csv(args.save_file, mode='a', header=True, index=False)


