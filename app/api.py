from fastapi import FastAPI, Query
from main import *

app = FastAPI(
title="Game Generator API",
description="An API to recreate a football game sequence based on pre-recorded data",
version="1.0",
)

@app.get("/generate_game")
def recreate_game(
    start_action: str = Query(..., description="The initial action to start the game sequence."),
    game_duration: int = Query(..., description="The desired total duration for the game sequence in minutes."),
    game_style: str = Query(..., description="The chosen game style affecting the transition probabilities ('attacking', 'defensive', or 'neutral').")
):
    game_sequence = generate_game(start_action, game_duration, game_style)
    return {"game_sequence": game_sequence}

#uvicorn app.api:app --reload