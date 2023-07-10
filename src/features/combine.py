import csv
import json

# Load the CSV file
csv_file = 'data/interim/games_playtimes.csv'

# Load the JSON file
json_file = 'data/interim/games_tags.json'

# Read the JSON data
with open(json_file, 'r') as file:
    game_tags = json.load(file)

# Update the CSV file with game tags
updated_rows = []

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames + ['Game Tags']

    for row in reader:
        game_id = row['Game ID']
        tags = game_tags.get(game_id, [])

        row['Game Tags'] = ', '.join(tags)
        updated_rows.append(row)

# Save the updated CSV file
updated_csv_file = 'data/processed/final.csv'

with open(updated_csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print("CSV file updated with game tags.")