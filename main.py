from solver import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import StringVar
from tkinter import messagebox
from tkinter import PhotoImage
import threading
from idlelib.tooltip import Hovertip
import webbrowser


class WordleSolverApp(tb.Window):
    def __init__(self):
        self.current_theme = "litera"  # light theme by default
        super().__init__(themename=self.current_theme)
        self.icon = PhotoImage(file="icon.png")

        self.style.configure("Default.TEntry", fieldbackground="white", foreground="#000000")
        self.style.configure("Known.TEntry", fieldbackground="#6aaa64", foreground="#ffffff")
        self.style.configure("Unknown.TEntry", fieldbackground="#c9b458", foreground="#ffffff")
        self.style.configure("Excluded.TEntry", fieldbackground="#787c7e", foreground="#ffffff")
        self.style.configure("Success-Inverse.TLabel", background="#18813b", foreground="#ffffff")

        self.apply_custom_styles()

        self.title("Wordle Solver")
        self.withdraw()
        self.iconphoto(False, self.icon)
        self.minsize(550, 650)
        self.resizable(False, False)
        self.center_window()
        self.deiconify()
        self.last_entry_value = ""
        self.is_dark_mode = False
        self.words = None
        self.analyzer = None

        self.setup_layout()

    def apply_custom_styles(self):
        # Buttons
        """Apply custom styles to ttk widgets.

        This method sets the style of various ttk widgets such as buttons,
        checkbuttons, and entries. The styles are set based on the current
        theme of the application.

        """
        self.style.configure("primary.TButton", font=("Arial", 16, "bold"))
        self.style.configure("info.TButton", font=("Arial", 16, "bold"))
        self.style.configure("warning.TButton", font=("Arial", 16, "bold"))
        self.style.configure("success.TButton", font=("Arial", 16, "bold"))
        self.style.configure("danger.TButton", font=("Arial", 11, "bold"))
        self.style.configure("secondary.TButton", font=("Arial", 16, "bold"))
        self.style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))
        self.style.configure(
            "OutlinePrimaryBold.TButton",
            font=("Arial", 14, "bold"),
            foreground="#0d6efd",
            background="white",
            borderwidth=2,
            relief="solid",
            padding=(10, 5),
            anchor="center",
            justify="center",
        )
        self.style.map(
            "OutlinePrimaryBold.TButton",
            foreground=[("active", "#0a58ca"), ("pressed", "#084298")],
            background=[("active", "white"), ("pressed", "white")],
            bordercolor=[("active", "#0a58ca"), ("pressed", "#084298")],
        )
        self.style.configure(
            "OutlineSuccess.TButton",
            font=("Arial", 14, "bold"),
            foreground="#198754",
            background="white",
            borderwidth=2,
            relief="solid",
            padding=(10, 5),
            anchor="center",
            justify="center",
        )
        self.style.map(
            "OutlineSuccess.TButton",
            foreground=[("active", "#146c43"), ("pressed", "#0f5132")],
            background=[("active", "white"), ("pressed", "white")],
            bordercolor=[("active", "#146c43"), ("pressed", "#0f5132")],
        )
        self.style.configure(
            "OutlineMidSuccess.TButton",
            font=("Arial", 14, "bold"),
            foreground="#6fcf97",
            background="white",
            borderwidth=2,
            relief="solid",
            padding=(10, 5),
            anchor="center",
            justify="center",
        )
        self.style.map(
            "OutlineMidSuccess.TButton",
            foreground=[("active", "#81dab0"), ("pressed", "#5bbf85")],
            background=[("active", "white"), ("pressed", "white")],
            bordercolor=[("active", "#81dab0"), ("pressed", "#5bbf85")],
        )

        # Checkbutton
        self.style.configure("Square.Toggle", font=("Arial", 12, "bold"))

    def toggle_theme(self):
        """
        Toggle between light and dark theme.

        This function changes the theme of the application window, and
        also updates the style of all the entries and buttons accordingly.

        If the theme is changed to dark, it sets the background color of
        all empty entries to match the dark theme.

        :return: None
        """
        self.is_dark_mode = not self.is_dark_mode
        new_theme = "darkly" if self.is_dark_mode else "litera"
        self.style.theme_use(new_theme)
        self.apply_custom_styles()

        # Reset entry styles after theme change
        if self.is_dark_mode:
            self.style.configure("Default.TEntry", fieldbackground="#121213", foreground="#ffffff")
            self.style.configure("Known.TEntry", fieldbackground="#538d4e", foreground="#ffffff")
            self.style.configure("Unknown.TEntry", fieldbackground="#b59f3b", foreground="#ffffff")
            self.style.configure("Excluded.TEntry", fieldbackground="#3a3a3c", foreground="#ffffff")
            self.style.configure(
                "OutlinePrimaryBold.TButton",
                font=("Arial", 14, "bold"),
                foreground="#66b2ff",
                background="#212529",
                borderwidth=2,
                relief="solid",
                padding=(10, 5),
            )
            self.style.map(
                "OutlinePrimaryBold.TButton",
                foreground=[("active", "#99ccff"), ("pressed", "#cce6ff")],
                background=[("active", "#212529"), ("pressed", "#212529")],
                bordercolor=[("active", "#99ccff"), ("pressed", "#cce6ff")],
            )
            self.style.configure(
                "OutlineSuccess.TButton",
                font=("Arial", 14, "bold"),
                foreground="#198754",
                background="#212529",
                borderwidth=2,
                relief="solid",
                padding=(10, 5),
            )
            self.style.map(
                "OutlineSuccess.TButton",
                foreground=[("active", "#27ae60"), ("pressed", "#1e8449")],
                background=[("active", "#212529"), ("pressed", "#212529")],
                bordercolor=[("active", "#27ae60"), ("pressed", "#1e8449")],
            )
            self.style.configure(
                "OutlineMidSuccess.TButton",
                font=("Arial", 14, "bold"),
                foreground="#6fcf97",  # soft green
                background="#212529",
                borderwidth=2,
                relief="solid",
                padding=(10, 5),
            )
            self.style.map(
                "OutlineMidSuccess.TButton",
                foreground=[("active", "#81dab0"), ("pressed", "#5bbf85")],
                background=[("active", "#212529"), ("pressed", "#212529")],
                bordercolor=[("active", "#81dab0"), ("pressed", "#5bbf85")],
            )

        else:
            self.style.configure("Default.TEntry", fieldbackground="white", foreground="#000000")
            self.style.configure("Known.TEntry", fieldbackground="#6aaa64", foreground="#ffffff")
            self.style.configure("Unknown.TEntry", fieldbackground="#c9b458", foreground="#ffffff")
            self.style.configure("Excluded.TEntry", fieldbackground="#787c7e", foreground="#ffffff")
            self.style.configure(
                "OutlinePrimaryBold.TButton",
                font=("Arial", 14, "bold"),
                foreground="#0d6efd",
                background="white",
                borderwidth=2,
                relief="solid",
                padding=(10, 5),
            )
            self.style.map(
                "OutlinePrimaryBold.TButton",
                foreground=[("active", "#0a58ca"), ("pressed", "#084298")],
                background=[("active", "white"), ("pressed", "white")],
                bordercolor=[("active", "#0a58ca"), ("pressed", "#084298")],
            )
            self.style.configure(
                "OutlineSuccess.TButton",
                font=("Arial", 14, "bold"),
                foreground="#198754",
                background="white",
                borderwidth=2,
                relief="solid",
                padding=(10, 5),
            )
            self.style.map(
                "OutlineSuccess.TButton",
                foreground=[("active", "#146c43"), ("pressed", "#0f5132")],
                background=[("active", "white"), ("pressed", "white")],
                bordercolor=[("active", "#146c43"), ("pressed", "#0f5132")],
            )
            self.style.configure(
                "OutlineMidSuccess.TButton",
                font=("Arial", 14, "bold"),
                foreground="#6fcf97",
                background="white",
                borderwidth=2,
                relief="solid",
                padding=(10, 5),
            )
            self.style.map(
                "OutlineMidSuccess.TButton",
                foreground=[("active", "#81dab0"), ("pressed", "#5bbf85")],
                background=[("active", "white"), ("pressed", "white")],
                bordercolor=[("active", "#81dab0"), ("pressed", "#5bbf85")],
            )

        self.style.configure("Success-Inverse.TLabel", background="#18813b", foreground="#ffffff")

        # Update all empty entries to Default style so background matches theme
        for entry in self.get_all_entries():
            if not entry.get():
                entry.configure(style="Default.TEntry")

    def center_window(self):
        """
        Centers the main application window on the screen.

        This function calculates the appropriate x and y coordinates such that
        the window is positioned at the center of the user's screen. It sets the
        window's geometry using a fixed width and height.
        """
        self.update_idletasks()
        width = 550
        height = 650
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def center_main_and_result(self, result_width, result_height):
        """
        Centers the main application window and the result window on the screen.

        This function takes into account the width and height of the result window
        when positioning the main window. It places the main window at the left
        side of the screen and the result window at the right side of the screen.

        The main window is positioned so that its top-left corner is at the center
        of the screen. The result window is positioned so that its top-left corner
        is at the center of the screen, right of the main window.

        If the combined width of the two windows is larger than the screen width,
        the windows will be positioned at the left edge of the screen. If the
        combined height of the windows is larger than the screen height, the
        windows will be positioned at the top edge of the screen.

        :param result_width: width of the result window in pixels
        :param result_height: height of the result window in pixels
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.update_idletasks()
        main_width = self.winfo_width()
        main_height = self.winfo_height()

        total_width = main_width + result_width
        total_height = max(main_height, result_height)

        x = (screen_width - total_width) // 2
        y = (screen_height - total_height) // 2

        self.geometry(f"{main_width}x{main_height}+{x}+{y}")
        self.result_window.geometry(f"{result_width}x{result_height}+{x + main_width}+{y}")

    def how_to_play(self):
        top = tb.Toplevel(self)
        top.title("How To Play")
        top.resizable(False, False)
        top.iconphoto(False, self.icon)

        # Center the window
        top.withdraw()
        top.update_idletasks()
        width = 550
        height = 700
        x = (top.winfo_screenwidth() // 2) - (width // 2)
        y = (top.winfo_screenheight() // 2) - (height // 2)
        top.geometry(f"{width}x{height}+{x}+{y}")
        top.deiconify()

        # Modal behavior
        top.grab_set()
        top.transient(self)

        # Main frame
        frame = tb.Frame(top, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        def section_title(text):
            return tb.Label(frame, text=text, font=("Segoe UI", 14, "bold"))

        def section_body(text):
            return tb.Label(frame, text=text, font=("Segoe UI", 11), wraplength=480, justify="left")

        row = 0

        # GOAL
        section_title("🎯 Goal").grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 2))
        row += 1
        section_body("Guess the hidden 5-letter word in 6 tries or less.").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )
        row += 1

        # Wordle link
        section_title("🔗 Play the Original Wordle").grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 2))
        row += 1
        section_body("Click the button below to open Wordle in your browser.").grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1

        def open_wordle():
            webbrowser.open_new("https://www.nytimes.com/games/wordle/")

        tb.Button(frame, text="🔗 Open Wordle", bootstyle="link", command=open_wordle).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )
        row += 1

        # How to Guess
        section_title("⌨️ How to Guess").grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 2))
        row += 1
        section_body("Enter a valid 5-letter English word each time you try.").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )
        row += 1

        # Color meanings
        section_title("🎨 Color Codes").grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 2))
        row += 1
        section_body(
            "🟩 Green: Correct letter in the correct spot\n🟨 Yellow: Correct letter but in the wrong spot\n⬛ Gray: Letter is not in the word"
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 10))
        row += 1

        # Tips
        section_title("💡 Tips").grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 2))
        row += 1
        section_body(
            "- Start with words like 'raise', 'adieu', or 'salet'.\n- Use the 'Best Words to Start' feature to get suggestions."
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 10))
        row += 1

        # How this app works
        section_title("🆘 How to Use This App").grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 2))
        row += 1
        section_body(
            "- After each guess, update the grid using the boxes.\n- Green = correct letter & position\n- Yellow = correct letter, wrong position\n- Gray = letter not in the word"
        ).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 20))
        row += 1

        # Final message
        section_body("Good luck and have fun! 🧩").grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 20))
        row += 1

        # Close button
        close_button = tb.Button(frame, text="Close", bootstyle="secondary", command=top.destroy)
        close_button.configure(width=12, padding=10)
        close_button.grid(row=row, column=1, sticky="e")

        # Expand settings
        frame.rowconfigure(row, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)

    def best_words(self):
        """
        Calculate and display the best starting words based on letter frequency.

        This function reads a list of filtered words from a file, analyzes the
        frequency of each letter, and suggests the top words to start with in a
        Wordle game. It displays the letter frequencies and the best starting words
        in a new window.

        The function operates in a separate thread to avoid blocking the main
        application.

        If the word list is not already loaded, it reads it from 'words_filtered.txt'.
        If the letter frequency analyzer is not initialized, it creates and analyzes
        it.

        The results are shown in a top-level window with two sections: one for
        letter frequencies and one for the best starting words based on frequency
        scores.
        """

        def worker():
            if self.words is None:
                file_path = "dict/words_filtered.txt"
                if not os.path.exists(file_path):
                    self.after(
                        0,
                        lambda: messagebox.showerror(
                            "File Not Found", "words_filtered.txt not found!\nPlease click 'Get Dictionary' first."
                        ),
                    )
                    return
                with open(file_path, "r", encoding="utf-8") as f:
                    self.words = tuple(line.strip() for line in f if line.strip())

            if self.analyzer is None:
                self.analyzer = LetterFrequencyAnalyzer()
                self.analyzer.analyze()

            letter_freqs = self.analyzer.frequencies.most_common()
            best_words = self.analyzer.suggest_best_words(self.words, top_n=26)

            self.after(0, lambda: show_results(letter_freqs, best_words))

        def show_results(letter_freqs, best_words):
            top = tb.Toplevel(self)
            top.title("Letter Frequency & Best Words To Start")
            top.resizable(False, False)

            # Center the window
            top.withdraw()
            top.iconphoto(False, self.icon)
            top.update_idletasks()
            width = 450
            height = 800
            x = (top.winfo_screenwidth() // 2) - (width // 2)
            y = (top.winfo_screenheight() // 2) - (height // 2)
            top.geometry(f"{width}x{height}+{x}+{y}")
            top.deiconify()

            # Modal behavior
            top.grab_set()
            top.transient(self)

            # Configure grid for top-level to center container vertically
            top.grid_rowconfigure(0, weight=1)
            top.grid_rowconfigure(2, weight=1)
            top.grid_columnconfigure(0, weight=1)

            container = tb.Frame(top)
            container.grid(row=1, column=0)  # center row

            # Center the container horizontally
            container.grid_columnconfigure(0, weight=1)
            container.grid_columnconfigure(1, weight=1)

            # Create label frames
            left_frame = tb.Labelframe(
                container,
                text="   Letter Frequency (%)   ",
                bootstyle="info",
                labelanchor="n",
            )
            right_frame = tb.Labelframe(
                container,
                text="   Best Words To Start (Score)   ",
                bootstyle="success",
                labelanchor="n",
            )

            left_frame.grid(row=0, column=0, padx=10, pady=5, ipady=5, sticky="n")
            right_frame.grid(row=0, column=1, padx=10, pady=5, ipady=5, sticky="n")

            # Make sure columns in each frame expand
            left_frame.grid_columnconfigure(0, weight=1)
            right_frame.grid_columnconfigure(0, weight=1)

            total_freq = sum(freq for _, freq in letter_freqs)
            max_rows = max(len(letter_freqs), len(best_words))

            for i in range(max_rows):
                if i < len(letter_freqs):
                    letter, freq = letter_freqs[i]
                    percent = freq / total_freq * 100
                    text = f"{letter.upper()}   ({percent:.1f}%)"
                    tb.Label(
                        left_frame,
                        text=text,
                        font=("Segoe UI", 12, "bold"),
                        anchor="center",
                        justify="center",
                        bootstyle="info-inverse",
                    ).grid(row=i, column=0, sticky="ew", padx=10, pady=2)

                if i < len(best_words):
                    word, score = best_words[i]
                    text = f"{word.upper()}   ({score})"
                    tb.Label(
                        right_frame,
                        text=text,
                        font=("Segoe UI", 12, "bold"),
                        anchor="center",
                        justify="center",
                        style="Success-Inverse.TLabel",
                    ).grid(row=i, column=0, sticky="ew", padx=10, pady=2)

        threading.Thread(target=worker, daemon=True).start()

    def reset_inputs(self):
        """
        Resets all input entries to empty strings and the default entry style.

        This method is used when the user clicks the "Reset" button. It clears all
        input entries and resets their style to the default style. If a result
        window exists, it is closed and the main application window is centered
        on the screen.

        :return: None
        """
        for entry in self.get_all_entries():
            entry.delete(0, END)
            entry.configure(style="Default.TEntry")
        # Close previous result window if exists
        if hasattr(self, "result_window") and self.result_window is not None and self.result_window.winfo_exists():
            self.result_window.destroy()
            self.center_window()

    def setup_layout(self):
        """
        Sets up the main window layout.

        This method configures the main window's rows and columns to have a
        specific weight, and creates two frames inside the main window: one
        for the left side and one for the right side. The left frame is used
        for the main input and the right frame is used for the buttons.

        :return: None
        """
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.left_frame = tb.Frame(self.master)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(2, 10))

        self.right_frame = tb.Frame(self.master)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.setup_left_frame()
        self.setup_right_frame()

    def setup_left_frame(self):
        """
        Sets up the left frame's layout.

        This method creates the left frame's content, which includes the input
        entries for the known positions, unknown positions, and excluded letters.
        Each input is a row of 5 entries, which are created using
        `create_entry_row` method.

        :return: None
        """

        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=1)

        # Known positions
        known_frame = tb.Labelframe(self.left_frame, text="   Known Positions   ")
        known_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        for i in range(5):
            known_frame.columnconfigure(i, weight=1)
        self.known_inputs = self.create_entry_row(known_frame, 5)

        # Unknown positions
        self.unknown_inputs = []
        unknown_frame = tb.Labelframe(self.left_frame, text="   Unknown Positions   ")
        unknown_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        for i in range(5):
            unknown_frame.columnconfigure(i, weight=1)
        for row_idx in range(3):
            row_inputs = self.create_entry_row(unknown_frame, 5, row=row_idx)
            self.unknown_inputs.append(row_inputs)

        # Excluded letters grid
        self.excluded_inputs = []
        excluded_frame = tb.Labelframe(self.left_frame, text="   Not Included   ")
        excluded_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        for i in range(5):
            excluded_frame.columnconfigure(i, weight=1)
        for row_idx in range(4):
            row_inputs = self.create_entry_row(excluded_frame, 5, row=row_idx)
            self.excluded_inputs.append(row_inputs)

    def setup_right_frame(self):
        """
        This method creates the right frame's content, which includes the buttons for
        submitting the query, downloading the dictionary, toggling dark mode, and
        resetting all inputs.

        :return: None
        """
        # Use grid manager for better layout control
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(3, weight=1)  # space above the reset button

        self.submit_button = tb.Button(
            self.right_frame,
            text="Submit Query",
            bootstyle=PRIMARY,
            command=self.submit_query,
        )
        self.submit_button.grid(row=0, column=0, sticky="ew", pady=(12, 5), ipady=5)

        self.dict_button = tb.Button(
            self.right_frame,
            text="Get Dictionary",
            bootstyle=INFO,
            command=self.get_dictionary,
        )
        self.dict_button.grid(row=1, column=0, sticky="ew", pady=5, ipady=5)

        self.dark_mode_var = tb.BooleanVar(value=False)

        self.dark_toggle = tb.Checkbutton(
            self.right_frame,
            text="Dark Mode",
            variable=self.dark_mode_var,
            bootstyle="square-toggle",
            command=self.toggle_theme,
        )
        self.dark_toggle.grid(row=2, column=0, sticky="ew", pady=10)

        self.howtoplay_button = tb.Button(
            self.right_frame,
            text="How To Play",
            bootstyle=SUCCESS,
            command=self.how_to_play,
        )
        self.howtoplay_button.grid(row=5, column=0, sticky="ew,s", pady=5, ipady=5)

        self.bestwords_button = tb.Button(
            self.right_frame,
            text="Best Words To Start",
            bootstyle=DANGER,
            command=self.best_words,
        )
        self.bestwords_button.grid(row=4, column=0, sticky="ew,s", pady=5, ipady=5)

        self.reset_button = tb.Button(
            self.right_frame,
            text="Reset All",
            bootstyle=WARNING,
            command=self.reset_inputs,
        )
        self.reset_button.grid(row=6, column=0, sticky="ew,s", pady=5, ipady=5)

    def get_all_entries(self):
        """
        Returns a list of all the input entries in the application window.

        :return: List of all input entries in the application window
        """
        entries = []
        entries.extend(self.known_inputs)
        for row in self.unknown_inputs:
            entries.extend(row)
        for row in self.excluded_inputs:
            entries.extend(row)
        return entries

    def store_last_value(self, event):
        """
        Stores the value of the last focused input entry in the application
        window. This is necessary for the reset button to clear the input
        entries to their original value.

        :param event: The event that triggered this function to be called
        :return: None
        """
        self.last_entry_value = event.widget.get()

    def create_entry_row(self, parent, num_entries, row=0):
        """
        Creates a row of input entries in the given parent widget.

        :param parent: The parent widget to create the entries in
        :param num_entries: The number of entries to create
        :param row: The row number to place the entries in (default=0)
        :return: A list of the created entries
        """
        entries = []
        vcmd = (self.register(self.validate_input), "%P")
        for idx in range(num_entries):
            sv = StringVar()
            entry = tb.Entry(
                parent,
                textvariable=sv,
                width=2,
                font=("Arial", 30, "bold"),
                justify="center",
                validate="key",
                validatecommand=vcmd,
                style="Default.TEntry",
            )
            entry.grid(row=row, column=idx, padx=4, pady=4, sticky="nsew")
            parent.columnconfigure(idx, weight=1)
            entry.bind("<KeyPress>", self.store_last_value)
            entry.bind("<KeyRelease>", self.handle_focus)

            entries.append(entry)
        return entries

    def validate_input(self, proposed_value):
        """
        Validates the input in an entry widget.

        The input is considered valid if it is an empty string, a single
        ASCII letter, or a single non-ASCII letter that can be converted to
        uppercase.

        :param proposed_value: The value to be validated
        :return: True if the input is valid, False otherwise
        """
        if not proposed_value:
            return True

        if len(proposed_value) > 1:
            return False

        char = proposed_value

        if not char.isalpha() or not char.isascii():
            return False

        self.after_idle(self.force_upper)
        return True

    def force_upper(self):
        """
        Converts the text in the currently focused entry to uppercase.

        This method checks if the currently focused widget is an entry
        field. If it is, it retrieves the current text, converts it to
        uppercase, and updates the entry with the uppercase text.
        """

        focused = self.focus_get()
        if focused and isinstance(focused, tb.Entry):
            value = focused.get()
            focused.delete(0, END)
            focused.insert(0, value.upper())

    def handle_focus(self, event):
        """
        Handles key press events in the input entries.

        This method handles the "Return", "Delete", "BackSpace", and any
        alphanumeric key presses in the input entries. The method is
        responsible for moving the focus to the next or previous entry based
        on the key pressed, setting the style of the entry based on whether
        it contains any text, and deleting any text in the entry if the
        "Delete" key is pressed.

        :param event: The key press event
        :return: None
        """
        widget = event.widget
        key = event.keysym
        char = event.char

        entries_list = self.get_all_entries()
        idx = entries_list.index(widget)

        if key == "Return":
            if idx + 1 < len(entries_list):
                entries_list[idx + 1].focus_set()
            return

        if key == "Delete":
            widget.delete(0, END)
            widget.configure(style="Default.TEntry")
            if idx > 0:
                entries_list[idx - 1].focus_set()
            return

        if key == "BackSpace":
            if widget.get():
                widget.delete(0, END)
            widget.configure(style="Default.TEntry")
            self.last_entry_value = widget.get()
            if not widget.get() and self.last_entry_value == "":
                if idx > 0:
                    entries_list[idx - 1].focus_set()
            return

        if char.isalpha() and char.isascii():
            if len(widget.get()) == 1:
                widget.delete(0, END)
                widget.insert(0, char.upper())

                if widget in self.known_inputs:
                    widget.configure(style="Known.TEntry")
                elif any(widget in row for row in self.unknown_inputs):
                    widget.configure(style="Unknown.TEntry")
                else:
                    widget.configure(style="Excluded.TEntry")

                if idx + 1 < len(entries_list):
                    entries_list[idx + 1].focus_set()
                return

        if widget.get() and idx + 1 < len(entries_list):
            entries_list[idx + 1].focus_set()

        value = widget.get()
        if widget in self.known_inputs:
            new_style = "Known.TEntry" if value else "Default.TEntry"
        elif any(widget in row for row in self.unknown_inputs):
            new_style = "Unknown.TEntry" if value else "Default.TEntry"
        else:
            new_style = "Excluded.TEntry" if value else "Default.TEntry"

        widget.configure(style=new_style)

    def get_dictionary(self):
        """Downloads the Wordle dictionary and filters it to 5-letter words if not already done.

        This method checks if the Wordle dictionary already exists. If it does, it
        asks the user if they want to re-download it. If yes, it downloads it and
        filters it to 5-letter words. If no, it filters the existing dictionary
        if it has not already been filtered. If the dictionary does not exist, it
        downloads it and filters it to 5-letter words.

        The method runs in a separate thread to not block the main thread.
        """

        def worker():
            dict_path = "dict/words.txt"
            filtered_path = "dict/words_filtered.txt"
            dict_url = "https://raw.githubusercontent.com/tabatkins/wordle-list/refs/heads/main/words"

            if os.path.exists(dict_path):
                result = messagebox.askyesno(
                    "Dictionary Exists", "words.txt already exists.\nDo you want to re-download it?"
                )
                if result:
                    downloader = DictionaryDownloader(dict_url)
                    downloader.download()
                    wf = WordFilter(dict_path, filtered_path)
                    wf.filter_and_save()
                    self.after(
                        0, lambda: messagebox.showinfo("Done", "Dictionary downloaded and filtered successfully.")
                    )
                else:
                    if not os.path.exists(filtered_path):
                        wf = WordFilter(dict_path, filtered_path)
                        wf.filter_and_save()
                        self.after(0, lambda: messagebox.showinfo("Done", "Filtered dictionary created successfully."))
                    else:
                        self.after(0, lambda: messagebox.showinfo("Done", "Filtered dictionary already exists."))
            else:
                downloader = DictionaryDownloader(dict_url)
                downloader.download()
                wf = WordFilter(dict_path, filtered_path)
                wf.filter_and_save()
                self.after(0, lambda: messagebox.showinfo("Done", "Dictionary downloaded and filtered successfully."))

        threading.Thread(target=worker, daemon=True).start()

    def submit_query(self):
        """
        Handles the "Submit Query" button click event.

        This method filters the words in the dictionary based on the inputs
        provided by the user and shows the results in a message box. It also
        checks for any conflicts in the user's inputs and shows an error message
        if there are any conflicts.

        The method runs in a separate thread to not block the main thread.
        """

        def worker():
            if self.words is None:
                file_path = "dict/words_filtered.txt"
                if not os.path.exists(file_path):
                    self.after(
                        0,
                        lambda: messagebox.showerror(
                            "File Not Found", "words_filtered.txt not found!\nPlease click 'Get Dictionary' first."
                        ),
                    )
                    return

                with open(file_path, "r", encoding="utf-8") as f:
                    self.words = tuple(line.strip() for line in f if line.strip())

            if self.analyzer is None:
                self.analyzer = LetterFrequencyAnalyzer()
                self.analyzer.analyze()

            if all(not entry.get().strip() for entry in self.get_all_entries()):
                self.after(
                    0, lambda: messagebox.showinfo("No Input", "Please enter at least one letter before submitting.")
                )
                return

            known_pattern = [entry.get().lower() for entry in self.known_inputs]
            unknowns = []
            for row in self.unknown_inputs:
                for idx, entry in enumerate(row):
                    value = entry.get().lower()
                    if value:
                        unknowns.append((idx, value))

            excluded_letters = set()
            for row in self.excluded_inputs:
                for entry in row:
                    value = entry.get().lower()
                    if value:
                        excluded_letters.add(value)

            # Check for overlap
            known_letters = {ch for ch in known_pattern if ch}
            unknown_letters = {v for _, v in unknowns}
            overlap = (known_letters | unknown_letters) & excluded_letters
            if overlap:
                self.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Input Conflict",
                        f"Conflict: letters {', '.join(overlap).upper()} "
                        f"are both included and excluded.\nPlease correct your inputs.",
                    ),
                )
                return

            # Use solver
            solver = WordleSolver(self.words)
            candidates = solver.filter_candidates(known_pattern, unknowns, excluded_letters)

            if len(candidates) == 0:
                self.after(
                    0, lambda: messagebox.showinfo("No Results", "No possible words found.\nPlease check your inputs.")
                )
                return

            if len(candidates) > 300:
                messagebox.showwarning(
                    "Too Many Results",
                    f"{len(candidates)} words matched your criteria.\n"
                    "Only the top 300 will be shown.\n\n"
                    "For better results, please adjust your input constraints and try again.",
                )

            ranked_candidates = self.analyzer.suggest_best_words(word_list=candidates, top_n=300)

            self.after(0, lambda: self.show_results(ranked_candidates))

        threading.Thread(target=worker, daemon=True).start()

    def show_results(self, candidates):
        if hasattr(self, "result_window") and self.result_window is not None and self.result_window.winfo_exists():
            self.result_window.destroy()

        self.result_window = tb.Toplevel(self)
        num_results = len(candidates)
        title = f"Possible Answers ({num_results} found)" if num_results != 1 else "Possible Answer (1 found)"

        self.result_window.title(title)
        self.result_window.geometry("450x650")
        self.result_window.withdraw()
        self.result_window.iconphoto(False, self.icon)
        self.result_window.resizable(False, False)
        self.result_window.focus_set()

        self.result_window.columnconfigure(0, weight=1)
        self.result_window.rowconfigure(0, weight=1)

        labelframe = tb.Labelframe(
            self.result_window,
            text=(
                f"   Top {num_results} Answers (Ranked By Letter Frequency)   "
                if num_results != 1
                else "   Best Possible Answer   "
            ),
        )
        labelframe.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        labelframe.columnconfigure(0, weight=1)
        labelframe.rowconfigure(0, weight=1)

        container = tb.Frame(labelframe)
        container.grid(row=0, column=0, sticky="nsew")
        labelframe.columnconfigure(0, weight=1)
        labelframe.rowconfigure(0, weight=1)

        canvas = tb.Canvas(container)
        scrollbar = tb.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        scrollable_frame = tb.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Identify highest score and how many words share it
        if candidates:
            max_score = candidates[0][1]
            top_words = [word for word, score in candidates if score == max_score]
            top_style = "OutlineSuccess.TButton" if len(top_words) == 1 else "OutlineMidSuccess.TButton"
        else:
            top_words = []
            top_style = "OutlinePrimaryBold.TButton"

        max_cols = 3
        for idx, (word, score) in enumerate(candidates):
            r, c = divmod(idx, max_cols)
            style = top_style if score == max_score else "OutlinePrimaryBold.TButton"

            btn = tb.Button(
                scrollable_frame,
                text=word.upper(),
                width=9,
                style=style,
                cursor="arrow",
                takefocus=False,
            )
            btn.grid(row=r, column=c, padx=8, pady=8)
            scrollable_frame.columnconfigure(c, weight=0)

            Hovertip(btn, f"Score: {score}", hover_delay=400)

        self.center_main_and_result(450, 650)
        self.result_window.deiconify()

        # Mousewheel scrolling
        def _on_mousewheel(event):
            """
            Handles mouse wheel scrolling for Windows and Linux systems.

            This function allows scrolling within a canvas widget using the mouse wheel.
            It calculates the total content height and compares it with the visible
            height of the canvas. If the content is larger than the visible area, it
            scrolls the canvas vertically based on the scroll event delta.

            :param event: The mouse wheel event containing the scroll delta.
            """

            content_height = canvas.bbox("all")[3]
            visible_height = canvas.winfo_height()
            if content_height > visible_height:
                canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        def _on_mousewheel_mac(event):
            """
            Handles mouse wheel scrolling for macOS systems.

            This function enables vertical scrolling within a canvas widget using the mouse wheel.
            It calculates the content height and compares it with the visible height of the canvas.
            If the content exceeds the visible area, it scrolls the canvas vertically based on the
            scroll event delta, adjusting for macOS-specific event handling.

            :param event: The mouse wheel event containing the scroll delta.
            """

            content_height = canvas.bbox("all")[3]
            visible_height = canvas.winfo_height()
            if content_height > visible_height:
                canvas.yview_scroll(-1 * int(event.delta), "units")

        system = self.result_window.tk.call("tk", "windowingsystem")
        if system == "aqua":
            self.result_window.bind_all("<MouseWheel>", _on_mousewheel_mac)
        else:
            self.result_window.bind_all("<MouseWheel>", _on_mousewheel)

        # Optional: Unbind on window close to avoid affecting main window
        def on_close():
            """
            Unbinds the mouse wheel event and closes the result window when it is closed.

            This method is called when the result window is closed. It unbinds the
            mouse wheel event to prevent it from affecting the main window and then
            closes the result window. Finally, it centers the main window on the screen.

            :return: None
            """
            self.result_window.unbind_all("<MouseWheel>")
            self.result_window.destroy()
            self.center_window()

        self.result_window.protocol("WM_DELETE_WINDOW", on_close)


if __name__ == "__main__":
    app = WordleSolverApp()
    app.mainloop()
