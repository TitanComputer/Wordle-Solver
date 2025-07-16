from solver import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import StringVar
from tkinter import messagebox
import threading


class WordleSolverApp(tb.Window):
    def __init__(self):
        self.current_theme = "litera"  # light theme by default
        super().__init__(themename=self.current_theme)

        self.style.configure("Default.TEntry", fieldbackground="white", foreground="#000000")
        self.style.configure("Known.TEntry", fieldbackground="#6aaa64", foreground="#ffffff")
        self.style.configure("Unknown.TEntry", fieldbackground="#c9b458", foreground="#ffffff")
        self.style.configure("Excluded.TEntry", fieldbackground="#787c7e", foreground="#ffffff")
        self.apply_custom_styles()

        self.title("Wordle Solver")
        self.withdraw()
        self.minsize(550, 650)
        self.resizable(False, False)
        self.center_window()
        self.deiconify()
        self.last_entry_value = ""
        self.is_dark_mode = False
        self.words = None

        self.setup_layout()

    def apply_custom_styles(self):
        # Buttons
        self.style.configure("primary.TButton", font=("Arial", 16, "bold"))
        self.style.configure("info.TButton", font=("Arial", 16, "bold"))
        self.style.configure("warning.TButton", font=("Arial", 16, "bold"))
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

        # Checkbutton
        self.style.configure("Square.Toggle", font=("Arial", 12, "bold"))

    def toggle_theme(self):
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
                foreground="#66b2ff",  # رنگ نوشته روشن‌تر برای دارک مود
                background="#212529",  # پس‌زمینه تیره (مطابق dark theme)
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

        # Update all empty entries to Default style so background matches theme
        for entry in self.get_all_entries():
            if not entry.get():
                entry.configure(style="Default.TEntry")

    def center_window(self):
        self.update_idletasks()
        width = 550
        height = 650
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def reset_inputs(self):
        for entry in self.get_all_entries():
            entry.delete(0, END)
            entry.configure(style="Default.TEntry")
        # Close previous result window if exists
        if hasattr(self, "result_window") and self.result_window is not None and self.result_window.winfo_exists():
            self.result_window.destroy()

    def setup_layout(self):

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

        self.reset_button = tb.Button(
            self.right_frame,
            text="Reset All",
            bootstyle=WARNING,
            command=self.reset_inputs,
        )
        self.reset_button.grid(row=4, column=0, sticky="ew,s", pady=5, ipady=5)

    def get_all_entries(self):
        entries = []
        entries.extend(self.known_inputs)
        for row in self.unknown_inputs:
            entries.extend(row)
        for row in self.excluded_inputs:
            entries.extend(row)
        return entries

    def store_last_value(self, event):
        self.last_entry_value = event.widget.get()

    def create_entry_row(self, parent, num_entries, row=0):
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
        focused = self.focus_get()
        if focused and isinstance(focused, tb.Entry):
            value = focused.get()
            focused.delete(0, END)
            focused.insert(0, value.upper())

    def handle_focus(self, event):
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
                if (
                    hasattr(self, "result_window")
                    and self.result_window is not None
                    and self.result_window.winfo_exists()
                ):
                    self.result_window.destroy()
                self.after(
                    0, lambda: messagebox.showinfo("No Results", "No possible words found.\nPlease check your inputs.")
                )
                return

            if len(candidates) > 240:
                if (
                    hasattr(self, "result_window")
                    and self.result_window is not None
                    and self.result_window.winfo_exists()
                ):
                    self.result_window.destroy()
                self.after(
                    0,
                    lambda: messagebox.showwarning(
                        "Too Many Results", "Too many possible words found (>240).\nPlease refine your inputs."
                    ),
                )
                return

            self.after(0, lambda: self.show_results(candidates))

        threading.Thread(target=worker, daemon=True).start()

    def show_results(self, candidates):
        if hasattr(self, "result_window") and self.result_window is not None and self.result_window.winfo_exists():
            self.result_window.destroy()

        self.result_window = tb.Toplevel(self)
        num_results = len(candidates)
        title = f"Possible Answers ({num_results} found)" if num_results != 1 else "Possible Answer (1 found)"
        self.result_window.title(title)

        self.result_window.geometry("450x650")
        self.result_window.resizable(False, False)
        self.result_window.focus_set()

        self.result_window.columnconfigure(0, weight=1)
        self.result_window.rowconfigure(0, weight=1)

        labelframe = tb.Labelframe(self.result_window, text="   Possible Answers   ")
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

        max_cols = 3
        for idx, word in enumerate(candidates):
            r, c = divmod(idx, max_cols)
            btn = tb.Button(
                scrollable_frame,
                text=word.upper(),
                width=9,
                style="OutlinePrimaryBold.TButton",
                cursor="arrow",
                takefocus=False,
            )

            btn.grid(row=r, column=c, padx=8, pady=8)
            scrollable_frame.columnconfigure(c, weight=0)

        # Mousewheel scrolling
        def _on_mousewheel(event):
            content_height = canvas.bbox("all")[3]
            visible_height = canvas.winfo_height()
            if content_height > visible_height:
                canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        def _on_mousewheel_mac(event):
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
            self.result_window.unbind_all("<MouseWheel>")
            self.result_window.destroy()

        self.result_window.protocol("WM_DELETE_WINDOW", on_close)


if __name__ == "__main__":
    app = WordleSolverApp()
    app.mainloop()
