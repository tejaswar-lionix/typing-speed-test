#!/usr/bin/env python3
"""Measure typing speed and accuracy."""
SAMPLE_TEXTS = {
    "easy": ["the quick brown fox jumps over the lazy dog"],
    "medium": ["practice every day and your typing speed will improve steadily"],
    "hard": [
        "consistent deliberate practice with immediate feedback compounds into durable skill"
    ],
}


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
