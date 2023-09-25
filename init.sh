#!/bin/bash

# ./init.sh pass 9 neutral

pip install -r requirements.txt

# Assigning command line arguments to variables
start_action=$1
game_duration=$2
game_style=$3

# Running the FastAPI application
uvicorn app.api:app --reload &

# Giving the server some time to start
sleep 5

# Determine the operating system and open the URL in the default web browser
case "$(uname -s)" in
   Darwin)
     open "http://127.0.0.1:8000/docs#/default/recreate_game_generate_game_get" ;;
   Linux)
     xdg-open "http://127.0.0.1:8000/docs#/default/recreate_game_generate_game_get" ;;
   CYGWIN*|MINGW32*|MSYS*|MINGW*)
     start "http://127.0.0.1:8000/docs#/default/recreate_game_generate_game_get" ;;
   *)
     echo 'Your OS is not supported for opening URLs from a shell script.' ;;
esac

# Making a GET request to the FastAPI server
curl -G http://127.0.0.1:8000/generate_game \
     --data-urlencode "start_action=$start_action" \
     --data-urlencode "game_duration=$game_duration" \
     --data-urlencode "game_style=$game_style" \
     -o game.json

