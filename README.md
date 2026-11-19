# typing-speed-test

Measure typing speed and accuracy with sample texts.

## Usage

```bash
python3 -c "from typing_test import *; print(words_per_minute(250, 60)); print(evaluate('helo', 'hello'))"
python3 -c "from typing_test import record_best, load_bests; print(record_best('bests.json', 'easy', 55)); print(load_bests('bests.json'))"
python3 -c "from typing_test import log_result, history; log_result('history.csv', 'easy', 55, 98); print(history('history.csv'))"
python3 -c "from typing_test import average_wpm; print(average_wpm('history.csv', level='easy'))"
python3 -c "from typing_test import clear_history; print(clear_history('history.csv'))"
```

## Features

- Words-per-minute calculation
- Character accuracy and exact-match scoring
- Deterministic text selection with pick_text(level, rng)
- Personal bests persisted as JSON with record_best(path, level, wpm)
- Session history logged to CSV with log_result(path, level, wpm, accuracy) and read with history(path)
- Average speed with average_wpm(path, level=None)
- Clear the history log with clear_history(path)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
