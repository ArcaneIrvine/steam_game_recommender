# import dependencies
import json
import time
import pandas as pd
from steam import Steam
from decouple import config

# Get the Steam Web API key
KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

# Load the JSON file
with open('data/interim/user_games.json', 'r') as file:
    user_games = json.load(file)

# Dictionary to store filtered data
filtered_games = {}

for user, games in user_games.items():
    filtered_playtimes = []
    for game in games:

        # Access the "game_id" and "playtime" within the item dictionary
        game_id = game["game_id"]
        time_played = game["playtime"]
        
        if time_played >= 60:
            print(f"User: {user}, game id: {game_id}, playtime: {time_played}")
            filtered_playtimes.append({"game_id": game_id, "playtime": time_played})
        else:
            print("-")
    
    # Add user data if there are filtered playtimes
    if filtered_playtimes:
        filtered_games[user] = filtered_playtimes

# Save filtered data to a JSON file
with open('data/interim/user_games_filtered.json', 'w') as file:
    json.dump(filtered_games, file)