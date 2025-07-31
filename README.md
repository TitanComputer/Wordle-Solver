# 💻 Wordle Solver

This is a graphical Wordle Solver application built with Python and `ttkbootstrap`.

This application helps you solve Wordle puzzles more easily by narrowing down possible answers based on your input.

## ❓ What is Wordle?

[Wordle](https://www.nytimes.com/games/wordle/index.html) is a word-guessing game where the player has 6 attempts to guess a hidden 5-letter word.

After each guess, the game gives feedback about the correctness and position of each letter using color codes.

This tool helps users find possible answers based on the feedback from their previous guesses.

## 🚀 Features

- Sleek GUI using [`ttkbootstrap`](https://ttkbootstrap.readthedocs.io/)
- Supports dark/light mode
- Result filtering based on positional and character feedback
- Downloadable `.exe` version (Windows only)

## 🖼️ Screenshots

<img width="1008" height="682" alt="Untitled" src="https://github.com/user-attachments/assets/7c49d857-64a2-4fde-88cd-8e9f4782bbc3" />

### 🎬 Usage Guide (Video)

https://github.com/user-attachments/assets/54eac32e-0a36-4084-b4b5-417c0724e505

## 📥 Download

You can download the latest compiled `.exe` version from the [Releases](https://github.com/TitanComputer/Wordle-Solver/releases/latest) section.  
No need to install Python — just download and run.

## ⚙️ Usage

If you're using the Python script:
```bash
python main.py
```
Or, run the Wordle-Solver.exe file directly if you downloaded the compiled version.

### 🖥️ How to Use the GUI

When you open the program:

1. **Enter known letters in the Known Positions row**  
   These are letters in the correct position (🟩). If you know a letter must be at a certain spot, type it in that position. Leave unknown spots empty.

2. **Enter misplaced letters in the Unknown Positions rows**  
   These are letters that are in the word, but not in the correct position (🟨). You can type multiple letters per box, separated by spaces, if needed.

3. **Enter excluded letters in the Not Included rows**  
   These are letters that are definitely **not** in the word (⬛️). Type all such letters in the input box.

4. **Click the "Submit Query" button**  
   The program will scan the dictionary and show only the words that match your clues.

5. **Review the results**  
   A list of possible words will be displayed. You can use this to help choose your next guess in Wordle.

6. **Use the "Reset" button** if you want to start over.

7. **Optional: Toggle Dark Mode** using the Dark Mode toggle to change the application's theme.

---

### 📌 Example

If Wordle gave you the following hint:

- Correct letter at position 2 is `A`
- `R` is somewhere in the word, but not in position 3
- Letters `S`, `E`, and `T` are not in the word

You would:
- Type `A` into the second box in the green row
- Type `R` into the yellow row (not in box 3)
- Type `S E T` into the gray box
- Click "Submit Query" to get valid words like: `HAIRY`, `LABOR`, etc.

---

### 💡 Notes

- All guesses must be exactly 5 letters
- The dictionary is case-insensitive and cleansed of invalid words
- You can update `words.txt` in the `dict/` folder to customize the wordlist by clicking on the "Get Dictionary" button


## 📦 Dependencies

- Python 3.9 or newer
- `ttkbootstrap`
- Recommended: Create a virtual environment

Standard libraries only (os, re, etc.)

If you're modifying and running the script directly and use additional packages (like requests or tkinter), install them via:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```bash
wordle_solver/
│
├── main.py                     # Main application entry point
├── solver.py                   # Application core logic
├── dict/
│   ├── words.txt               # Dictionary of english words
│   └── words_filtered.txt      # Dictionary of valid 5-letter words
├── README.md                   # Project documentation
├── assets/
│   ├── icon.png                # Project icon
│   ├── heart.png               # Heart Logo
│   └── donate.png              # Donate Picture
└── requirements.txt            # Python dependencies
```
## 🎨 Icon Credit

The application icon used in this project is sourced from [Flaticon](https://www.flaticon.com/free-icons/puzzle).

**Puzzle icon** created by [monkik](https://www.flaticon.com/authors/monkik) – [Flaticon](https://www.flaticon.com/)

## 🛠 Compiled with Nuitka and UPX
The executable was built using [`Nuitka`](https://nuitka.net/) and [`UPX`](https://github.com/upx/upx) for better performance and compactness.

You can build the standalone executable using the following command:

```bash
.\venv\Scripts\python.exe -m nuitka --jobs=4 --enable-plugin=upx --upx-binary="YOUR PATH\upx.exe" --enable-plugin=multiprocessing --lto=yes --enable-plugin=tk-inter --windows-console-mode=disable --follow-imports --windows-icon-from-ico="icon.ico" --include-data-dir=assets=assets --python-flag=no_site,no_asserts,no_docstrings --onefile --standalone --msvc=latest main.py
```

## 🤝 Contributing
Pull requests are welcome.
If you have suggestions for improvements or new features, feel free to open an issue.

## ☕ Support
If you find this project useful and would like to support its development, consider donating:

<a href="http://www.coffeete.ir/Titan"><img width="500" height="140" alt="buymeacoffee" src="https://github.com/user-attachments/assets/8ddccb3e-2afc-4fd9-a782-89464ec7dead" /></a>

## 💰 USDT (Tether) – TRC20 Wallet Address:

```bash
TGoKk5zD3BMSGbmzHnD19m9YLpH5ZP8nQe
```
Thanks a lot for your support! 🙏
