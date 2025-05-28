# Level 2: Filterwise Analysis

This module evaluates how effectively **individual 'Discrimination and Slur' related filters** detect specific categories of hate speech. It isolates the behavior of each filter through controlled experiments across three test scenarios.

## Objective

The analysis focuses on four types of hate-related filters:

1. **Disability**
2. **Sex, Sexuality, or Gender (SSG)**
3. **Misogyny**
4. **Race, Ethnicity, or Religion (RER)**

The goal is to determine:
- How accurately each filter detects relevant content
- How filters behave in isolation or in combination
- Overlaps, gaps, and blind spots in moderation logic

---

## Test Case Design

Each dataset is tested under three experimental scenarios:

| Case | Description |
|------|-------------|
| **Case 1** | Only the **relevant filter** is ON; the other three are OFF. |
| **Case 2** | All filters are ON **except the relevant one**. |
| **Case 3** | **All four filters are ON** simultaneously. |

These scenarios help assess both the **coverage** and **specificity** of moderation filters.

---

## Folder Structure
```plaintext
DatasetName/
├── Case1_Relevant_filter_only_on/
├── Case2_All_but_relevant_on/
└── Case3_All_filters_on/
```

Each case folder follows a general structure where file names are based on the hate category being evaluated. The same naming pattern applies for all hate categories:

| File Name | Description |
|-----------|-------------|
| `level2C*_disabilityMod.csv`    | Moderated examples related to Disability hate in Case *. |
| `level2C*_disabilityNotMod.csv`| Unmoderated examples related to Disability hate in Case *. |
| `*_hate.csv`                   | Input subset of examples for the relevant hate category. |
| `analysis.py`                  | Script to compute stats and generate global result files. |

---

### 🔀 `merged_files/` Subfolder

Each case folder includes a `merged_files/` directory that contains:

- **Merged moderation result files for each hate category**.
- Each file aggregates examples from **all datasets** for a specific category (e.g., disability, misogyny).
- Helps evaluate **filter performance across datasets**, rather than just within a single dataset.

---

## Global Output Files

Running `analysis.py` in a dataset folder generates two types of outputs:

| File Name | Description |
|-----------|-------------|
| `Dataset_Level2_*_results.csv`   | Summary results of Case * across all hate categories. |
| `Dataset_Level2_*_analysis.csv` | Final metric-based analysis file for Case *. |

### Columns in `*_analysis.csv`

| Column                | Description |
|------------------------|-------------|
| `file_name`            | Category or filename. |
| `total_messages`       | Number of input messages. |
| `automod_flagged_msgs` | Count of flagged messages by Automod. |
| `not_flagged_msgs`     | Count of unflagged messages. |
| `twitch_flagged_msgs`  | Count of prefiltered messages. |
| `total_flagged_msgs`   | Combined total of flagged messages. |
| `moderation_rate`      | Ratio of moderated to total messages. |
| `non_mod_rate`         | Ratio of unmoderated to total messages. |
| `unmatched`            | Messages excluded due to encoding or errors. |
| `ableism`, `misogyny`, `racism`, `homophobia` | Number of examples classified in each category by Automod. |
| `level_1` to `level_4` | Number of examples classified in each level or severity by Automod. |

---

## Notes

- File naming follows the pattern:  
  `level2C[case_number]_[hate_type]{Mod,NotMod}.csv`
  
- `merged_files` offer a macro-level understanding of cross-dataset moderation performance for each hate type.
