# main.py - starts the Premier League Player Analyzer application and builds the main window

import os
import tkinter as tk
from tkinter import ttk, messagebox
from manager import PlayerManager
from gui_players import PlayersTab
from gui_matchday import MatchDayTab
from gui_leaderboard import LeaderboardTab

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Create the manager, build the Tkinter window and 3 tabs, and start the event loop
def main():
    manager = PlayerManager(os.path.join(BASE_DIR, "data", "players.csv"))
    message = manager.load_all()

    root = tk.Tk()
    root.title("Premier League Player Analyzer")
    root.geometry("1050x650")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)
    status_var = tk.StringVar(value=message)
    ttk.Label(root, textvariable=status_var).pack(fill="x")

    tabs = []                                  # list of all tabs

    # Refresh all three tabs whenever player data changes
    def refresh_all():
        for tab in tabs:
            tab.refresh()

    tabs.append(PlayersTab(notebook, manager, refresh_all))
    tabs.append(MatchDayTab(notebook, manager, refresh_all))
    tabs.append(LeaderboardTab(notebook, manager, refresh_all))
    for tab, title in zip(tabs, ("Players", "Match Day", "Leaderboard")):
        notebook.add(tab, text=title)

    # Save all player records immediately when clicking File -> Save
    def save_now():
        if manager.save_all():
            status_var.set("Saved successfully.")
        else:
            messagebox.showerror("Save failed", "Could not save the file.")

    menu = tk.Menu(root)
    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label="Save", command=save_now)
    file_menu.add_command(label="Exit", command=root.destroy)
    menu.add_cascade(label="File", menu=file_menu)
    root.config(menu=menu)

    refresh_all()
    root.mainloop()


if __name__ == "__main__":
    main()
