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

---

## 3. Project Folder Structure

```text
premier_league_player_analyzer/
|-- main.py                Starts the program, builds the window and 3 tabs
|-- models.py              Constants (tuples, dicts) + Player class
|-- manager.py             PlayerManager class
|-- gui_players.py         Players tab (create, view, search, delete)
|-- file_handler.py        Load and save CSV files
|-- validation.py          Input checking functions
|-- analysis.py            NumPy 38-match projection, weighted score, summary
|-- gui_matchday.py        Match Day tab (add match-day stats)
|-- gui_leaderboard.py     Leaderboard tab (rank by position)
|-- README.md              Project instructions and overview
|-- TEST_CHECKLIST.md      21-case manual verification checklist
|-- data/
|   |-- players.csv        20 fictional sample players (5 teams x 4 positions)

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
