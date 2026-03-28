"""
save_manager.py
---------------
Handles loading and saving persistent game data to/from data.json.

Data persisted:
  - high_score       : all-time highest score
  - best_wave        : furthest wave ever reached
  - total_games      : lifetime games played
  - total_enemies    : lifetime enemies defeated

Usage:
    from save_manager import SaveManager
    sm = SaveManager()          # loads data.json (or creates defaults)
    sm.data["high_score"]       # read a value
    sm.update_after_game(score, wave, enemies)  # update & auto-save
    sm.save()                   # manual save
"""

import json
import os

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "high_score":    0,
    "best_wave":     0,
    "total_games":   0,
    "total_enemies": 0,
}


class SaveManager:
    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath
        self.data: dict = {}
        self.load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self) -> None:
        """Load data.json; create it with defaults if it doesn't exist."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                # Merge: use saved values, fall back to defaults for any missing key
                self.data = {**DEFAULT_DATA, **saved}
            except (json.JSONDecodeError, OSError):
                # Corrupted or unreadable – start fresh
                self.data = dict(DEFAULT_DATA)
                self.save()
        else:
            self.data = dict(DEFAULT_DATA)
            self.save()   # write the sample file on first run

    def save(self) -> None:
        """Write current data to data.json."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except OSError as e:
            print(f"[SaveManager] Warning: could not save data – {e}")

    def update_after_game(self, score: int, wave: int,
                          enemies_killed: int = 0) -> None:
        """
        Call once when a game ends.
        Updates records and increments counters, then saves automatically.
        """
        self.data["total_games"]   += 1
        self.data["total_enemies"] += enemies_killed

        changed = False
        if score > self.data["high_score"]:
            self.data["high_score"] = score
            changed = True
        if wave > self.data["best_wave"]:
            self.data["best_wave"] = wave
            changed = True

        self.save()
        return changed   # True if a new record was set

    # Convenience read-only properties
    @property
    def high_score(self) -> int:
        return self.data.get("high_score", 0)

    @property
    def best_wave(self) -> int:
        return self.data.get("best_wave", 0)

    @property
    def total_games(self) -> int:
        return self.data.get("total_games", 0)
