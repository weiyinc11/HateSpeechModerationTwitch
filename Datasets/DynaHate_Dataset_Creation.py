# -*- coding: utf-8 -*-
"""Dynahate_Preprocessing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14LmN-Xl_fEYxtuZwt5VkwLfk-SnL7Q9t
"""

import pandas as pd
import re
from html import unescape

# Load the dataset
df = pd.read_csv("/content/Dynamically Generated Hate Dataset v0.2.3 (1).csv")  # Replace with your actual file path

# Select only the specified columns
df = df[['text', 'label', 'type', 'target']]

# Replace 'hate' with 1 and 'nothate' with 0 in the 'label' column
df['label'] = df['label'].map({'hate': 1, 'nothate': 0})

# Remove examples that exceed the 500-character limit
df = df[df['text'].str.len() <= 500]
print(len(df))

df['text'] = df['text'].apply(lambda x: re.sub(r'@\S+', '', x))

# 2. Convert HTML entities to their respective emojis
df['text'] = df['text'].apply(unescape)

# 3. Remove duplicate examples based on the 'text' column
df = df.drop_duplicates(subset='text')

# Save the cleaned dataset to a CSV file
total_data_points = len(df)
total_hate = df['label'].sum()

hate_df = df[df['label'] == 1]
df.to_csv("dynahate.csv", index=False)
hate_df.to_csv("only_hate_dynahate.csv", index=False)
print(len(df))
print(len(hate_df))

hate_df = hate_df[(hate_df['label'] == 1) & (hate_df['type'] != 'notgiven') & (hate_df['target'] != 'notgiven')]
# Split the 'target' column into individual targets and flatten the list
all_targets = hate_df['target'].dropna().apply(lambda x: x.split(',')).explode()
# print(len(hate_df))
# Get unique targets
unique_targets = all_targets.str.strip().unique()

# Print the results
print(f"Total unique targets: {len(unique_targets)}")
print(f"Unique targets: {unique_targets}")

import os
import zipfile
import pandas as pd

# Function to filter rows based on a list of targets
def filter_by_targets(df, target_list):
    return df[df['target'].fillna('').apply(lambda x: any(t in str(x).split(',') for t in target_list))]

# Define the target mappings for each Twitch filter
twitch_filters = {
    "Disability": ['dis'],
    "Sexuality, sex, or gender": ['gay', 'gay.man', 'gay.wom', 'bis', 'trans', 'gendermin', 'lgbtq'],
    "Misogyny": ['wom', 'gay.wom', 'mus.wom', 'asi.wom', 'indig.wom', 'non.white.wom', 'bla.wom'],
    "Race, ethnicity, or religion": [
        'bla', 'mus', 'jew', 'indig', 'for', 'asi.south', 'asi.east', 'asi.chin', 'arab',
        'hispanic', 'pol', 'african', 'ethnic.minority', 'russian', 'mixed.race', 'asi.pak',
        'eastern.europe', 'non.white', 'other.religion', 'other.national', 'nazis', 'hitler',
        'trav', 'ref', 'asi', 'asylum', 'asi.man', 'bla.man', 'bla.wom'
    ],
}

# Create subsets for each filter
hate_df = pd.read_csv("only_hate_dynahate.csv")  # Replace with your actual file path

disability_df = filter_by_targets(hate_df, twitch_filters["Disability"])
sexuality_sex_gender_df = filter_by_targets(hate_df, twitch_filters["Sexuality, sex, or gender"])
misogyny_df = filter_by_targets(hate_df, twitch_filters["Misogyny"])
race_ethnicity_religion_df = filter_by_targets(hate_df, twitch_filters["Race, ethnicity, or religion"])

# Print subset statistics
print(f"Disability subset size: {len(disability_df)}")
print(f"Sexuality, sex, or gender subset size: {len(sexuality_sex_gender_df)}")
print(f"Misogyny subset size: {len(misogyny_df)}")
print(f"Race, ethnicity, or religion subset size: {len(race_ethnicity_religion_df)}")

# Create a folder to save CSV files
output_folder = "Level2_Dynahate"
os.makedirs(output_folder, exist_ok=True)

# Save the subsets into the folder
disability_df.to_csv(f"{output_folder}/disability_hate.csv", index=False)
sexuality_sex_gender_df.to_csv(f"{output_folder}/sexuality_sex_gender_hate.csv", index=False)
misogyny_df.to_csv(f"{output_folder}/misogyny_hate.csv", index=False)
race_ethnicity_religion_df.to_csv(f"{output_folder}/race_ethnicity_religion_hate.csv", index=False)

# Zip the folder
zip_file = "Level2_Dynahate.zip"
with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            zipf.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file), os.path.join(output_folder, '..')))

print(f"All files saved in {output_folder} and zipped as {zip_file}")

import os
import pandas as pd
import zipfile

# Define the updated mapping
category_mapping = {
    "Disability": {
        "Physical or Mental Disabilities": ["dis"]
    },
    "Sexuality, Sex, or Gender": {
        "Men": ["gay.man", "asi.man", "bla.man"],
        "Gender and Identity": ["trans", "gendermin", "lgbtq","gay", "bis"]
    },
    "Misogyny": {
        "Women": ["wom", "gay.wom", "mus.wom", "asi.wom", "indig.wom", "non.white.wom","bla.wom"],
    },
    "Race, Ethnicity, or Religion (RER)": {
        "Black": ["bla", "bla.man", "bla.wom"],
        "Asian": ["asi.south", "asi.pak", "asi.east", "asi.chin"],
        "Hindu": ["indig"],
        "Muslim": ["mus", "mus.wom"],
        "Jewish": ["jew"],
        "Ethnic Minority": ["mixed.race", "ethnic.minority"],
        "Immigrants": ["ref", "asylum", "for"],
        "Nationalities": ["pol", "russian", "eastern.europe", "arab", "hispanic"]
    }
}

# Load the hate_df dataset
hate_df = pd.read_csv("only_hate_dynahate.csv")  # Replace with your actual file path

# Function to filter rows based on a list of targets
def filter_by_targets(df, target_list):
    return df[df['target'].fillna('').apply(lambda x: any(t in str(x).split(',') for t in target_list))]

# Create Level 2 datasets and save them under Level 2 folders
output_folder = "Level3_Dynahate"
os.makedirs(output_folder, exist_ok=True)

print("Dataset sizes:")
for level3_category, subcategories in category_mapping.items():
    # Create folder for the Level 2 category
    level3_folder = os.path.join(output_folder, level3_category.replace(" ", "_"))
    os.makedirs(level3_folder, exist_ok=True)

    for subcategory, targets in subcategories.items():
        # Create folder for the subcategory
        subcategory_folder = os.path.join(level3_folder, subcategory.replace(" ", "_"))
        os.makedirs(subcategory_folder, exist_ok=True)

        # Filter dataset and save
        subset = filter_by_targets(hate_df, targets)
        subset.to_csv(os.path.join(subcategory_folder, f"{subcategory.replace(' ', '_')}.csv"), index=False)
        print(f"{level3_category} -> {subcategory}: {len(subset)}")

# Zip the Level 2 folder
zip_file = "Level3_Dynahate.zip"
with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            zipf.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file), os.path.join(output_folder, '..')))

print(f"Level 3 datasets saved in {output_folder} and zipped as {zip_file}")

