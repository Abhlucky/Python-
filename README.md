# 🎯 Number Guessing Game

A simple Python number guessing game where the computer randomly selects a number between **1 and 100**, and the player tries to guess it.

## 📌 Features

* Generates a random number between **1 and 100**
* Takes the player's guess as input
* Checks whether the guess is correct
* Displays a winning message if the guess is correct
* Shows the correct number if the guess is wrong

## 🛠️ Requirements

* Python 3.x

No external libraries are required. The game uses Python's built-in `random` module.

## ▶️ How to Run

1. Make sure Python is installed on your computer.
2. Open the project folder in VS Code or a terminal.
3. Run the following command:

```bash
python Guess.py
```

## 🎮 How to Play

1. Run the program.
2. Enter a number between **1 and 100**.
3. The program will check your guess.
4. If your guess is correct, you win!
5. If your guess is incorrect, the program reveals the correct number.

## 💻 Example

```text
Guess a number between 1 and 100: 45
you lost!! The number was 72
```

If you guess the correct number:

```text
Guess a number between 1 and 100: 72
you won!!!
```

## 📂 Project Structure

```text
Guessing-Game/
│
├── Guess.py
└── README.md
```

## 📚 Concepts Used

This project demonstrates basic Python concepts:

* `import`
* `random.randint()`
* `input()`
* Type conversion using `int()`
* `if-else` conditions
* Variables
* Printing output

## 🚀 Future Improvements

Some features that can be added later:

* Multiple attempts
* Hints like **Too High / Too Low**
* Score system
* Difficulty levels
* Play Again option
* Number of attempts counter

---

**Made with Python 🐍**
