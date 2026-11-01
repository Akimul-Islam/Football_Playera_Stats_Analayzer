

POSITIONS = ("GK", "DEF", "MID", "FWD")                                    
STAT_FIELDS = ("goals", "assists", "clean_sheets", "saves", "tackles",
               "yellow_cards", "red_cards")                                
PLAYER_FIELDS = ("player_id", "name", "team", "jersey", "position",
                 "appearances") + STAT_FIELDS                              
TOTAL_MATCHDAYS = 38
MIN_APPEARANCES = 3
MAX_JERSEY = 99


TEAM_CODES = {"Arsenal": "ARS", "Chelsea": "CHE", "Liverpool": "LIV",
              "Manchester City": "MCI", "Manchester United": "MUN",
              "Tottenham Hotspur": "TOT", "Newcastle United": "NEW",
              "Aston Villa": "AVL", "Brighton": "BHA", "West Ham United": "WHU"}


MAX_PER_MATCHDAY = {"goals": 10, "assists": 10, "clean_sheets": 1, "saves": 20,
                    "tackles": 20, "yellow_cards": 2, "red_cards": 1}


WEIGHTS = {
    "FWD": {"goals": 5, "assists": 4, "yellow_cards": -1, "red_cards": -3},
    "MID": {"goals": 4, "assists": 5, "tackles": 2, "yellow_cards": -1, "red_cards": -3},
    "DEF": {"goals": 4, "assists": 3, "clean_sheets": 5, "tackles": 4,
            "yellow_cards": -1, "red_cards": -3},
    "GK":  {"clean_sheets": 5, "saves": 1, "yellow_cards": -1, "red_cards": -3},
}


class Player:

    def __init__(self, player_id, name, team, jersey, position, appearances=0, stats=None):
        self.player_id = player_id
        self.name = name
        self.team = team
        self.jersey = jersey              
        self.position = position          
        self.appearances = appearances    
        if stats is None:                 
            stats = {field: 0 for field in STAT_FIELDS}
        self.stats = stats

    def add_matchday(self, new_stats):
        """Add one match day: new_stats is a dict {stat: int}. Updates the totals."""
        for field in STAT_FIELDS:
            self.stats[field] += new_stats[field]
        self.appearances += 1

    def to_dict(self):
        """Return a flat dictionary with the keys in PLAYER_FIELDS."""
        data = {"player_id": self.player_id, "name": self.name, "team": self.team,
                "jersey": self.jersey, "position": self.position,
                "appearances": self.appearances}
        data.update(self.stats)
        return data

    @staticmethod
    def from_dict(data):
        """Build a Player from a CSV row dictionary.
        Raises KeyError if a column is missing, ValueError if a number or value is invalid."""
        player_id = data["player_id"].strip()
        name = data["name"].strip()
        team = data["team"].strip()
        position = data["position"].strip()
        jersey = int(data["jersey"])
        appearances = int(data["appearances"])

        if not player_id or not name:
            raise ValueError("Missing player_id or name in CSV row")
        if team not in TEAM_CODES:
            raise ValueError("Unknown team in CSV row")
        if position not in POSITIONS:
            raise ValueError("Invalid position in CSV row")
        if jersey < 1 or jersey > MAX_JERSEY:
            raise ValueError("Invalid jersey number in CSV row")
        if appearances < 0 or appearances > TOTAL_MATCHDAYS:
            raise ValueError("Invalid appearances count in CSV row")

        stats = {}
        for field in STAT_FIELDS:
            value = int(data[field])
            if value < 0:
                raise ValueError("Negative stat in CSV row")
            stats[field] = value

        return Player(player_id, name, team, jersey, position, appearances, stats)

