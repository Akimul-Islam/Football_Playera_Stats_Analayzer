# file_handler.py - load and save players to a CSV file

import csv
import os
from models import Player, PLAYER_FIELDS


# Load players from a CSV file and return (list_of_players, skipped_count)
def load_players(filepath):
    players = []
    skipped = 0
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    player = Player.from_dict(row)
                    players.append(player)
                except (KeyError, ValueError, TypeError, AttributeError):
                    skipped += 1
    except (FileNotFoundError, OSError):
        return ([], 0)
    return (players, skipped)


# Save the list of Player objects to a CSV file and return True if successful
def save_players(filepath, players):
    try:
        folder = os.path.dirname(filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=PLAYER_FIELDS)
            writer.writeheader()
            for player in players:
                writer.writerow(player.to_dict())
        return True
    except OSError:
        return False


