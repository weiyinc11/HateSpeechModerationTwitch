# Datasets

This directory contains scripts to preprocess and classify the original datasets into three experimental levels used for content moderation analysis.

## Structure

| File Name                                | Description |
|------------------------------------------|-------------|
| `DynaHate_Dataset_Creation.py`           | Script for preprocessing the DynaHate dataset and generating sub-datasets for all three experimental levels. |
| `Dynamically Generated Hate Dataset v0.2.3 (1).csv` | Original DynaHate dataset used as the source for generating level-wise sub-datasets. |
| `SBIC_Dataset_Creation.py`               | Script for preprocessing the SBIC (Social Bias Inference Corpus) dataset and generating sub-datasets for all three experimental levels. |
| `SBIC.v2.trn.csv`                        | Original SBIC dataset used as the source for generating sub-datasets. |
| `toxigen_Dataset_Creation.py`            | Script for preprocessing the ToxiGen dataset and generating sub-datasets for all three experimental levels. |
| `toxigen.csv`                            | Preprocessed ToxiGen dataset used for evaluation. |
| `IHC.csv`                                | Implicit Hate Corpus (IHC) dataset, used specifically for Level 1 experiments. |

## Column Descriptions (by Dataset)

Below are the key columns used from each dataset in this project, along with their descriptions.

---

### DynaHate
| Column | Description |
|--------|-------------|
| `text`   | The full textual content of the sample. |
| `label`  | Binary label indicating whether the sample is hateful (1) or not (0). |
| `type`   | Category or type of hate (e.g., racial, religious). |
| `target` | The specific group or entity targeted by the hateful content. |

---

### SBIC (Social Bias Inference Corpus)
| Column            | Description |
|-------------------|-------------|
| `post`             | The actual post or statement that was annotated. |
| `intentYN`         | Indicates whether the intent behind the post was to offend (`Yes`/`No`). |
| `offensiveYN`      | Indicates whether the post could be considered offensive. |
| `sexYN`            | Flags if the content contains sexual or lewd references. |
| `whoTarget`        | Specifies whether the statement targets an individual or a group. |
| `targetMinority`   | The demographic group targeted by the post, if any. |
| `targetCategory`   | High-level classification of the targeted group (e.g., gender, race). |
| `targetStereotype` | The stereotype or biased assumption implied by the post. |

---

### ToxiGen
| Column            | Description |
|-------------------|-------------|
| `generation`       | The generated text sample. This is text thats passed in experiment. |
| `group`            | The demographic or identity group mentioned or targeted. |
| `prompt_label`     | Prompt label is the binary value indicating whether or not the prompt is toxic |
| `roberta_prediction` | The probability predicted by RoBERTa model for each instance. |

---

### IHC (Implicit Hate Corpus)
| Column | Description |
|--------|-------------|
| `text`   | The sentence or post potentially containing implicit hate. |
| `label`  | Indicates whether the post is hateful (`1`) or not (`0`). |


## Usage

Each script can be executed independently to (re)generate or preprocess the corresponding dataset. Ensure that the required dependencies (e.g., `pandas`, `numpy`) are installed before running the scripts.

Example:
```bash
python DynaHate_Dataset_Creation.py
