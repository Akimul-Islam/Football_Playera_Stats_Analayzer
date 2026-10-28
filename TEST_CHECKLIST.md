# Test Checklist (Premier League Player Analyzer)

| # | Test | Expected result | Status |
|---|---|---|---|
| 1 | Start the app | Window opens, status bar says `Loaded 20 players. Skipped 0 bad rows.` | PASS |
| 2 | Choose Arsenal, jersey 7 | ID box shows `ARS-07` live | PASS |
| 3 | Create "Leo Marin", Arsenal, 7, MID | Success message, player in the table | PASS |
| 4 | Create another player with Arsenal + jersey 7 | Error "That jersey number is already used in this team (ID ARS-07)" | PASS |
| 5 | Same name in the same team, different jersey | Error "This player already exists in this team" | PASS |
| 6 | Empty name / name with digits | Error, no crash | PASS |
| 7 | Jersey `abc`, `0`, `100` | Error each time | PASS |
| 8 | No team or no position chosen | Error message | PASS |
| 9 | Match Day: add stats for `ARS-07` | Saved, info label shows 1 appearance | PASS |
| 10 | Goals `-1`, `abc`, `50` | Error each time | PASS |
| 11 | Match Day with no player selected | Error message | PASS |
| 12 | Add 38 match days to one player, then a 39th | Error "This player already has 38 appearances" | PASS |
| 13 | Leaderboard FWD | Ranked by score; the new player (under 3 apps) is not listed | PASS |
| 14 | Leaderboard GK / DEF / MID | Only that position | PASS |
| 15 | Check one forward's score by hand (`ARS-09`, Marco Silvano) | `193.8` matches the app | PASS |
| 16 | Search `arsenal` (lowercase) | Only Arsenal players | PASS |
| 17 | Search nonsense | "No players found" | PASS |
| 18 | Delete the created player | Confirmation popup, then removed | PASS |
| 19 | Close and reopen the app | Created players and added stats are still there (persistence) | PASS |
| 20 | Rename `players.csv`, start the app | App opens with zero players, no crash | PASS |
| 21 | Load `players_bad.csv` / `players_empty.csv` | Bad rows skipped; empty file OK; no crash | PASS |
