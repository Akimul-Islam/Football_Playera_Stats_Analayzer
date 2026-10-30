# manager.py - PlayerManager class that connects the GUI, files, validation, and analysis

import file_handler
import analysis
import validation
from models import Player, STAT_FIELDS, POSITIONS, TEAM_CODES


class PlayerManager:
    """Manages the list of players, duplicate sets, CSV saving/loading, and leaderboard queries."""

    # Set up the manager with the CSV file path, an empty player list, and duplicate-check sets
    def __init__(self, players_file):
        self.players_file = players_file
        self.players = []
        self.player_ids = set()
        self.name_keys = set()

    # Load all players from CSV and skip rows with duplicate IDs, mismatched IDs, or duplicate names
    def load_all(self):
        loaded_players, skipped = file_handler.load_players(self.players_file)
        self.players = []
        self.player_ids = set()
        self.name_keys = set()

        for player in loaded_players:
            expected_id = self.make_player_id(player.team, player.jersey)
            name_key = (player.name.lower(), player.team)
            if (player.player_id != expected_id or
                    player.player_id in self.player_ids or
                    name_key in self.name_keys):
                skipped += 1
            else:
                self.players.append(player)
                self.player_ids.add(player.player_id)
                self.name_keys.add(name_key)

        return f"Loaded {len(self.players)} players. Skipped {skipped} bad rows."

    # Save all current players back to the CSV file
    def save_all(self):
        return file_handler.save_players(self.players_file, self.players)

    # Build a player ID from the team's 3-letter code and a 2-digit jersey number
    def make_player_id(self, team, jersey):
        return f"{TEAM_CODES[team]}-{jersey:02d}"

    # Return a live preview of the player ID for the GUI, or empty string if inputs are incomplete
    def preview_player_id(self, team, jersey_text):
        if team not in TEAM_CODES:
            return ""
        try:
            jersey = validation.validate_jersey(jersey_text)
            return self.make_player_id(team, jersey)
        except ValueError:
            return ""

    # Validate inputs, create a new Player, add to list and sets, and save to CSV
    def create_player(self, name, team, jersey_text, position):
        name = validation.validate_name(name)
        team = validation.validate_choice(team, TEAM_CODES, "team")
        jersey = validation.validate_jersey(jersey_text)
        position = validation.validate_choice(position, POSITIONS, "position")
        player_id = self.make_player_id(team, jersey)
        validation.validate_no_duplicate(player_id, name, team, self.player_ids, self.name_keys)

        new_player = Player(player_id, name, team, jersey, position)
        self.players.append(new_player)
        self.player_ids.add(player_id)
        self.name_keys.add((name.lower(), team))
        self.save_all()
        return new_player

    # Find and return the Player with the given player_id, or None if not found
    def find_player(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None

    # Delete a player by ID from the list and sets, then save to CSV
    def delete_player(self, player_id):
        player_id = validation.validate_existing_player_id(player_id, self.player_ids)
        player = self.find_player(player_id)
        if player is not None:
            self.players.remove(player)
            self.name_keys.discard((player.name.lower(), player.team))
        self.player_ids.discard(player_id)
        self.save_all()

    # Search players by keyword (ID, name, or team) and optional position filter
    def search_players(self, keyword, position="All"):
        kw = keyword.strip().lower()
        results = []
        for player in self.players:
            if position != "All" and player.position != position:
                continue
            if (kw == "" or
                    kw in player.player_id.lower() or
                    kw in player.name.lower() or
                    kw in player.team.lower()):
                results.append(player)
        return results

    # Validate and add one match day's stats to a player, then save to CSV
    def add_matchday_stats(self, player_id, stat_texts):
        player_id = validation.validate_existing_player_id(player_id, self.player_ids)
        player = self.find_player(player_id)
        validation.validate_appearance_limit(player.appearances)
        new_stats = {}
        for field in STAT_FIELDS:
            new_stats[field] = validation.validate_stat(stat_texts[field], field)
        player.add_matchday(new_stats)
        self.save_all()
        return player

    # Return the full list of Player objects
    def get_all_players(self):
        return self.players

    # Return a sorted list of allowed team names
    def get_team_names(self):
        return sorted(TEAM_CODES)

    # Return a sorted list of "ID | Name" strings for the Match Day dropdown
    def get_player_labels(self):
        labels = [f"{p.player_id} | {p.name}" for p in self.players]
        return sorted(labels)

    # Return the ranked leaderboard rows for the chosen position
    def get_leaderboard(self, position):
        return analysis.build_leaderboard(self.players, position)
