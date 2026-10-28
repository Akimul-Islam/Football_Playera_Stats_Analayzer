# test_basic.py - basic automated tests for validation, file handling, analysis, and manager

import os
from models import Player, POSITIONS, TEAM_CODES
import validation
import file_handler
import analysis
from manager import PlayerManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Run automated checks on every non-GUI module
def run_tests():
    # 1. Validation tests
    assert validation.validate_name("  Leo Marin ") == "Leo Marin"
    assert validation.validate_jersey("7") == 7
    assert validation.validate_choice("FWD", POSITIONS, "position") == "FWD"
    assert validation.validate_choice("Arsenal", TEAM_CODES, "team") == "Arsenal"
    assert validation.validate_stat("2", "goals") == 2

    # Check invalid inputs raise ValueError
    for bad_name in ("", "   ", "Leo123", "---", "A" * 35):
        try:
            validation.validate_name(bad_name)
            assert False, f"Should have failed for name: {bad_name}"
        except ValueError:
            pass

    for bad_jersey in ("abc", "0", "100", "-5"):
        try:
            validation.validate_jersey(bad_jersey)
            assert False, f"Should have failed for jersey: {bad_jersey}"
        except ValueError:
            pass

    for bad_goals in ("-1", "abc", "50"):
        try:
            validation.validate_stat(bad_goals, "goals")
            assert False, f"Should have failed for goals: {bad_goals}"
        except ValueError:
            pass

    # 2. Analysis worked example test (Section 4.4 of the plan)
    silvano = Player(
        "ARS-09", "Marco Silvano", "Arsenal", 9, "FWD", 10,
        {"goals": 8, "assists": 3, "clean_sheets": 0, "saves": 0,
         "tackles": 2, "yellow_cards": 1, "red_cards": 0}
    )
    projected = analysis.project_stats(silvano)
    assert projected["goals"] == 30.4
    assert projected["assists"] == 11.4
    assert projected["yellow_cards"] == 3.8
    assert analysis.calculate_score(silvano) == 193.8

    # 3. File handler tests (real CSV, bad CSV, empty CSV, missing CSV)
    real_csv = os.path.join(BASE_DIR, "data", "players.csv")
    bad_csv = os.path.join(BASE_DIR, "data", "test", "players_bad.csv")
    empty_csv = os.path.join(BASE_DIR, "data", "test", "players_empty.csv")
    missing_csv = os.path.join(BASE_DIR, "data", "test", "does_not_exist.csv")

    players, skipped = file_handler.load_players(real_csv)
    assert len(players) == 20 and skipped == 0

    bad_players, bad_skipped = file_handler.load_players(bad_csv)
    assert len(bad_players) == 5 and bad_skipped == 3

    empty_players, empty_skipped = file_handler.load_players(empty_csv)
    assert len(empty_players) == 0 and empty_skipped == 0

    missing_players, missing_skipped = file_handler.load_players(missing_csv)
    assert len(missing_players) == 0 and missing_skipped == 0

    # 4. PlayerManager end-to-end workflow on a temporary file
    temp_csv = os.path.join(BASE_DIR, "data", "test", "temp_test_players.csv")
    if os.path.exists(temp_csv):
        os.remove(temp_csv)

    mgr = PlayerManager(real_csv)
    msg = mgr.load_all()
    assert msg == "Loaded 20 players. Skipped 0 bad rows."
    mgr.players_file = temp_csv

    assert mgr.preview_player_id("Arsenal", "7") == "ARS-07"
    assert mgr.preview_player_id("Arsenal", "0") == ""
    assert mgr.preview_player_id("Arsenal", "100") == ""
    assert mgr.preview_player_id("", "7") == ""

    created = mgr.create_player("Leo Marin", "Arsenal", "7", "MID")
    assert created.player_id == "ARS-07"
    assert len(mgr.get_all_players()) == 21

    # Add 1 match day and check persistence
    stats_entry = {
        "goals": "1", "assists": "2", "clean_sheets": "0",
        "saves": "0", "tackles": "4", "yellow_cards": "0", "red_cards": "0"
    }
    mgr.add_matchday_stats("ARS-07", stats_entry)
    assert mgr.find_player("ARS-07").appearances == 1

    # Delete and verify removal from sets
    mgr.delete_player("ARS-07")
    assert len(mgr.get_all_players()) == 20
    assert "ARS-07" not in mgr.player_ids

    if os.path.exists(temp_csv):
        os.remove(temp_csv)

    print("All automated tests passed!")


if __name__ == "__main__":
    run_tests()
