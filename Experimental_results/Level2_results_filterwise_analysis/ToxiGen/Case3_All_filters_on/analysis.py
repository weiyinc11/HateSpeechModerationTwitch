# import pandas as pd
# import os

# def analyze_file(input_file, moderated_file, non_moderated_file):
#     # Load CSVs into dataframes
#     input_df = pd.read_csv(input_file)
#     moderated_df = pd.read_csv(moderated_file)
#     non_moderated_df = pd.read_csv(non_moderated_file, on_bad_lines="skip", engine="python")
    
#     # Define patterns to remove
#     patterns = ['!dice', '!audit', r'You rolled a [1-6]']
#     regex_pattern = '|'.join(patterns)
#     non_moderated_df = non_moderated_df[~non_moderated_df['message'].str.match(regex_pattern, na=False)]
    
#     # Preprocessing: Remove duplicates
#     moderated_df = moderated_df.drop_duplicates(subset='msg_sent')
#     non_moderated_df = non_moderated_df.drop_duplicates(subset='message')
#     input_df = input_df.drop_duplicates(subset='text')
    
#     # Metrics calculation
#     total_messages = len(input_df)
#     automod_flagged = len(moderated_df)
#     notflagged_messages = len(non_moderated_df)
#     twitch_flagged = total_messages - (automod_flagged + notflagged_messages)
#     total_flagged = automod_flagged + twitch_flagged
#     moderation_rate = (total_flagged / total_messages) * 100
#     notmoderated_rate = (notflagged_messages / total_messages) * 100
    
#     # Category and severity distributions
#     category_distribution = moderated_df['content_category'].value_counts()
#     severity_distribution = moderated_df['category_level'].value_counts()
    
#     # Consolidate results
#     result = {
#         "file_name": os.path.basename(input_file),
#         "total_messages": total_messages,
#         "automod_flagged_msgs": automod_flagged,
#         "not_flagged_msgs": notflagged_messages,
#         "twitch_flagged_msgs": twitch_flagged,
#         "total_flagged_msgs": total_flagged,
#         "moderation_rate": moderation_rate,
#         "non_mod_rate": notmoderated_rate
#     }
    
#     # Add category and severity counts to the result
#     result.update(category_distribution.to_dict())
#     result.update(severity_distribution.add_prefix("level_").to_dict())
    
#     return result

# def process_multiple_files(file_groups, output_csv):
#     results = []
#     for group in file_groups:
#         result = analyze_file(group['input'], group['moderated'], group['non_moderated'])
#         results.append(result)
    
#     # Save results to CSV
#     results_df = pd.DataFrame(results)
#     results_df.to_csv(output_csv, index=False)
#     print(f"Results saved to {output_csv}")

# # Example usage
# file_groups = [
#     {
#         "input": "disability_subset.csv",
#         "moderated": "disability_subset_1.csv",
#         "non_moderated": "disability_subset_1_notMod.csv"
#     },
#     {
#         "input": "misogyny_subset.csv",
#         "moderated": "misogyny_subset_1.csv",
#         "non_moderated": "misogyny_subset_1_notmod.csv"
#     },
#     {
#         "input": "race,_ethnicity,_or_religion_subset.csv",
#         "moderated": "race,_ethnicity,_or_religion_subset_1.csv",
#         "non_moderated": "race,_ethnicity,_or_religion_subset_1_notMod.csv"
#     },
#     {
#         "input": "sexuality,_sex,_or_gender_subset.csv",
#         "moderated": "sexuality,_sex,_or_gender_subset_1.csv",
#         "non_moderated": "sexuality,_sex,_or_gender_subset_1_notMod.csv"
#     }
# ]

# output_csv = "analysis_results.csv"
# process_multiple_files(file_groups, output_csv)
import pandas as pd
import re
import unicodedata
import os

# Normalize text function
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

# Analysis function
def analyze_file(input_file, moderated_file, non_moderated_file):
    # Load CSVs into dataframes
    # Load CSVs into dataframes
    input_df = pd.read_csv(input_file)
    moderated_df = pd.read_csv(moderated_file)
    non_moderated_df = pd.read_csv(non_moderated_file, on_bad_lines="skip", engine="python")
    
    # Normalize text
    input_df['text'] = input_df['text'].apply(normalize_text)
    moderated_df['msg_sent'] = moderated_df['msg_sent'].apply(normalize_text)
    non_moderated_df['message'] = non_moderated_df['message'].apply(normalize_text)
    patterns = ['!dice', '!audit', r'You rolled a [1-6]']

# Create a regex pattern that matches any of the defined patterns
    regex_pattern = '|'.join(patterns)
    non_moderated_df = non_moderated_df[~non_moderated_df['message'].str.match(regex_pattern, na=False)]
    # Remove duplicates
    moderated_df = moderated_df.drop_duplicates(subset='msg_sent')
    non_moderated_df = non_moderated_df.drop_duplicates(subset='message')
    input_df = input_df.drop_duplicates(subset='text')
    
    # Combine moderated and non-moderated texts
    moderated_texts = moderated_df[['msg_sent']].copy()
    moderated_texts['twitch_output'] = 1

    non_moderated_texts = non_moderated_df[['message']].copy()
    non_moderated_texts.rename(columns={'message': 'msg_sent'}, inplace=True)
    non_moderated_texts['twitch_output'] = 0

    combined_df = pd.concat([moderated_texts, non_moderated_texts], ignore_index=True)

    # Handle unmatched msg_sent 
    unmatched_msg_sent = []
    for output_text in combined_df['msg_sent']:
        exact_match = input_df['text'] == output_text
        if exact_match.any():
            continue

        prefix_match = input_df['text'].apply(lambda x: x.startswith(output_text))
        if prefix_match.any():
            input_df.loc[prefix_match, 'text'] = output_text
        else:
            unmatched_msg_sent.append(output_text)

    
    # Left merge with input_df
    merged_df = input_df.merge(combined_df, left_on='text', right_on='msg_sent', how='left')

    # Assign label 2 to rows without a label
    merged_df['twitch_output'] = merged_df['twitch_output'].fillna(2)

    # Add 'moderation' column
    merged_df['moderation'] = merged_df['twitch_output'].apply(lambda x: 1 if x in [1, 2] else 0)

    # Calculate metrics
    total_messages = len(input_df)
    automod_flagged = (merged_df['twitch_output'] == 1).sum()
    notflagged_messages = (merged_df['twitch_output'] == 0).sum()
    twitch_flagged = (merged_df['twitch_output'] == 2).sum()
    total_flagged = (merged_df['moderation'] == 1).sum()
    moderation_rate = (total_flagged / total_messages) * 100
    notmoderated_rate = (notflagged_messages / total_messages) * 100
    unmatched = len(unmatched_msg_sent)

    # Consolidate results
    category_distribution = moderated_df['content_category'].value_counts()
    severity_distribution = moderated_df['category_level'].value_counts()
    result = {
        "file_name": os.path.basename(input_file),
        "total_messages": total_messages,
        "automod_flagged_msgs": automod_flagged,
        "not_flagged_msgs": notflagged_messages,
        "twitch_flagged_msgs": twitch_flagged,
        "total_flagged_msgs": total_flagged,
        "moderation_rate": moderation_rate,
        "non_mod_rate": notmoderated_rate,
        "unmatched" : unmatched
    }
    
    # Add category and severity counts to the result
    result.update(category_distribution.to_dict())
    result.update(severity_distribution.add_prefix("level_").to_dict())
    
    return result, merged_df

# Process multiple files
def process_multiple_files(file_groups, output_csv, merged_output_dir):
    results = []
    for group in file_groups:
        result, merged_df = analyze_file(group['input'], group['moderated'], group['non_moderated'])
        results.append(result)
        
        # Save individual merged DataFrame for each file
        merged_filename = os.path.join(merged_output_dir, f"{result['file_name']}_merged.csv")
        merged_df.to_csv(merged_filename, index=False)
        print(f"Merged file saved to {merged_filename}")
    
    # Save aggregated results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

import re
import glob

def concatenate_merged_files(merged_output_dir, output_file):
    """
    Concatenate all merged files in the specified directory into a single file.
    Adds a column indicating the filter type or dataset name from the file name.
    """
    all_files = glob.glob(f"{merged_output_dir}/*.csv")  # Get all CSV files in the directory
    concatenated_data = []

    for file in all_files:
        df = pd.read_csv(file)
        # Extract the dataset name by removing "_merged.csv" from the file name
        dataset_name = re.sub(r"_merged\.csv$", "", os.path.basename(file))
        df['source_file'] = dataset_name  # Add the dataset name as the source column
        concatenated_data.append(df)

    # Concatenate all DataFrames
    concatenated_df = pd.concat(concatenated_data, ignore_index=True)
    concatenated_df.to_csv(output_file, index=False)
    print(f"All merged files concatenated into {output_file}")

file_groups = [
    {
        "input": "disability_hate.csv",
        "moderated": "level2C3_disabilityMod.csv",
        "non_moderated": "level2C3_disabilityNotMod.csv"
    },
    {
        "input": "misogyny_hate.csv",
        "moderated": "level2C3_misogynyMod.csv",
        "non_moderated": "level2C3_misogynyNotMod.csv"
    },
    {
        "input": "race_ethnicity_religion_hate.csv",
        "moderated": "level2C3_RERMod.csv",
        "non_moderated": "level2C3_RERNotMod.csv"
    },
    {
        "input": "sexuality_sex_gender_hate.csv",
        "moderated": "level2C3_SSGMod.csv",
        "non_moderated": "level2C3_SSGNotMod.csv"
    }
]

output_csv = "ToxiGen_Level2_allfilters_analysis.csv"
merged_output_dir = "merged_files"
os.makedirs(merged_output_dir, exist_ok=True)
process_multiple_files(file_groups, output_csv, merged_output_dir)
# Example usage
concatenated_output_file = "ToxiGen_Level2_allfilters_results.csv"
concatenate_merged_files(merged_output_dir, concatenated_output_file)