import time
import json
import pandas as pd
from steam import Steam
from decouple import config

# Get the Steam Web API key
KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

# Load the JSON file
with open('data/interim/user_games.json', 'r') as file:
    data = json.load(file)

# Extract the necessary information from the data (for 200 users)
game_ids = []
playtime = []
game_names = []
owners = []
# count = 0

try:
    # Loop through the data for the first x users
    for user in data:
        # if count >= 3:
                # break
        
        for game in data[user]:
            game_id = game['game_id']

            # Get game ID information
            game_info = steam.apps.get_app_details(game_id)
            game_info_dict = json.loads(game_info)

            # Check if the request for the game has been successful for the given game ID
            success = game_info_dict[str(game_id)]['success']
            if success == False:
                print("Game ID:", game_id, "unsuccessful")

            # If it is, append the game name to the array
            else:
                game_name = game_info_dict[str(game_id)]['data']['name']
                print("Owner:",user, "Game ID:", game_id, "Game name:", game_name)
                owners.append(user)
                game_ids.append(game_id)
                playtime.append(game['playtime'] / 60)
                game_names.append(game_name)

            # Delay for 1 second between API calls
            time.sleep(1)

        # Increment the count
        # count += 1

except Exception as e:
    # Handle the exception and print an error message
    print("An error occurred:", str(e))

# Create a DataFrame from the data
df = pd.DataFrame({'Owner':owners, 'Game ID': game_ids, 'Game name:': game_names, 'Hours Played': playtime})

# Sort the data based on 'Hours Played'
df.sort_values(by='Hours Played', ascending=False, inplace=True)

# Save the DataFrame as a CSV file
df.to_csv('data/interim/games_playtimes.csv', index=False)
