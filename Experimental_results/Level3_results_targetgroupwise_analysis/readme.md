# Level 3: Target Group-wise Analysis

This module evaluates how effectively automod filters detect **hate targeted at specific community/target group**. Experiments are structured to isolate the impact of filter configuration on each target group.

## Objective

The analysis focuses on how well each of the following moderation filters handle hate directed at the following communities:

| Filter Category | Communities Evaluated |
|------------------|------------------------|
| Disability       | `physical_ableism`, `mental_ableism` |
| Sex, Sexuality, or Gender (SSG)         | `misandry` |
| Race, Ethnicity, or Religion (RER) | `anti_black`, `anti_semitism`, `islamophobia` |

---

## Test Case Design

Each group is evaluated using three moderation configurations:

| Case | Description |
|------|-------------|
| **Case 1** | Only the **relevant filter** is ON; other three filters are OFF. |
| **Case 2** | All filters are ON **except** the relevant one. |
| **Case 3** | **All filters are ON** together. |

---

## Folder Structure
```plaintext
DatasetName/
├── Case1_Relevant_filter_only_on/
├── Case2_All_but_relevant_on/
└── Case3_All_filters_on/
```

## Case Folder Contents

Each case folder contains the following files for each community:

| File Name Format | Description |
|------------------|-------------|
| `level3C*_antiblackMod.csv`     | Moderated (flagged) examples for the specified community (eg. antiblack) in Case *. |
| `level3C*_antiblackNotMod.csv`  | Unmoderated (not flagged) examples for the specified community(eg. antiblack) in Case *. |
| `antiblack.csv`                 | Input subset of hate samples related to that target group (eg. antiblack). |
| `analysis.py`                  | Script to compute statistics and generate result/analysis files. |

> **Note:** The above format generalizes to all communities:
> - `level3C*_misandryMod.csv`, `level3C*_islamophobiaNotMod.csv`, etc.

---

### 🔀 `merged_files/` Subfolder

Each case folder includes a `merged_files/` directory that contains:

- **Merged moderation result files for each hate community/target group**.
- Each file aggregates examples from **all datasets** for a specific community (e.g., antiblack, islamophobia).
- Helps evaluate **filter performance across datasets**, rather than just within a single dataset.

---

## Global Output Files

Running `analysis.py` inside a dataset folder generates:

| File Name | Description |
|-----------|-------------|
| `Dataset_Level3_onlyX_results.csv`   | Combined result summary for Case X across all communities. |
| `Dataset_Level3_onlyX_analysis.csv` | Detailed statistical analysis for Case X. |

### Columns in `*_analysis.csv`

| Column                | Description |
|------------------------|-------------|
| `file_name`            | Community name or result file name. |
| `total_messages`       | Total messages in the evaluated subset. |
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
  `level3C[case_number]_[target_group]{Mod,NotMod}.csv`
