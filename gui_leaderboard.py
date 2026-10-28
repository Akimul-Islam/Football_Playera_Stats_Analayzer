# gui_leaderboard.py - Leaderboard tab showing 38-match projections and weighted scores by position

import tkinter as tk
from tkinter import ttk
from models import POSITIONS, WEIGHTS


class LeaderboardTab(ttk.Frame):
    """GUI tab for viewing position-specific leaderboards and NumPy score summaries."""

    # Set up the Leaderboard tab with position selector, Treeview table, and summary labels
    def __init__(self, parent, manager, on_change):
        super().__init__(parent, padding=10)
        self.manager = manager
        self.on_change = on_change

        self.position_var = tk.StringVar(value="FWD")
        self.weights_var = tk.StringVar()
        self.summary_var = tk.StringVar()

        self.build_ui()

    # Build the top position selector, leaderboard table, and bottom information labels
    def build_ui(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(top_frame, text="Position:").pack(side="left", padx=(0, 4))
        pos_combo = ttk.Combobox(
            top_frame, textvariable=self.position_var, values=POSITIONS, state="readonly", width=10
        )
        pos_combo.pack(side="left", padx=4)
        pos_combo.bind("<<ComboboxSelected>>", self.on_show)
        ttk.Button(top_frame, text="Show", command=self.on_show).pack(side="left", padx=4)

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=(0, 8))

        columns = ("rank", "name", "team", "appearances", "projected", "score")
        headings = ("Rank", "Player", "Team", "Apps", "Projected 38-match stats", "Score")
        widths = (60, 160, 150, 60, 420, 90)

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col, title, width in zip(columns, headings, widths):
            self.tree.heading(col, text=title)
            anchor = "w" if col == "projected" else "center"
            self.tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Label(self, textvariable=self.weights_var).pack(fill="x", pady=2)
        ttk.Label(self, textvariable=self.summary_var).pack(fill="x", pady=2)
        ttk.Label(
            self,
            text="Projected to 38 match days. Players need at least 3 appearances to be ranked.",
        ).pack(fill="x", pady=2)

    # Refresh the leaderboard table and labels for the currently chosen position
    def refresh(self):
        position = self.position_var.get()
        if position not in POSITIONS:
            position = "FWD"
            self.position_var.set(position)

        rows = self.manager.get_leaderboard(position)
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    row["rank"],
                    row["name"],
                    row["team"],
                    row["appearances"],
                    row["projected"],
                    row["score"],
                ),
            )

        weight_parts = []
        for field, weight in WEIGHTS[position].items():
            weight_parts.append(f"{field} {weight}")
        self.weights_var.set("Weights: " + ", ".join(weight_parts))

        if len(rows) == 0:
            self.summary_var.set("No ranked players for this position")
        else:
            summary = self.manager.get_score_summary(rows)
            self.summary_var.set(
                f"Players ranked: {summary['count']} | Average score: {summary['average']} | "
                f"Highest: {summary['highest']} | Lowest: {summary['lowest']}"
            )

    # Handle the Show button or Combobox change by refreshing the leaderboard
    def on_show(self, event=None):
        self.refresh()
