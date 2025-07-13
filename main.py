from solver import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import StringVar


class WordleSolverApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Solver")

        self.style = tb.Style("litera")  # theme light
        self.is_dark_mode = False

        self.setup_layout()

    def setup_layout(self):

        self.master.columnconfigure(0, weight=3)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.left_frame = tb.Frame(self.master)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.right_frame = tb.Frame(self.master)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.setup_left_frame()
        self.setup_right_frame()

    def setup_left_frame(self):
        # Known positions
        known_frame = tb.Labelframe(self.left_frame, text="Known positions")
        known_frame.pack(fill=X, pady=5)
        self.known_inputs = self.create_entry_row(known_frame, 5)

        # Unknown positions
        unknown_frame = tb.Labelframe(self.left_frame, text="Unknown positions")
        unknown_frame.pack(fill=X, pady=5)
        self.unknown_inputs = self.create_entry_row(unknown_frame, 5)

        # Excluded letters grid
        excluded_frame = tb.Labelframe(self.left_frame, text="Excluded letters")
        excluded_frame.pack(fill=X, pady=5)
        self.excluded_inputs = []
        for _ in range(5):
            row_frame = tb.Frame(excluded_frame)
            row_frame.pack(fill=X, pady=2)
            row_inputs = self.create_entry_row(row_frame, 5)
            self.excluded_inputs.append(row_inputs)

    def setup_right_frame(self):
        self.submit_button = tb.Button(
            self.right_frame, text="Submit Query", bootstyle=PRIMARY, command=self.submit_query
        )
        self.submit_button.pack(fill=X, pady=5)

        self.dict_button = tb.Button(
            self.right_frame, text="Get Dictionary", bootstyle=INFO, command=self.get_dictionary
        )
        self.dict_button.pack(fill=X, pady=5)

        self.dark_mode_var = tb.BooleanVar(value=False)
        self.dark_switch = tb.Checkbutton(
            self.right_frame,
            text="Dark Mode",
            variable=self.dark_mode_var,
            command=self.toggle_theme,
            bootstyle="switch",
        )
        self.dark_switch.pack(fill=X, pady=10)

    def create_entry_row(self, parent, num_entries):
        entries = []
        for _ in range(num_entries):
            sv = StringVar()
            entry = tb.Entry(parent, textvariable=sv, width=2, justify="center")
            entry.pack(side=LEFT, padx=2)
            entry.bind("<KeyRelease>", self.limit_entry)
            entries.append(entry)
        return entries

    def limit_entry(self, event):
        widget = event.widget
        value = widget.get()

        if len(value) > 1:
            widget.delete(1, END)
        elif len(value) == 1 and not value.isalpha():
            widget.delete(0, END)
        elif len(value) == 1:
            widget.delete(0, END)
            widget.insert(0, value.upper())

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        new_theme = "darkly" if self.is_dark_mode else "litera"
        self.style.theme_use(new_theme)

    def submit_query(self):
        print("Submit Query clicked")

    def get_dictionary(self):
        print("Get Dictionary clicked")


if __name__ == "__main__":
    app = tb.Window(themename="litera")  # theme light
    WordleSolverApp(app)
    app.mainloop()
