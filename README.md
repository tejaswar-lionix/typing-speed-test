# typing-speed-test

Measure typing speed and accuracy with sample texts.

## Usage

```bash
python3 -c "from typing_test import *; print(words_per_minute(250, 60)); print(evaluate('helo', 'hello'))"
```

## Features

- Words-per-minute calculation
- Character accuracy and exact-match scoring
- Deterministic text selection with pick_text(level, rng)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
