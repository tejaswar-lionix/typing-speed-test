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


if __name__ == "__main__":
    unittest.main()
