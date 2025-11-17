import os
from fuzzywuzzy import process

database = {}
with open('database.txt', 'r', encoding='utf-8') as f:
    for line in f:
        id, name = line.strip().split(' = ')
        database[id] = name

region = input("Enter your region (E/P/J/W): ").upper()

root_folder = input("Enter the directory path: ")

if not os.path.exists(root_folder):
    print("Directory not found!")
    exit()

for folder in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, folder)
    if os.path.isdir(folder_path):
        matches = process.extract(folder, database.values(), limit=1)
        if matches:
            best_match_name = matches[0][0]
            matching_ids = [id for id, name in database.items() if name == best_match_name]
            
            selected_id = None
            for id in matching_ids:
                if id.endswith(region):
                    selected_id = id
                    break
            
            if not selected_id and matching_ids:
                selected_id = matching_ids[0]
            
            if selected_id:
                new_name = f"{best_match_name} [{selected_id}]"
                os.rename(folder_path, os.path.join(root_folder, new_name))
                print(f"Renamed folder {folder} to {new_name}")
