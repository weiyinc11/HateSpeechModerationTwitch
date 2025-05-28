# Counterfactual Analysis

This module evaluates the performance of content moderation systems on counterfactual examples where targeted slurs are selectively introduced into hate speech samples.

## Structure

### Data/
| File Name | Description |
|-----------|-------------|
| `Original(Hate_related_to_BlackJewishMuslims_noslurs).csv` | Original hate samples without explicit slurs targeting Black, Jewish, and Muslim communities. |
| `Counter(Hate_related_to_BlackJewishMuslims_slurs).csv`    | Counterfactual samples created by inserting group-specific slurs into the original texts. |

### Results/
| File Name | Description |
|-----------|-------------|
| `Hate_related_to_BlackJewishMuslims_slurs_mod.csv`            | Subset of slur-inserted samples that were flagged by the moderation system. |
| `Hate_related_to_BlackJewishMuslims_noslurs_mod.csv`            | Subset of non-slur samples that were flagged by the moderation system. |
| `Hate_related_to_BlackJewishMuslims_slurs_1_notMod.csv`     | Subset of slur-inserted samples that were not flagged by the moderation system. |
| `Hate_related_to_BlackJewishMuslims_noslurs_1_notMod.csv`   | Subset of non-slur samples that were not flagged by the moderation system. |


## Usage

- Review the `Data` folder for input samples.
- Results in the `Results` folder indicate moderation decisions.
- Analysis can help identify if moderation systems are disproportionately sensitive to specific keywords rather than semantic intent.

