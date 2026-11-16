import os
import tempfile
import unittest

from typing_test import accuracy, evaluate, words_per_minute


class TypingTests(unittest.TestCase):
    def test_words_per_minute(self):
        self.assertEqual(words_per_minute(250, 60), 50.0)
        self.assertEqual(words_per_minute(100, 30), 40.0)

    def test_words_per_minute_validation(self):
        with self.assertRaises(ValueError):
            words_per_minute(10, 0)
        with self.assertRaises(ValueError):
            words_per_minute(-1, 10)

    def test_accuracy(self):
        self.assertEqual(accuracy(90, 100), 90.0)
        self.assertEqual(accuracy(0, 0), 0.0)

    def test_accuracy_validation(self):
        with self.assertRaises(ValueError):
            accuracy(11, 10)

    def test_evaluate(self):
        result = evaluate("helo", "hello")
        self.assertEqual(result["correct_characters"], 3)
        self.assertEqual(result["total_characters"], 5)
        self.assertFalse(result["exact_match"])
        self.assertTrue(evaluate("hello", "hello")["exact_match"])


class PickTextTests(unittest.TestCase):
    def test_pick_text_is_deterministic(self):
        import random

        from typing_test import SAMPLE_TEXTS, pick_text

        first = pick_text("easy", random.Random(3))
        second = pick_text("easy", random.Random(3))
        self.assertEqual(first, second)
        self.assertIn(first, SAMPLE_TEXTS["easy"])

    def test_pick_text_rejects_unknown_level(self):
        from typing_test import pick_text

        with self.assertRaises(ValueError):
            pick_text("impossible")


class BestTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.directory.name, "bests.json")

    def tearDown(self):
        self.directory.cleanup()

    def test_missing_file_returns_empty(self):
        from typing_test import load_bests

        self.assertEqual(load_bests(self.path), {})

    def test_first_score_is_stored(self):
        from typing_test import load_bests, record_best

        self.assertEqual(record_best(self.path, "easy", 42), 42)
        self.assertEqual(load_bests(self.path), {"easy": 42})

    def test_lower_score_does_not_replace(self):
        from typing_test import load_bests, record_best

        record_best(self.path, "easy", 50)
        self.assertEqual(record_best(self.path, "easy", 40), 50)
        self.assertEqual(load_bests(self.path), {"easy": 50})

    def test_higher_score_replaces(self):
        from typing_test import load_bests, record_best

        record_best(self.path, "easy", 50)
        self.assertEqual(record_best(self.path, "easy", 60), 60)
        self.assertEqual(load_bests(self.path), {"easy": 60})

    def test_unknown_level_raises(self):
        from typing_test import record_best

        with self.assertRaises(ValueError):
            record_best(self.path, "impossible", 50)

    def test_negative_wpm_raises(self):
        from typing_test import record_best

        with self.assertRaises(ValueError):
            record_best(self.path, "easy", -1)


if __name__ == "__main__":
    unittest.main()
