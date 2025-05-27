from datetime import datetime
import os
import time
import csv
import json
import copy
import pandas as pd
currTime = datetime.now()

folderName = currTime.strftime('%m-%d-%Y')
print(folderName)
currentDir = os.getcwd()

dataToSendCSV = currentDir + '/dataToSendCSV'
results = currentDir + '/results'

# Check to see if there is a new folder for the current date in the dataToSendCSV folder. if so, convert the csv files to a json file with the text header column as the data

def make_json(csvFilePath):
    data = {}
    fileName = csvFilePath.split('.')[0].split(currentDir)[1].split('/')[-1]
    headers = []
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        data = [row for row in csvReader]

    with open(currentDir+'/dataToSend/'+fileName+'.json', 'w+') as jsonf:
        json.dump(data, jsonf)

def setupDataToSendFiles():
    # Removing the already tested messages and cutting the json files
    path = os.path.join(os.getcwd(), 'lastSent.json')
    if os.path.exists(path):
        #cut json to the next
        with open(os.path.join(os.getcwd(), 'lastSent.json')) as f:
            lastSentMsg = json.loads(f.read())

        dataSenddir = os.path.join(os.getcwd(), 'dataToSend')
        for dataSendjson in os.listdir(dataSenddir):
            filename = os.fsdecode(dataSendjson)

            if str(lastSentMsg[0]['dataToSendFile']) in filename:
                dataPath = os.path.join(dataSenddir, filename)
                with open(dataPath, 'r+') as f_og:
                    data = json.load(f_og)
                    cutJson = []
                    f_index = 1000000000000000000000000
                    for index, each in enumerate(data):
                        if each['text'] == lastSentMsg[0]['msg']:
                            f_index = index
                        else:
                            if index > f_index:
                                cutJson.append(each)
                    f_og.seek(0)
                    f_og.write(json.dumps(cutJson, ensure_ascii=False))
                    f_og.truncate()


    currDateDataToSend = ''

    listofFilesinDTS = os.listdir(dataToSendCSV)
    for each in listofFilesinDTS: 
        if os.path.isdir(dataToSendCSV+'/'+each): 
            if each == folderName:
                currDateDataToSend = dataToSendCSV + "/" + each

    if currDateDataToSend == '': 
        time.sleep(60)
        setupDataToSendFiles()
    else: 
        # count = 0
        if len(os.listdir(os.path.join(currentDir, 'dataToSend'))) == 0:
            for index, each in enumerate(os.listdir(currDateDataToSend)):
                if index == 0:
                    with open(os.path.join(currentDir, "dataSendCurrNum.json"), 'r+') as f_og:
                        f_og.write(json.dumps([{"current_json":each.split('.')[0] + '.json',"fileNum":1}], ensure_ascii=False))
                make_json(currDateDataToSend+'/'+each)
        return
        
setupDataToSendFiles()
print("Experimental Setup Complete. Data Ready to parse.")
