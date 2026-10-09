"""PyPassword Generator: create randomized passwords from chosen character groups.

The standard-library ``secrets`` module supplies cryptographically secure random
choices. No passwords are saved to disk or transmitted by this application.
"""

import secrets
import string


LETTERS = string.ascii_letters
NUMBERS = string.digits
SYMBOLS = "!#$%&()*+"
MAX_PASSWORD_LENGTH = 128
RECOMMENDED_MIN_LENGTH = 12


def generate_password(letter_count: int, symbol_count: int, number_count: int) -> str:
    """Generate a password with exactly the requested character-group counts.

    Raises:
        TypeError: If any count is not an integer.
        ValueError: If a count is negative or total length is outside 1..128.
    """
    counts = (letter_count, symbol_count, number_count)

    if any(type(count) is not int for count in counts):
        raise TypeError("Character counts must be integers.")
    if any(count < 0 for count in counts):
        raise ValueError("Character counts cannot be negative.")

    total_length = sum(counts)
    if not 1 <= total_length <= MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password length must be between 1 and {MAX_PASSWORD_LENGTH} characters."
        )

    characters = (
        [secrets.choice(LETTERS) for _ in range(letter_count)]
        + [secrets.choice(SYMBOLS) for _ in range(symbol_count)]
        + [secrets.choice(NUMBERS) for _ in range(number_count)]
    )

    # Shuffle the groups so letters, symbols, and numbers aren't predictable by position.
    secrets.SystemRandom().shuffle(characters)
    return "".join(characters)


def ask_for_count(prompt: str) -> int:
    """Ask repeatedly for an integer count from 0 to MAX_PASSWORD_LENGTH."""
    while True:
        raw_value = input(prompt).strip()
        try:
            count = int(raw_value)
        except ValueError:
            print("Please enter a whole number (for example, 5).")
            continue

        if count < 0:
            print("Please enter 0 or a positive number.")
        elif count > MAX_PASSWORD_LENGTH:
            print(f"Please choose {MAX_PASSWORD_LENGTH} or fewer characters per group.")
        else:
            return count


def ask_to_repeat() -> bool:
    """Ask whether another password should be generated."""
    while True:
        answer = input("\nGenerate another password? (yes/no): ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please type yes or no.")


def main() -> None:
    """Run the interactive password generator."""
    print("=" * 42)
    print("         WELCOME TO PyPassword")
    print("=" * 42)
    print("Create a randomized password using letters, symbols, and numbers.")

    while True:
        print("\nChoose the number of characters in each group:")
        letter_count = ask_for_count("How many letters? ")
        symbol_count = ask_for_count("How many symbols? ")
        number_count = ask_for_count("How many numbers? ")

        total_length = letter_count + symbol_count + number_count
        if total_length == 0:
            print("Please select at least one character. Try again.")
            continue
        if total_length > MAX_PASSWORD_LENGTH:
            print(f"The total cannot exceed {MAX_PASSWORD_LENGTH} characters. Try again.")
            continue

        if total_length < RECOMMENDED_MIN_LENGTH:
            print(
                f"Note: {total_length} characters is short. "
                f"Consider using at least {RECOMMENDED_MIN_LENGTH} for real accounts."
            )

        password = generate_password(letter_count, symbol_count, number_count)
        print(f"\nYour generated password: {password}")
        print(f"Password length: {total_length} characters")
        print("Keep it private, and save it in a trusted password manager.")

        if not ask_to_repeat():
            print("\nThank you for using PyPassword!")
            break


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPassword generation cancelled.")
