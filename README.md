# 🔐 PyPassword Generator

**A beginner-friendly Python command-line password generator using cryptographically secure randomness.**

PyPassword Generator is an interactive console application that creates randomized passwords based on the number of **letters, symbols, and digits** you choose. It mixes the characters into a single password and gives you the option to generate another without restarting the program.

I built this project to practice Python fundamentals and improve my understanding of input validation, lists, loops, functions, and randomization—while learning why password generation requires stronger randomness than ordinary games or simulations.

> **Educational project:** Passwords are generated locally and are not saved by this application. They are displayed in the terminal, so be mindful of screen recordings, screenshots, and terminal history.

## ✨ Features

- **Custom character counts:** Choose exactly how many letters, symbols, and digits to include.
- **Unpredictable character selection:** Uses Python's `secrets` module rather than the general-purpose `random` module.
- **Secure shuffling:** Randomly mixes the character groups using `secrets.SystemRandom().shuffle()`.
- **Input validation:** Handles invalid, negative, and excessive counts without crashing.
- **Flexible usage:** Supports zero of any individual group, but requires at least one character overall.
- **Strength reminder:** Warns when the password is shorter than 12 characters.
- **Generate again:** Make another password without relaunching the script.
- **No dependencies:** Works with the Python standard library.
- **Automated tests:** Includes built-in `unittest` tests for the generator and CLI.

## 🛠️ Technologies & concepts

| Technology / concept | How it's used |
| --- | --- |
| Python 3 | Main programming language |
| `secrets.choice()` | Selects individual characters using cryptographically secure randomness |
| `secrets.SystemRandom().shuffle()` | Mixes characters securely |
| `string.ascii_letters`, `string.digits` | Defines the available letters and numbers |
| Functions | Separates generation, validation, and interaction |
| Lists and loops | Builds passwords from requested character counts |
| `try` / `except` | Handles non-numeric input and interrupted sessions |
| `unittest` | Checks calculations, edge cases, and terminal interactions |

## 📁 Project structure

```text
py-password-generator/
├── password_generator.py       # Interactive CLI and password generation
├── test_password_generator.py  # Automated tests
├── README.md                   # Documentation
└── .gitignore                  # Git exclusions
```

## 🚀 Getting started

### Requirements

- Python **3.8 or newer**
- A terminal (PowerShell, Command Prompt, Terminal, etc.)

No `pip install` command or third-party package is required.

### Run locally

1. Download or clone the project.
2. Open the `py-password-generator` folder in VS Code or your terminal.
3. Run:

   **Windows:**
   ```powershell
   python password_generator.py
   ```

   **macOS / Linux:**
   ```bash
   python3 password_generator.py
   ```

   On Windows, `py password_generator.py` may also work.

### Clone from GitHub (after you publish your repository)

```bash
git clone https://github.com/Fafali1234557/py-password-generator.git
cd py-password-generator
python password_generator.py
```

Replace `Fafali1234557` with your GitHub username. If you're using macOS or Linux, run `python3` instead of `python` when necessary.

## 💻 Example interaction

```text
==========================================
         WELCOME TO PyPassword
==========================================
Create a randomized password using letters, symbols, and numbers.

Choose the number of characters in each group:
How many letters? 8
How many symbols? 2
How many numbers? 2

Your generated password: [randomized 12-character password]
Password length: 12 characters
Keep it private, and save it in a trusted password manager.

Generate another password? (yes/no): no

Thank you for using PyPassword!
```

**The example is illustrative:** Your actual password will be different each time.

## 🧠 How it works

### 1. Define allowed character groups

```python
import string

LETTERS = string.ascii_letters  # A-Z and a-z
NUMBERS = string.digits         # 0-9
SYMBOLS = "!#$%&()*+"
```

This preserves the symbol set used in the original project. You can extend `SYMBOLS` if you need additional symbols supported by your target service.

### 2. Ask the user for counts

The `ask_for_count()` function keeps prompting until the user enters a valid whole number from 0 to 128. The program also checks that the **total** password length is between 1 and 128 characters.

### 3. Generate the characters securely

```python
import secrets

characters = [secrets.choice(LETTERS) for _ in range(letter_count)]
characters += [secrets.choice(SYMBOLS) for _ in range(symbol_count)]
characters += [secrets.choice(NUMBERS) for _ in range(number_count)]
```

Unlike `random.choice()`, `secrets.choice()` is designed for applications where unpredictable values matter, such as tokens and passwords.

### 4. Shuffle and join

```python
secrets.SystemRandom().shuffle(characters)
password = "".join(characters)
```

Shuffling avoids leaving all letters first, then symbols, then digits. The final list is converted into a string using `join()`.

### 5. Show the result

The password is printed to the terminal. The user may choose to generate another one or exit.

## 🧪 Tests

Run the automated tests from the project folder:

```bash
python -m unittest -v
```

On macOS/Linux, you may need `python3 -m unittest -v`.

The tests verify:

- Exact counts of letters, symbols, and digits
- Correct output lengths and allowed characters
- Zero, negative, non-integer, and over-limit inputs
- Retrying invalid input and yes/no responses
- Handling a completely empty selection or excessive total length
- Generating multiple passwords in one session
- Warnings for short passwords

## 🔒 Security notes

- The application uses a **cryptographically secure random source**, but password strength also depends on length, character choices, and how you store and use the password.
- For real accounts, prefer a unique password of **at least 12–16 characters**, or follow the service's specific requirements. Longer is generally better.
- Use a trusted password manager and enable multi-factor authentication where possible.
- The application **prints passwords to the terminal**. Avoid sharing screenshots or pasting a password into public places.
- The application does **not** write passwords to files, connect to a network, or store generated passwords. Your terminal or device may have its own recording or logging behavior.
- The limited symbol set may not match every site's password rules. Check the target service's accepted characters.

## 📚 What I learned

This project helped me practise:

- Lists, `for` loops, and list comprehensions
- Functions, parameters, and return values
- User input and type conversion
- `while` loops and conditional statements
- Error handling with `try` / `except`
- Joining strings with `"".join()`
- Writing tests for expected and unexpected inputs
- Using secure randomness appropriately

## 🔮 Future improvements

- [ ] Add optional minimum length presets (12, 16, 20+)
- [ ] Allow users to include or exclude ambiguous characters such as `O`, `0`, `l`, and `1`
- [ ] Add an optional password-strength explanation
- [ ] Provide an option to generate multiple passwords at once
- [ ] Build a graphical desktop interface
- [ ] Add a user-friendly web interface without sending passwords to a server

## 🤝 Feedback and contributions

This is a learning project, and feedback is welcome. Feel free to explore the code, suggest improvements, or fork the repository for experimentation.

---

**Built with Python and a passion for learning by building. 🐍🔐**
