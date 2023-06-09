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

print(user_games)
