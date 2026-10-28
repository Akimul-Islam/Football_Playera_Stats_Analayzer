# Premier League Player Analyzer

**CSC 4162 Mid-Term Project | Fall 2026-27**

A desktop Python application built with **Tkinter**, **NumPy**, and **CSV file handling** that stores fictional Premier League player records, records match-day statistics, projects player numbers to a full 38-match season, and ranks players by position using weighted scores.

---

## 1. Requirements

- **Python 3.10+** (Tkinter is included with standard Python installations)
- **NumPy** (`pip install numpy`)

---

## 2. How to Run the Project

1. Open a terminal inside the `premier_league_player_analyzer` folder.
2. Install NumPy if it is not installed yet:
   ```bash
   pip install numpy
   ```
3. Start the desktop application:
   ```bash
   python main.py
   ```
4. *(Optional)* Run the basic automated test script:
   ```bash
   python test_basic.py
   ```

---

## 3. Project Folder Structure

```text
premier_league_player_analyzer/
|-- main.py              (Member 1)  Starts the program, builds the window and 3 tabs
|-- models.py            (Member 1)  Constants (tuples, dicts) + Player class
|-- manager.py           (Member 1)  PlayerManager class
|-- gui_players.py       (Member 1)  Players tab (create, view, search, delete)
|-- file_handler.py      (Member 2)  Load and save CSV files
|-- validation.py        (Member 2)  Input checking functions
|-- analysis.py          (Member 2)  NumPy 38-match projection, weighted score, summary
|-- gui_matchday.py      (Member 2)  Match Day tab (add match-day stats)
|-- gui_leaderboard.py   (Member 2)  Leaderboard tab (rank by position)
|-- test_basic.py        (Member 4)  Automated checks for validation, files, and NumPy math
|-- README.md            (Member 4)  Project instructions and overview
|-- TEST_CHECKLIST.md    (Member 3)  21-case manual verification checklist
|-- data/
|   |-- players.csv      (Member 3)  20 fictional sample players (5 teams x 4 positions)
|   |-- test/
|       |-- players_bad.csv    (Member 3)  CSV with corrupted rows for error-handling demo
|       |-- players_empty.csv  (Member 3)  Empty CSV file test
|-- screenshots/         (Member 4)  Folder for demo screenshots
|-- report/
    |-- report.md        (Member 5)  Complete 10-section mid-term project report
```

---

## 4. Main Features (7 Operations)

1. **Create Player:** Auto-generates `player_id` (`TEAM-JERSEY`, e.g., `ARS-07`) live as you pick a team and jersey number, preventing duplicate IDs and duplicate player names in the same team.
2. **View Players:** Displays all players with their team, jersey, position, and season appearances in a scrollable table.
3. **Search & Filter Players:** Searches by ID, name, or team keyword (case-insensitive) and filters by position (`All`, `GK`, `DEF`, `MID`, `FWD`).
4. **Delete Player:** Deletes the selected player after a confirmation dialog and updates all tabs and the CSV file.
5. **Add Match-Day Stats:** Adds one appearance and updates cumulative season stats (`goals`, `assists`, `clean_sheets`, `saves`, `tackles`, `yellow_cards`, `red_cards`) up to 38 appearances.
6. **Position Leaderboard with 38-Match Projection:** Projects stats to 38 matches (`stat / appearances * 38`) and ranks players with at least 3 appearances using position-specific weights and `numpy.dot`.
7. **Automatic CSV Save & Load:** Loads `data/players.csv` at startup, skips bad rows safely, and auto-saves after every change.
