# import dependencies
import requests
import csv
from steam import Steam
from decouple import config
from pprint import pprint

# Get the Steam Web API key
KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

# API link for checking user's profiles
base_url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/'

random_steam_ids = []
steam_id = 76561198327129152 # initial steam_id

# Increment the initial steam_id by 1 for x repetitions
for _ in range(1000):
    # Final URL with the correct key and paramaters for the request
    URL = f'{base_url}?key={KEY}&steamids={steam_id}'
    response = requests.get(URL)

    # Extract the JSON data from the HTTP response
    data = response.json()

    # If there is a User with the given ID
    if 'players' in data['response'] and len(data['response']['players']) > 0:
        player = data['response']['players'][0]
        
        # If communityvisibilitystate and profilestate exist in the user's data
        if 'communityvisibilitystate' in player and 'profilestate' in player:
            community_visibility_state = player['communityvisibilitystate']
            profile_state = player['profilestate']

            # If the user has a profile and the profile is public
            if community_visibility_state == 3 and profile_state == 1:
                user_games = steam.users.get_owned_games(steam_id)
                
                # If the user has more than 1 games
                if 'game_count' in user_games:
                    if user_games['game_count'] >= 1:
                        # add the user id in the array
                        pprint(user_games)
                        random_steam_ids.append(steam_id)
                    else:
                        print("User", steam_id, "has no games")
                else:
                    print("User", steam_id, "has no games")

            else:
                print("communityvisibilitystate is not 3 and profile_state is not 1 for user", steam_id)

        else:
            print("communityvisibilitystate and/or profilestate are not available for user", steam_id)
    else:
        print("No user found for the Steam ID:", steam_id)

    # increment by 1
    steam_id += 1
    
print("Total IDs gathered:", len(random_steam_ids))

# Save the IDs to a CSV file
with open('data/useable_steam_ids.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Steam ID'])  # Write the header row
    writer.writerows([[id] for id in random_steam_ids])