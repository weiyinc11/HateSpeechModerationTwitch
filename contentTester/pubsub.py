import twitchAPI.oauth
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.type import AuthScope
from twitchAPI.oauth import UserAuthenticator
import twitchAPI
import asyncio
from uuid import UUID
from datetime import datetime, timedelta
import os
import json
import csv

print("Client secret: ", os.getenv('CLIENT_SECRET'))
APP_ID = os.getenv("ps_APP_ID")
APP_SECRET = os.getenv("ps_APP_SECRET")
TARGET_CHANNEL = os.getenv("ps_CHANNEL")
TOKEN = os.getenv("ps_TOKEN")
REFRESH_TOKEN = os.getenv("ps_REFRESH_TOKEN")

msg_sent = [datetime.now(), 0]
dataSendDr = os.path.join(os.getcwd(), 'dataToSend')
def getNextfile(done_count):
    files = os.listdir(dataSendDr)
    for file in files: 
        if os.path.isfile(os.path.join(dataSendDr, file)):
            nextFile = file
            break

    if os.path.isfile(os.path.join(os.getcwd(), 'dataSendCurrNum.json')):
        data = [{"current_json":nextFile,"fileNum":done_count}]
        done_count += 1
        with open(os.path.join(os.getcwd(), 'dataSendCurrNum.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return nextFile

def write(fileName, data):
    now = datetime.now()
    folderName = now.strftime("%m-%d-%Y")
    todayResults = os.path.join(os.getcwd(), '/results/'+folderName)

    if not os.path.isdir(todayResults):
        with open(fileName, 'w', newline='\n') as csvfile:
            fieldnames = ['name', 'branch', 'year', 'cgpa']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    else: 
        with open(fileName, 'a') as csvfile:
            csv.write(data)
    print("CSV file written successfully! ")

async def callback_automod(uuid: UUID, data: dict) -> None:
    time = datetime.now()
    t = os.path.join(os.getcwd(), 'dataSendCurrNum.json')
    with open(t, 'r') as file:
        dataf = json.load(file)
        done_count = dataf[0]['fileNum']
        fileNameCurr = dataf[0]['current_json'].split('.')[0]

        now = datetime.now()
        folderName = now.strftime("%m-%d-%Y")
        todayResults = os.path.join(os.getcwd(), 'results/'+folderName)

        try:
            print((not os.path.isdir(todayResults)))
            if not os.path.isdir(todayResults):
                os.mkdir(todayResults)
        except OSError as error:
            print(error) 

    print("File written to: " + fileNameCurr)
    print("File num: " + str(done_count))
    header = ['msg_sent', 'fragments', 'content_category', 'category_level', 'problematic_positions', 'sent_at', 'received_at']
    frag = data['data']['message']['content']['fragments']
    dataJson = [
        {
            'msg_sent': data['data']['message']['content']['text'],
            'fragments': [each for each in frag if len(each) > 1], 
            'content_category': data['data']['content_classification']['category'],
            'category_level': data['data']['content_classification']['level'], 
            'problematic_positions': data['data']['caught_message_reason']['automod_failure']['positions_in_message'],
            'sent_at': data['data']['message']['sent_at'],
            'received_at': time, 
        }
    ]

    try:
        new_csv = os.path.join(todayResults, str(fileNameCurr+'_'+str(done_count)+'.csv'))
        if not os.path.isfile(new_csv):
            with open(new_csv, 'w', encoding='utf-8', newline='') as newcsvfile:
                writer = csv.DictWriter(newcsvfile, fieldnames=header)
                writer.writeheader()
                writer.writerows(dataJson)
                newcsvfile.close()
        else: 
            with open(new_csv, 'a', encoding='utf-8', newline='') as newcsvfile:
                writer = csv.DictWriter(newcsvfile, fieldnames=header)
                writer.writerow(dataJson[0])
                newcsvfile.close()
        print("CSV file written to successfully! ")
    except: 
        print("Error in csv")


    file.close()
    print('got callback for UUID ' + str(uuid))

def checkstatus():
    with open(os.path.join(os.getcwd(), 'dataSendCurrNum.json'), 'r') as checkExp:
        checkdata = json.load(checkExp)
        killExp = checkdata[0]['current_json']
    checkExp.close()

    if killExp == "experiment complete":
        return True

done_count = -1
async def run_example(TOKEN, REFRESH_TOKEN):
    twitch = await Twitch(APP_ID, APP_SECRET)

    # Here is a built-in method of authenticating your pubsub bot with the THEN-correct twitch user scope. Please refer to documentation by Twitch to ensure that your bot is authenticated to proceed. 
    # auth = UserAuthenticator(twitch, [AuthScope.WHISPERS_READ, AuthScope.CHANNEL_MODERATE], force_verify=False)
    # token, refresh_token = await auth.authenticate()
    # print(token, refresh_token)

    # you can get your user auth token and user auth refresh token following the example in twitchAPI.oauth
    await twitch.set_user_authentication(TOKEN, [AuthScope.CHANNEL_MODERATE], REFRESH_TOKEN)
    user = await first(twitch.get_users(logins=[TARGET_CHANNEL]))

    expCont = True
    while expCont:
        startTime = datetime.now()
        while((startTime + timedelta(seconds=30)) > datetime.now()):
            pubsub = PubSub(twitch)
            pubsub.start()
            uuid = await pubsub.listen_automod_queue(user.id, user.id, callback_automod)
            print('listening...')

            input("Press enter to close: ")
            await pubsub.unlisten(uuid)
            pubsub.stop()
            await twitch.close()
            exit()
        TOKEN, REFRESH_TOKEN = await twitchAPI.oauth.refresh_access_token(REFRESH_TOKEN, APP_ID, APP_SECRET, None, 'https://id.twitch.tv/oauth2/')
        await twitch.set_user_authentication(TOKEN, [AuthScope.WHISPERS_READ, AuthScope.CHANNEL_MODERATE], REFRESH_TOKEN)
        user = await first(twitch.get_users(logins=[TARGET_CHANNEL]))
        print("Token refreshed! ")

asyncio.run(run_example(TOKEN, REFRESH_TOKEN)) 