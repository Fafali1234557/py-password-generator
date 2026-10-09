"""Unit tests for the PyPassword Generator.

Run: python -m unittest -v
"""

import io
import string
import unittest
from collections import Counter
from contextlib import redirect_stdout
from unittest.mock import patch

from password_generator import (
    LETTERS,
    MAX_PASSWORD_LENGTH,
    NUMBERS,
    SYMBOLS,
    ask_for_count,
    ask_to_repeat,
    generate_password,
    main,
)


class TestGeneratePassword(unittest.TestCase):
    def test_exact_counts_and_length(self):
        for letters, symbols, numbers in (
            (8, 3, 2), (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (10, 0, 10), (0, 10, 10), (64, 32, 32),
        ):
            with self.subTest(counts=(letters, symbols, numbers)):
                password = generate_password(letters, symbols, numbers)
                self.assertEqual(len(password), letters + symbols + numbers)
                self.assertEqual(sum(c in LETTERS for c in password), letters)
                self.assertEqual(sum(c in SYMBOLS for c in password), symbols)
                self.assertEqual(sum(c in NUMBERS for c in password), numbers)

    def test_groups_do_not_overlap(self):
        self.assertTrue(set(LETTERS).isdisjoint(SYMBOLS))
        self.assertTrue(set(LETTERS).isdisjoint(NUMBERS))
        self.assertTrue(set(SYMBOLS).isdisjoint(NUMBERS))

    def test_output_is_a_string(self):
        self.assertIsInstance(generate_password(6, 2, 2), str)

    def test_password_characters_come_from_supported_sets(self):
        self.assertTrue(set(generate_password(9, 5, 3)).issubset(set(LETTERS + SYMBOLS + NUMBERS)))

    def test_zero_total_rejected(self):
        with self.assertRaisesRegex(ValueError, "Password length"):
            generate_password(0, 0, 0)

    def test_negative_letter_count_rejected(self):
        with self.assertRaises(ValueError):
            generate_password(-1, 1, 1)

    def test_negative_symbol_count_rejected(self):
        with self.assertRaises(ValueError):
            generate_password(1, -1, 1)

    def test_negative_number_count_rejected(self):
        with self.assertRaises(ValueError):
            generate_password(1, 1, -1)

    def test_excess_length_rejected(self):
        with self.assertRaises(ValueError):
            generate_password(MAX_PASSWORD_LENGTH, 1, 0)

    def test_non_integer_rejected(self):
        for bad_value in (1.5, "3", None, True):
            with self.subTest(value=bad_value):
                with self.assertRaises(TypeError):
                    generate_password(bad_value, 1, 1)

    def test_not_a_fixed_output(self):
        # Two securely sampled long passwords matching is astronomically unlikely.
        self.assertNotEqual(generate_password(30, 10, 10), generate_password(30, 10, 10))


class TestInteractiveInput(unittest.TestCase):
    def test_valid_count(self):
        with patch("builtins.input", return_value="  12  "):
            self.assertEqual(ask_for_count("Count: "), 12)

    def test_invalid_integer_retried(self):
        with patch("builtins.input", side_effect=["abc", "2.5", "5"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(ask_for_count("Count: "), 5)

    def test_negative_retried(self):
        with patch("builtins.input", side_effect=["-2", "4"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(ask_for_count("Count: "), 4)

    def test_count_too_large_retried(self):
        with patch("builtins.input", side_effect=["129", "128"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(ask_for_count("Count: "), MAX_PASSWORD_LENGTH)

    def test_yes_variants(self):
        for answer in ("YES", "y", " Yes "):
            with self.subTest(answer=answer):
                with patch("builtins.input", return_value=answer):
                    self.assertTrue(ask_to_repeat())

    def test_no_variants(self):
        for answer in ("NO", "n", " No "):
            with self.subTest(answer=answer):
                with patch("builtins.input", return_value=answer):
                    self.assertFalse(ask_to_repeat())

    def test_invalid_yes_no_retried(self):
        with patch("builtins.input", side_effect=["maybe", "yes"]):
            with redirect_stdout(io.StringIO()):
                self.assertTrue(ask_to_repeat())

    def test_main_retries_zero_total(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["0", "0", "0", "8", "2", "2", "no"]):
            with redirect_stdout(output):
                main()
        self.assertIn("Please select at least one character", output.getvalue())
        self.assertIn("Password length: 12 characters", output.getvalue())

    def test_main_retries_total_too_large(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["128", "1", "0", "8", "2", "2", "no"]):
            with redirect_stdout(output):
                main()
        self.assertIn("total cannot exceed", output.getvalue())
        self.assertIn("Password length: 12 characters", output.getvalue())

    def test_main_replay(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["8", "2", "2", "yes", "10", "3", "3", "no"]):
            with redirect_stdout(output):
                main()
        self.assertEqual(output.getvalue().count("Your generated password:"), 2)
        self.assertIn("Thank you for using PyPassword!", output.getvalue())

    def test_short_password_warning(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["4", "1", "1", "n"]):
            with redirect_stdout(output):
                main()
        self.assertIn("characters is short", output.getvalue())


if __name__ == "__main__":
    unittest.main()
