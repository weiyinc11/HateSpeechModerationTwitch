# Silencing Empowerment, Allowing Bigotry: Auditing the Moderation of Hate Speech on Twitch 
In this paper, we conduct an audit of Twitch's Machine Learning Content Moderation tool `automod` via Twitch API and IRC tools. Sending over 107,000 messages collated from 4 hatespeech datasets, we measure the efficacy of `automod` on flagging hateful content. See our paper for more details about our motivation, experimental design, measurements of efficacy and further considerations. 

## Open Source Code Documentation
## 1. File Structure of `/contentTester`
    ├── bashScript
    │   └── experiment1.sh
    |   └── .env_example
    ├── dataToSend
    │   └── sexuality_sex_gender_hate.json
    ├── dataToSendCSV
    │   └── 01-18-2025
    │       ├── disability_hate.csv
    │       └── misogyny_hate.csv
    ├── bot1.js
    ├── bot2.js
    ├── data.py
    ├── dataSendCurrNum.json
    ├── example.json
    ├── lastSent.json

### Important Directories 
`/bashscript` contains the a bash script file which runs all the required files for the experiment and extracts the environment variables from your environment variables file. `.env_example` is provided to ensure variable names for bot 1 and bot 2 client IDs etc. are matching. Please provide your own twitch application tokens and refresh tokens for correct authentication. How to extract tokens? See here. 

`/dataToSendCSV` directory stores the CSV files of messages that will be sent to the target channel. Note that the messages must be under column name 'text' for the experiment to run without error. The file structure tree above demonstrates a folder with the date of experiment run containing the day's files to run. Please make sure that the name of the folder containing these files follows the structure: `/MM-DD-YYYY`. This allows you to find the corresponding file in the results directory. 

`/results` will be populated with two csv files per csv file in your day's `/dataToSendCSV` directory. This will include a yourCSVFileName+notMod+ segmentNumber.csv containing all messages not flagged as hateful content. This file will store the user that sent that message under 'user', the message itself 'message' and relevant timestamps. yourCSVFileName + segmentNumber.csv stores all messages flagged as hateful content. The column names are as so: `msg_sent, fragments, content_category, category_level, problematic_positions, sent_at, received_at`. To view these values in the original Twitch POST request, please see `example.json`. Examples of the two types of CSV result files are provided in the `/results/01-15-2025` directory. 

### Experiment Files
`data.py` firstly converts the CSVs in `/dataToSendCSV` into JSON files and loads them into `/dataToSend`. Once the experiment setup is complete, `data.py` lets you know. 

`bot1.js` runs the message injection code which simulates a user sending a message in your target channel's chat. 

`bot2.js` and `pubsub.py` acts as recievers listening to the messages sent from bot 1 and filters them by moderated or not. For every moderated message, `pubsub.py` processes the moderation event triggered and extracts the relevant information from POST requests as seen as `example.json`. 

`lastSent.json` stores the last message that we successfully sent to the target channel's chat in order to resume progress when an experiment is unexpectedly terminated.

`dataSendCurrNum.json` stores the currently accessed data file from our `/dataToSend` directory in order to identify where in our day's set of data we should resume progress. 

## 2. Setting up Bots and Token Extraction
To quickly and reliably establish authenticated user access to send and receive messages for our bots, we must first create Twtich registered applications which can be accessed via a Twitch Account's Developer Portal. 

Once an 'Other' application with redirect url as `https://localhost:3000` has been created, make sure to save the client id and secret and upload them to the respective variables in your environment file. 

We will use Twitch's Implicit Flow User Access Tokens method to extract our user access token and refresh tokens so that we do not need to repeat this process. 

First, copy the below url replacing with your respective client ID into a browser. 

    https://id.twitch.tv/oauth2/authorize
    ?response_type=code
    &client_id=<yourClientID>
    &redirect_uri=https://localhost:3000
    &scope=chat%3Aedit+chat%3Aread

    Output: https://localhost:3000/?code=<yourCode>&scope=chat%3Aedit+chat%3Aread

Using the output from above, fill in the respective information for your bot in the following command. Ensure that you have curl. 

    curl -X POST 'https://id.twitch.tv/oauth2/token' \
        -H 'Content-Type: application/x-www-form-urlencoded' \
        -d 'client_id=<yourClientID>&client_secret=<yourClientSecret>&code=<yourCode>&grant_type=authorization_code&redirect_uri=https://localhost:3000'

    Output: {"access_token":"example_token_here","expires_in":13384,"refresh_token":"refresh_token_here","scope":["chat:edit","chat:read"],"token_type":"bearer"}

## 3. Running the experiment
Via bot 2's account credentials, log into the Twitch Creator platform and manipulate the `automod` settings as you like. Please reference the paper to view examples of moderation ranges in the appendix. 

Once you have uploaded your CSV data files into the `/dataToSendCSV/MM-DD-YYYY/` directory ensuring that message plaintexts are under the column name 'text', we can navigate to `/bashScript` to run the following command: `./experiment1.sh`

Running experiments with large datasets, we found that [`tmux`](https://github.com/tmux/tmux/wiki) was helpful in containing separate experiments for prolonged periods of time avoiding disturbances in experiment processing. 

## 4. Results and Analysis of the experiment
    ├── Case_studies
    │   ├── Counterfactual_analysis
    |       ├── Data
    |       ├── Results
    |       └── readme.md 
    |   ├── Policy_adherence_evaluation
    |       ├── Data
    |       ├── Results
    |       └── readme.md    
    |   └── Robustness_analysis
    |       ├── Input
    |       ├── Results
    |       └── readme.md 
    ├── Datasets
    │       ├── DynaHate_Dataset_Creation.py
    │       ├── Dynamically Generated Hate Dataset v0.2.3 (1).csv
    │       ├── IHC.csv
    │       ├── readme.md
    │       ├── SBIC_Dataset_Creation.py
    │       ├── SBIC.v2.trn.csv
    │       ├── toxigen.csv
    │       └── toxigen_Dataset_Creation.py
    ├── Experimental_results
    │   ├── Level1_results_overall_analysis
    │       ├── Context_awareness_experiment
    │       ├── Dynahate
    |       ├── IHC
    |       ├── SBIC
    |       └── ToxiGen
    |   ├── Level2_results_filterwise_analysis
    │       ├── Dynahate
    |       ├── SBIC
    |       └── ToxiGen
    |   └── Level3_results_targetgroupwise_analysis
    │       ├── Dynahate
    |       ├── SBIC
    |       └── ToxiGen
    
