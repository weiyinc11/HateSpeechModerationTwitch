

import pandas as pd
import numpy as np
import re

def normalize_text(text):
    """
    Normalize text for consistent comparison.
    """
    if not isinstance(text, str):
        return text
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-visible characters
    text = re.sub(r'[^\x20-\x7E]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    text = re.sub(r'^\.\s', '', text)
    return text

# Load the files
input_file = "IHC.csv"
moderated_file = "IHC_Mod.csv"
non_moderated_file = "IHC_notMod.csv"

# Load CSVs into dataframes
input_df = pd.read_csv(input_file)
moderated_df = pd.read_csv(moderated_file)
non_moderated_df = pd.read_csv(non_moderated_file, on_bad_lines="skip", engine="python")

# Define patterns to remove
patterns = ['!dice', '!audit', r'You rolled a [1-6]']

# Create a regex pattern that matches any of the defined patterns
regex_pattern = '|'.join(patterns)
non_moderated_df = non_moderated_df[~non_moderated_df['message'].str.match(regex_pattern, na=False)]

non_moderated_df = non_moderated_df.drop_duplicates(subset='message')
# print(non_moderated_df.head(10))
print(len(moderated_df))
print(len(non_moderated_df))
print(len(input_df))
moderated_df['msg_sent'] = moderated_df['msg_sent'].apply(normalize_text)
input_df['text'] = input_df['text'].apply(normalize_text)
non_moderated_df['message'] = non_moderated_df['message'].apply(normalize_text)

# Preprocessing: Remove duplicates based on 'msg_sent' column in moderated_df and 'message' in non_moderated_df
moderated_df = moderated_df.drop_duplicates(subset='msg_sent')
non_moderated_df = non_moderated_df.drop_duplicates(subset='message')
input_df = input_df.drop_duplicates(subset='text')

print(len(moderated_df))
print(len(non_moderated_df))
print(len(input_df))

# Combine data from both files
moderated_texts = moderated_df[['msg_sent']].copy()
moderated_texts['twitch_output'] = 1

non_moderated_texts = non_moderated_df[['message']].copy()
non_moderated_texts.rename(columns={'message': 'msg_sent'}, inplace=True)
non_moderated_texts['twitch_output'] = 0

# Concatenate the two dataframes
combined_df = pd.concat([moderated_texts, non_moderated_texts], ignore_index=True)

unmatched_msg_sent = []

# Process each msg_sent in output_data
for output_text in combined_df['msg_sent']:
    # Check if output_text exists in input_data['text'] exactly
    exact_match = input_df['text'] == output_text

    if exact_match.any():
        # If exact match exists, no changes needed
        continue

    # Check if output_text is a prefix of any input_data['text']
    prefix_match = input_df['text'].apply(lambda x: x.startswith(output_text))

    if prefix_match.any():
        # Truncate the matching input text to match output_text
        input_df.loc[prefix_match, 'text'] = output_text
    else:
        # Track unmatched msg_sent for review
        unmatched_msg_sent.append(output_text)

unmatched_msg_sent_df = pd.DataFrame({'unmatched_msg_sent': unmatched_msg_sent})

len(unmatched_msg_sent), input_df.shape
print(len(unmatched_msg_sent))
unmatched_msg_sent_df.to_csv("unmatched_ihc.csv")

# Total examples
total_examples = len(input_df)

# Examples non-moderated
non_moderated_count = len(combined_df[combined_df['twitch_output'] == 0])

# Examples moderated due to filter
moderated_filter_count = total_examples - non_moderated_count

# Calculate percentages
non_moderated_percent = (non_moderated_count / total_examples) * 100
moderated_percent = (moderated_filter_count / total_examples) * 100

# Display results
print(f"Total examples: {total_examples}")
print(f"Non-moderated examples: {non_moderated_count} ({non_moderated_percent:.2f}%)")
print(f"Total moderated examples: {moderated_filter_count} ({moderated_percent:.2f}%)")

merged_data = input_df.merge(combined_df, left_on='text', right_on='msg_sent', how='left', indicator=True)
print(len(merged_data))
merged_data['twitch_output'] = merged_data['twitch_output'].fillna(2)
print(input_df.columns)
print(combined_df.columns)
print(merged_data.columns)

# Fill missing label values with 0
merged_data['moderation'] = merged_data['twitch_output'].apply(lambda x: 1 if x in [1, 2] else 0)
    
print(merged_data['moderation'].value_counts())

TN = len(merged_data[(merged_data['label'] ==0) & (merged_data['moderation'] == 0)])
FP = len(merged_data[(merged_data['label'] ==0) & (merged_data['moderation'] == 1)])
TP = len(merged_data[(merged_data['label'] ==1) & (merged_data['moderation'] == 1)])
FN = len(merged_data[(merged_data['label'] ==1) & (merged_data['moderation'] == 0)])

Dynahate_Global = merged_data[(merged_data['twitch_output'] ==2)]
Dynahate_Global['text'].to_csv("global_ihc.csv",index=False)

print("Global flagged:", len(merged_data[merged_data['twitch_output']==2]))
print("True Negative (TN):", TN)
print("False Positive (FP):", FP)
print("True Positive (TP):", TP)
print("False Negative (FN):", FN)

precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1_score = 2 * (precision * recall) / (precision + recall)
accuracy = (TP + TN) / (TP + TN + FP + FN)

print("Precision:", precision)
print("Recall:", recall)
print("F1=score:",f1_score)
print("Accuracy:", accuracy)

merged_data.to_csv('ihc_Level1.csv', index=False)


