from solver import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import StringVar


class WordleSolverApp(tb.Window):
    def __init__(self):
        self.current_theme = "darkly"  # dark theme by default
        super().__init__(themename=self.current_theme)

        self.style.configure("Default.TEntry", fieldbackground="#1e1e1e", foreground="#ffffff")
        self.style.configure("Known.TEntry", fieldbackground="#538d4e", foreground="#ffffff")
        self.style.configure("Unknown.TEntry", fieldbackground="#b59f3b", foreground="#ffffff")
        self.style.configure("Excluded.TEntry", fieldbackground="#3a3a3c", foreground="#ffffff")

        self.title("Wordle Solver")
        self.withdraw()
        self.minsize(400, 600)
        self.center_window()
        self.deiconify()
        self.last_entry_value = ""

        self.setup_layout()

    def center_window(self):
        self.update_idletasks()
        width = 400
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_layout(self):

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

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

    def get_all_entries(self):
        entries = []
        entries.extend(self.known_inputs)
        entries.extend(self.unknown_inputs)
        for row in self.excluded_inputs:
            entries.extend(row)
        return entries

    def store_last_value(self, event):
        self.last_entry_value = event.widget.get()

    def create_entry_row(self, parent, num_entries):
        entries = []
        vcmd = (self.register(self.validate_input), "%P")
        for _ in range(num_entries):
            sv = StringVar()
            entry = tb.Entry(
                parent,
                textvariable=sv,
                width=2,
                font=("Arial", 20, "bold"),
                justify="center",
                validate="key",
                validatecommand=vcmd,
                style="Default.TEntry",
            )
            entry.pack(side=LEFT, padx=4, pady=4, ipady=5)
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

        entries_list = self.get_all_entries()
        idx = entries_list.index(widget)

        if key == "Delete":
            widget.delete(0, END)
            widget.configure(style="Default.TEntry")
            if idx > 0:
                entries_list[idx - 1].focus_set()
            return

        if key == "BackSpace":
            if widget.get():
                widget.delete(0, END)
            # Always reset style after clear
            widget.configure(style="Default.TEntry")

            # Update last_entry_value so next Backspace works correctly
            self.last_entry_value = widget.get()

            if not widget.get() and self.last_entry_value == "":
                if idx > 0:
                    entries_list[idx - 1].focus_set()
            return

        if widget.get() and idx + 1 < len(entries_list):
            entries_list[idx + 1].focus_set()

        value = widget.get()
        if widget in self.known_inputs:
            new_style = "Known.TEntry" if value else "Default.TEntry"
        elif widget in self.unknown_inputs:
            new_style = "Unknown.TEntry" if value else "Default.TEntry"
        else:
            new_style = "Excluded.TEntry" if value else "Default.TEntry"

        widget.configure(style=new_style)

    def submit_query(self):
        print("Submit Query clicked")

    def get_dictionary(self):
        print("Get Dictionary clicked")


if __name__ == "__main__":
    app = WordleSolverApp()
    app.mainloop()
