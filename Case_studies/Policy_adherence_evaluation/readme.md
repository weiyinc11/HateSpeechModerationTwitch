# Policy Adherence Evaluation

This module assesses how well the twitch's automod systems adhere to defined platform policies by analyzing system responses under varying filtration levels of automod.

## Structure

### Data/
| File Name                 | Description |
|---------------------------|-------------|
| `final_200_examples.csv`  | Dataset of 200 curated examples used to evaluate adherence to moderation policies across different settings. |

#### Column Descriptions
| Column Name       | Description |
|-------------------|-------------|
| `phrase`          | The potentially sensitive or targeted term being evaluated (e.g., "bitches"). |
| `text`            | Full sentence or phrase containing the term, representing a real-world usage scenario. |
| `type of example` | Contextual classification of the phrase, such as: `empowering`, `music`, `endearing`, `educational`, etc. |


### Results/
| File Name                                      | Description |
|------------------------------------------------|-------------|
| `final_200_examples_MaxFiltration_mod.csv`       | Subset of moderated content under maximum-filtration . |
| `final_200_examples_SomeFiltration_mod.csv`      | Subset of moderated content under some-filtration. |
| `final_200_examples_NoFiltration_mod.csv`       | Subset of moderated content under no-filtration. |
| `final_200_examples_MaxFiltration_1_notMod.csv`| Subset of unmoderated content under maximum-filtration. |
| `final_200_examples_SomeFiltration_1_notMod.csv`| Subset of unmoderated content under partial-filtration. |
| `final_200_examples_NoFiltration_1_notMod.csv` | Subset of unmoderated content under no-filtration. |


## Usage

- Begin with `final_200_examples.csv` to understand the dataset used.
- Examine results across filtration levels to compare moderation consistency.

