# Robustness Analysis

This module evaluates the robustness of content moderation systems against adversarial attacks applied to hate-indicative phrases. It tests whether obfuscation techniques can bypass moderation filters.

## Structure

### Input/
| File Name                            | Description |
|--------------------------------------|-------------|
| `Merged_Adversarial_Perturbations.csv` | Dataset containing adversarially perturbed phrases generated using various obfuscation techniques. |

#### Column Descriptions
| Column     | Description |
|------------|-------------|
| `Fragment` | Sensitive term or keyword being perturbed. |
| `Method`   | Type of adversarial modification applied (e.g., punctuation, spacing, phonetic play). |
| `text`     | Full sentence after the perturbation has been applied. |

### Results/
| File Name                                       | Description |
|------------------------------------------------|-------------|
| `Merged_Adversarial_Perturbations_mod.csv`       | Adversarial examples that were flagged by the moderation system.  |
| `Merged_Adversarial_Perturbations_1_notMod.csv`| Adversarial examples that were not flagged by the moderation system. |

## Usage

- Refer to the `Input` file to study how various perturbations were crafted.
- Use the `Results` files to assess which perturbations successfully bypassed moderation.
- Focus on `*_notMod.csv` to identify failure cases.
