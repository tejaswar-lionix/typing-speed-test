#!/usr/bin/env python3
"""Measure typing speed and accuracy."""
import csv
import json
import os
from datetime import date

SAMPLE_TEXTS = {
    "easy": ["the quick brown fox jumps over the lazy dog"],
    "medium": ["practice every day and your typing speed will improve steadily"],
    "hard": [
        "consistent deliberate practice with immediate feedback compounds into durable skill"
    ],
}
HISTORY_HEADERS = ["date", "level", "wpm", "accuracy"]


def words_per_minute(characters, seconds):
    if characters < 0:
        raise ValueError("characters must not be negative")
    if seconds <= 0:
        raise ValueError("seconds must be positive")
    return round((characters / 5) / (seconds / 60), 1)


def accuracy(correct, total):
    if correct < 0 or total < 0:
        raise ValueError("counts must not be negative")
    if correct > total:
        raise ValueError("correct cannot exceed total")
    if total == 0:
        return 0.0
    return round(correct / total * 100, 1)


def evaluate(typed, expected):
    correct = sum(1 for a, b in zip(typed, expected) if a == b)
    total = max(len(typed), len(expected))
    return {
        "correct_characters": correct,
        "total_characters": total,
        "accuracy": accuracy(correct, total),
        "exact_match": typed == expected,
    }


def pick_text(level="easy", rng=None):
    """Pick a sample text for the given difficulty level."""
    import random

    if level not in SAMPLE_TEXTS:
        raise ValueError("level must be easy, medium, or hard")
    rng = rng or random.Random()
    return rng.choice(SAMPLE_TEXTS[level])


def load_bests(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def record_best(path, level, wpm):
    """Record a personal best for a level and return the stored best."""
    if level not in SAMPLE_TEXTS:
        raise ValueError("level must be easy, medium, or hard")
    if wpm < 0:
        raise ValueError("wpm must not be negative")
    bests = load_bests(path)
    if level not in bests or wpm > bests[level]:
        bests[level] = wpm
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(bests, handle, indent=2)
    return bests[level]


def log_result(path, level, wpm, accuracy, day=None):
    """Append a session result to a CSV history log."""
    if level not in SAMPLE_TEXTS:
        raise ValueError("level must be easy, medium, or hard")
    if wpm < 0:
        raise ValueError("wpm must not be negative")
    if not 0 <= accuracy <= 100:
        raise ValueError("accuracy must be between 0 and 100")
    row = [day or date.today().isoformat(), level, wpm, accuracy]
    needs_header = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if needs_header:
            writer.writerow(HISTORY_HEADERS)
        writer.writerow(row)
    return row


def history(path):
    """Return recorded session results as a list of dictionaries."""
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as handle:
        return [
            {
                "date": row["date"],
                "level": row["level"],
                "wpm": float(row["wpm"]),
                "accuracy": float(row["accuracy"]),
            }
            for row in csv.DictReader(handle)
        ]


def clear_history(path):
    """Remove the history file, returning True when it was deleted."""
    if not os.path.exists(path):
        return False
    os.remove(path)
    return True


def average_wpm(path, level=None):
    """Return the mean words-per-minute from the history log."""
    rows = history(path)
    if level is not None:
        rows = [row for row in rows if row["level"] == level]
    if not rows:
        return 0.0
    return round(sum(row["wpm"] for row in rows) / len(rows), 1)


def best_wpm(path):
    """Return the best recorded WPM per level from the history log."""
    bests = {}
    for row in history(path):
        level = row["level"]
        if level not in bests or row["wpm"] > bests[level]:
            bests[level] = row["wpm"]
    return bests
