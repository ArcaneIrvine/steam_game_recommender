# import dependencies
import json
import time
import pandas as pd
from steam import Steam
from decouple import config

# Get the Steam Web API key
KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

# Load dataset
IDs = pd.read_csv('data/raw/steam_ids.csv')

# Dictionary to track user-game ownership
user_games = {}

# Iterate over each user ID
for id in IDs['Steam_ID']:
    user_games[id] = []  # Initialize an empty list for each user ID
    
    # Get the list of games owned by the user
    owned_games = steam.users.get_owned_games(id)
    
    # Iterate over each game in the owned games list
    for game in owned_games['games']:
        game_id = game['appid']
        playtime = game['playtime_forever']
        user_games[id].append({'game_id': game_id, 'playtime': playtime})  # Add game ID and playtime to the user's list of owned games
        
    time.sleep(1)  # Delay for 1 second between API calls

"""
# Print the user-game ownership
for id, games in user_games.items():
    print(f"User {id} owns: {games}")
"""

# Export the user-game ownership to a JSON file
with open('data/interim/user_games.json', 'w') as file:
    json.dump(user_games, file)