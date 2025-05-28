# Level 1: Overall Analysis

This directory contains results for **Level 1** - Overall analysis of automod hate ralated filters for moderation. At this level, automod is evaluated on its ability to detect **hateful content** across various datasets. For all the experiments where filter level is not mentioned take it as **maximum filtration** of automod.

## Structure

### 1. Context_awareness_experiment/
| File Name                     | Description |
|-------------------------------|-------------|
| `Hate.csv`                    | Dataset containing 100 hateful examples. |
| `Hate_Mod.csv`                | Moderated examples from the hate dataset. |
| `Hate_notMod.csv`            | Unflagged examples from the hate dataset. |
| `HateNonhateboth.csv`        | Mixed dataset with both hate and non-hate samples interleaved. |
| `HateNonhateboth_Mod.csv`    | Moderated examples from the mixed dataset. |
| `HateNonhateboth_notMod.csv`| Unflagged examples from the mixed dataset. |

> **Goal:** Evaluate whether moderation is sensitive to context. `Hate.csv` file contains 100 hateful examples and `HateNonhateboth.csv` contains 100 hate and 100 nonhate examples interleaved. These can help in understanding whether the surrounding context matters in moderation decision or not. 

---

### 2. Dynahate/
| File Name            | Description |
|----------------------|-------------|
| `Dynahate.csv`| Dataset. |
| `Dynahate_mod.csv`   | examples flagged by the automod from Dataset. |
| `Dynahate_notmod.csv`| examples that are not flagged by the automod from Dataset. |
| `dynahate_Level1.csv`| Level 1 analysis of the DynaHate dataset. |
| `global_dynahate.csv`| prefiltered examples (flagged before sending). |
| `unmatched_dynahate.csv`| Samples unmatched due to encoding/noise. |
| `analysis.py`            | Script for computing statastics(precision, recall, and other metrics and generation `*_Level1.csv`,`global_*.csv` and `unmatched_*.csv`). |

---

### 3. SBIC/
Similar structure to Dynahate:
| File Name            | Description |
|----------------------|-------------|
| `SBIC.csv`| Dataset. |
| `SBIC_mod.csv`   | examples flagged by the automod from Dataset. |
| `SBIC_notmod.csv`| examples that are not flagged by the automod from Dataset. |
| `sbic_Level1.csv`| Level 1 analysis of the SBIC dataset. |
| `global_sbic.csv`| prefiltered examples (flagged before sending). |
| `unmatched_sbic.csv`| Samples unmatched due to encoding/noise. |
| `analysis.py`            | Script for computing statastics(precision, recall, and other metrics and generation `*_Level1.csv`,`global_*.csv` and `unmatched_*.csv`). |


---

### 3. SBIC/
Similar structure to Dynahate:
| File Name            | Description |
|----------------------|-------------|
| `Toxigen.csv`| Dataset. |
| `Toxigen_mod.csv`   | examples flagged by the automod from Dataset. |
| `Toxigen_notmod.csv`| examples that are not flagged by the automod from Dataset. |
| `toxigen_Level1.csv`| Level 1 analysis of the Toxigen dataset. |
| `global_toxigen.csv`| prefiltered examples (flagged before sending). |
| `unmatched_toxigen.csv`| Samples unmatched due to encoding/noise. |
| `analysis.py`            | Script for computing statastics(precision, recall, and other metrics and generation `*_Level1.csv`,`global_*.csv` and `unmatched_*.csv`). |

---

### 5. IHC/
IHC experiments are conducted across five filter levels:
- `No_filter`, `Less_filter`, `Some_filter`, `More_filter`, `Max_filter`

Each folder follows a structure similar to other datasets. Below is the structure for **Max_filter**:

| File Name            | Description |
|----------------------|-------------|
| `IHC.csv`| Dataset. |
| `IHC_mod.csv`   | examples flagged by the automod from Dataset. |
| `IHC_notmod.csv`| examples that are not flagged by the automod from Dataset. |
| `ihc_Level1.csv`| Level 1 analysis of the IHC dataset. |
| `global_ihc.csv`| prefiltered examples (flagged before sending). |
| `unmatched_ihc.csv`| Samples unmatched due to encoding/noise. |
| `analysis.py`            | Script for computing statastics(precision, recall, and other metrics and generation `*_Level1.csv`,`global_*.csv` and `unmatched_*.csv`). |

## Column Descriptions for `*_Level1.csv`

These files contain detailed moderation results derived from the original datasets and additional annotations from the moderation system.

| Column Name     | Description |
|------------------|-------------|
| *(Input columns)* | All columns from the original dataset are retained (e.g., `text`, `label`, `target`). |
| `msg_sent`        | The message that was actually sent to the chatbox or moderation system. |
| `twitch_output`   | Output label from the moderation system:<br> `0` – Unflagged<br> `1` – Flagged<br> `2` – Prefiltered (blocked before submission). |
| `moderation`      | Final moderation status:<br> `0` – Not moderated (same as unflagged)<br> `1` – Moderated (includes flagged and prefiltered). |

---

## Notes

- All CSV files contain moderation outcomes, generally divided into flagged (`*_mod.csv`) and not flagged (`*_notMod.csv`) sets.
- Scripts such as `analysis.py` are used to calculate differences in moderation results and identify unmatched samples.

