#!/bin/bash
#!/bin/bash node 
#!/bin/bash python3

if [ -f .env ]; then
  set -a
  source .env
  set +a
else
  echo ".env file not found. Please create one based on .env.example."
  exit 1
fi

cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"

cd ..
SCRIPT_DIR_BF="$(pwd)"

PATH_BOT1="$SCRIPT_DIR_BF/bot1.js"
PATH_BOT2="$SCRIPT_DIR_BF/bot2.js"
DATA_BOT="$SCRIPT_DIR_BF/data.py"
PUBSUB_BOT="$SCRIPT_DIR_BF/pubsub.py"

# argsBot1=()
# argsBot2=()
# argsPubSub=()
# count=0
# for arg in "$@"; do
#     for arg_t in $arg; do
#         if [ "$count" -eq 0 ]; then
#             argsBot1+=($arg_t)
#         elif [ "$count" -eq 1 ]; then
#             argsBot2+=($arg_t)
#         else
#             argsPubSub+=($arg_t)
#         fi
#     done 
#     count+=1
# done

# node $PATH_BOT1 ${argsBot1[@]} & node $PATH_BOT2 ${argsBot2[@]} & python3 $DATA_BOT & python $PUBSUB_BOT ${argsPubSub[@]}
node $PATH_BOT1 & node $PATH_BOT2 & python3 $DATA_BOT & python $PUBSUB_BOT