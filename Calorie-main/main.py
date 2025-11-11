"""!
@file main.py
@brief A simple Tkinter GUI application.
@author Jules
"""

import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    """!
    @brief The main application class.
    This class creates a simple GUI with a label, an entry, and a button.
    """
    def __init__(self):
        """!
        @brief The constructor for the App class.
        Initializes the main window and its widgets.
        """
        super().__init__()

        self.title("Simple GUI")
        self.geometry("300x150")

        # Style configuration
        style = ttk.Style(self)
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12, "bold"))
        style.configure("TEntry", font=("Helvetica", 12))

        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Widgets
        self.label = ttk.Label(main_frame, text="Enter a message:")
        self.label.pack(pady=5)

        self.entry = ttk.Entry(main_frame, width=30)
        self.entry.pack(pady=5)

        self.button = ttk.Button(main_frame, text="Update Message", command=self.update_message)
        self.button.pack(pady=10)

    def update_message(self):
        """!
        @brief Updates the label text.
        This function is called when the button is clicked. It gets the text
        from the entry widget and updates the label's text.
        """
        new_message = self.entry.get()
        if new_message:
            self.label.config(text=f"Message: {new_message}")
        else:
            self.label.config(text="Please enter a message.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
