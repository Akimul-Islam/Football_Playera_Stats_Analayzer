# analysis.py - NumPy projection, weighted score, leaderboard, and summary calculations

import numpy as np
from models import STAT_FIELDS, WEIGHTS, MIN_APPEARANCES, TOTAL_MATCHDAYS


# Convert a player's season stats into a NumPy float array in the order of STAT_FIELDS
def get_stat_array(player):
    return np.array([player.stats[field] for field in STAT_FIELDS], dtype=float)


# Convert a position's stat weights into a NumPy float array in the order of STAT_FIELDS
def get_weight_array(position):
    weights = WEIGHTS[position]
    return np.array([weights.get(field, 0) for field in STAT_FIELDS], dtype=float)


# Project a player's cumulative stats to a full 38-match season using NumPy
def project_stats(player):
    if player.appearances == 0:
        return {field: 0.0 for field in STAT_FIELDS}
    projected = get_stat_array(player) / player.appearances * TOTAL_MATCHDAYS
    return {field: round(float(value), 1) for field, value in zip(STAT_FIELDS, projected)}


# Calculate a player's position-weighted projected season score using np.dot
def calculate_score(player):
    if player.appearances == 0:
        return 0.0
    projected = get_stat_array(player) / player.appearances * TOTAL_MATCHDAYS
    score = np.dot(projected, get_weight_array(player.position))
    return round(float(score), 1)


# Build the ranked leaderboard list of dictionaries for one position
def build_leaderboard(players, position):
    rows = []
    for player in players:
        if player.position != position or player.appearances < MIN_APPEARANCES:
            continue
        projected = project_stats(player)
        projected_parts = []
        for field in WEIGHTS[position]:
            projected_parts.append(f"{field}={projected[field]}")
        projected_text = ", ".join(projected_parts)
        row = {
            "rank": 0,
            "player_id": player.player_id,
            "name": player.name,
            "team": player.team,
            "appearances": player.appearances,
            "projected": projected_text,
            "score": calculate_score(player),
        }
        rows.append(row)

    rows.sort(key=lambda row: -row["score"])
    for index, row in enumerate(rows, start=1):
        row["rank"] = index
    return rows


# Calculate count, average, highest, and lowest score from leaderboard rows using NumPy
def summarize_scores(rows):
    if len(rows) == 0:
        return {"count": 0, "average": 0.0, "highest": 0.0, "lowest": 0.0}
    scores = np.array([row["score"] for row in rows], dtype=float)
    return {
        "count": len(rows),
        "average": round(float(np.mean(scores)), 1),
        "highest": round(float(np.max(scores)), 1),
        "lowest": round(float(np.min(scores)), 1),
    }


if __name__ == "__main__":
    from models import Player
    sample = Player("ARS-09", "Marco Silvano", "Arsenal", 9, "FWD", 10,
                    {"goals": 8, "assists": 3, "clean_sheets": 0, "saves": 0,
                     "tackles": 2, "yellow_cards": 1, "red_cards": 0})
    print("Projected:", project_stats(sample))
    print("Worked example score (expected 193.8):", calculate_score(sample))
