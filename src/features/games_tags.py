import time
import json
import polars as pl
from steam import Steam
from decouple import config

# Get the Steam Web API key
KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

# Load the data
df = pl.read_csv("data/interim/games_playtimes.csv")

seen_ids = set()
category_data = {}

for id in df['Game ID']:
    if id in seen_ids:
        continue

    seen_ids.add(id)
    
    try:
        info = steam.apps.get_app_details(id)
        info_dict = json.loads(info)

        categories = info_dict[str(id)]['data']['categories']
        category_names = [category['description'] for category in categories]

        category_data[str(id)] = category_names

        print(f"Game ID: {id}, Categories: {category_names}")

        # Delay for 1 second between API calls
        time.sleep(1)
    
    except KeyError:
        print(f"No information found for Game ID: {id}")
        continue

# Save the category data to a JSON file
with open('data/interim/games_tags.json', 'w') as file:
    json.dump(category_data, file, indent=4)
