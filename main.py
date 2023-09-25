from app.generate_game_v1 import *
from app.prepare_data import read_data, preprocess_data
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


def generate_game(start_action, game_duration, game_style) :

    # Reading the file paths from environment variable
    files_path = os.getenv("FILES_PATH")
    if files_path:
        files = files_path.split(",")  
    else:
        files = [] 

    # Reading data
    combined_data = read_data(files)

    # Preprocessing data
    df = preprocess_data(combined_data)

    # Creating a Game object
    game = GameGenerator(combined_data, df)
    game_sequence = game.generate_game(start_action, game_duration, game_style)
    return game_sequence
