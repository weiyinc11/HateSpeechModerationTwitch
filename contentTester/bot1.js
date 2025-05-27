const { exec } = require('child_process');
const tmi = require('tmi.js');
const fs = require('fs');
const path = require("path");
const os = require('os');
var process = require('process');

var access_token = '';
var refresh_token = process.env.b1_REFRESH_TOKEN; 
var expires_in = 0;
const client_id = process.env.b1_CLIENT_ID;
const client_secret = process.env.b1_CLIENT_SECRET;

// Function called when the "dice" command is issued
function rollDice () {
    const sides = 6;
    return Math.floor(Math.random() * sides) + 1;
  }
  
  // Called every time the bot connects to Twitch chat
  function onConnectedHandler (addr, port) {
    console.log(`* Connected to ${addr}:${port}`);
  }


  async function getData() {
    const directory = path.join(__dirname, '/dataToSend')
    const moveTo = path.join(__dirname, '/results')
    let dataSection = [];
    
    try {
        const files = await fs.promises.readdir(directory);

        const filenames = files.filter(file => {
            const filePath = path.join(directory, file);
            return fs.statSync(filePath).isFile();
        });
        
        count = 1
        for (const fileName of filenames) {
            console.log(fileName)
            // get the dataSend number so that we don't need to rename the files but instead done_count goes by the starting file number-- this allows the results files to correspond to the csv.
            if (count == 1){
                done_count = 1
                fs.writeFileSync('dataSendCurrNum.json', JSON.stringify([{'current_json': fileName, 'fileNum': done_count}]), {flag: 'w'});
            }
        
            const data = await fs.promises.readFile(path.join(directory, fileName), 'utf8');
            
            const json_data = JSON.parse(data);
            const end = Math.floor(json_data.length + 1);
            const start = 0;

            let file_data = [];
            for (let i = start; i < end; i++) {
                const rare = json_data[i];
                file_data.push(rare);
            }

            dataSection.push(file_data);
            count++; 
        }
    } catch (err) {
        console.error('Error:', err);
    }
    return dataSection;
}
//   returns a list of lists per json file in dataToSend --> each list per file contains half of the job.


function renewToken(callback) {
    exec(`curl -X POST https://id.twitch.tv/oauth2/token \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'grant_type=refresh_token&refresh_token=${refresh_token}&client_id=${client_id}&client_secret=${client_secret}'`, (error, stdout, stderr) => {
        if (error) {
        console.error(`exec error: ${error}`);
        return;
        }
        console.log(`stdout: ${stdout}`);
        // console.error(`stderr: ${stderr}`);

        var resAccess = String(stdout);
        var each = resAccess.split(',');
        // console.log("each: " + each[0]);
        // console.log("split: " + each[0].split(':')[1]);
        refresh_token = each[1].split(':')[1].replace(/"/g, '');
        
        console.log("Access token: " + each[0].split(':')[1].replace(/"/g, ''));
        console.log("Refresh Token: " + each[2].split(':')[1].replace(/"/g, ''));
        console.log("Expires In: " + each[1].split(':')[1].replace(/"/g, ''));

        result = {
            "access_token": each[0].split(':')[1].replace(/"/g, ''),
            "refresh_token" : each[2].split(':')[1].replace(/"/g, ''),
            "expiresIn" : each[1].split(':')[1].replace(/"/g, '')
        };

        callback(result);
    });
}


async function processFileData(fileData, client, target, startIndex) {
    return new Promise((resolve) => {
        let index = startIndex;
        let count = process.env.b1_msg_count; 
        const intervalId = setInterval(() => {
            if (count > 0 && index < fileData.length) {
                try{
                    text = fileData[index].text
                    client.say(target, fileData[index].text);
                    index++;
                    count--;
                } catch {
                    clearInterval(intervalId);
                    resolve(index);
                }
            } else {
                clearInterval(intervalId);
                resolve(index);
            }
        }, process.env.b1_randomWaitMsgTime);
    });
}



async function run(client, target) {
    const data = await getData();

    for (let i = 0; i < data.length; i++) {
        let index = 0;
        while (index < Math.floor(data[i].length)) {
            index = await processFileData(data[i], client, target, index);
            if (index < data[i].length) {
                console.log('Pausing for 10 seconds...');
                await new Promise(resolve => setTimeout(resolve, 3500)); // Pause for 10 seconds
            } else {
                client.say(target, 'done');
            }
        }
    }
}

// -------------------------------------------------------------------------------------------------------------------

function autoRenew(){
    renewToken(function(res) {
        access_token = res.access_token;
        refresh_token = res.refresh_token;
        expires_in = parseInt(res.expiresIn);

        // Define configuration options
        const opts = {
            identity: {
            username: process.env.b1_username,
            password: String(access_token)
            },
            channels: [
                process.env.b1_channel,
            ]
        };
        
        // Create a client with our options
        const client = new tmi.client(opts);
        
        // Register our event handlers (defined below)
        client.on('message', onMessageHandler);
        client.on('connected', onConnectedHandler);
        
        // Connect to Twitch:
        client.connect();
        
        setInterval(() => {
            console.log("Renewing Token...");
            autoRenew();
        }, expires_in * 1000);
        
        // Called every time a message comes in
        function onMessageHandler (target, tags, msg, self) {
            if (self) { 
                return
            } else {
                if (msg.includes("!")){
                    if (msg === '!dice') {
                        const num = rollDice();
                        client.say(target, `You rolled a ${num}`);
                        console.log(`* Executed ${msg} command`);
                    } else if (msg === '!audit') {
                        run(client, target);
                        console.log(`* Executed ${msg} command`);
                    } else {
                        const temp = 0;
                    }
                } else {
                    if (msg === 'Experiment Complete'){
                        client.disconnect();
                        process.exit(0);
                    }
                }
            }
        }
    });
}


autoRenew();
