# Simple Python GUI Application

This project is a simple, modern-looking Graphical User Interface (GUI) application built with Python's Tkinter library and its themed widget set (ttk).

## How the Code Works

The application is contained within a single file, `main.py`. Below is a detailed breakdown of its structure and functionality.

### 1. Imports

```python
import tkinter as tk
from tkinter import ttk
```

-   `tkinter` is Python's standard GUI library. We import it with the alias `tk` for convenience.
-   `tkinter.ttk` is a submodule of Tkinter that provides access to the "themed widget" set, which gives the application a more modern look and feel across different operating systems.

### 2. The `App` Class

The entire application is encapsulated in a class called `App`, which inherits from `tk.Tk`, the main window class in Tkinter.

```python
class App(tk.Tk):
    # ...
```

#### The Constructor: `__init__(self)`

This method is called when a new `App` object is created. It's responsible for setting up the main window and all the widgets inside it.

```python
def __init__(self):
    super().__init__()

    self.title("Simple GUI")
    self.geometry("300x150")
```

-   `super().__init__()`: This calls the constructor of the parent class (`tk.Tk`) to initialize the main window.
-   `self.title(...)`: Sets the text that appears in the title bar of the window.
-   `self.geometry(...)`: Sets the initial size of the window (width x height).

#### Styling the Widgets

```python
style = ttk.Style(self)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12, "bold"))
style.configure("TEntry", font=("Helvetica", 12))
```

-   To create a consistent and modern look, we use a `ttk.Style` object.
-   `style.configure(...)` allows us to define the appearance for different widget types (`TLabel`, `TButton`, `TEntry`). Here, we are setting a clean "Helvetica" font for all our widgets.

#### Creating the Widgets

The widgets (label, entry box, and button) are placed inside a `ttk.Frame`, which acts as a container.

```python
main_frame = ttk.Frame(self, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)
```

-   The `padding="20"` adds some empty space around the inside of the frame.
-   `.pack(...)` is a geometry manager that places the frame inside the main window. `fill=tk.BOTH` and `expand=True` make the frame resize automatically if the window size changes.

The individual widgets are then created and packed into the `main_frame`:

```python
self.label = ttk.Label(main_frame, text="Enter a message:")
self.label.pack(pady=5)

self.entry = ttk.Entry(main_frame, width=30)
self.entry.pack(pady=5)

self.button = ttk.Button(main_frame, text="Update Message", command=self.update_message)
self.button.pack(pady=10)
```

-   `ttk.Label`: A simple text label.
-   `ttk.Entry`: A text box for user input.
-   `ttk.Button`: A clickable button. The `command=self.update_message` argument is crucial—it tells the button to call the `update_message` function when clicked.
-   `pady` adds a little vertical space between the widgets.

#### The `update_message(self)` Method

This function defines what happens when the button is clicked.

```python
def update_message(self):
    new_message = self.entry.get()
    if new_message:
        self.label.config(text=f"Message: {new_message}")
    else:
        self.label.config(text="Please enter a message.")
```

-   `self.entry.get()`: Retrieves the text currently in the entry box.
-   `self.label.config(...)`: Updates the text of the label to show the new message.

### 3. Running the Application

The final block of code is what actually starts the application.

```python
if __name__ == "__main__":
    app = App()
    app.mainloop()
```

-   `if __name__ == "__main__":` is a standard Python construct that ensures this code only runs when the script is executed directly.
-   `app = App()`: Creates an instance of our `App` class.
-   `app.mainloop()`: Starts the Tkinter event loop. This is what keeps the window open, listens for events (like button clicks), and keeps the application running until the user closes the window.

## How to Run the Application

To run this application, simply execute the `main.py` file from your terminal:

```bash
python main.py
```
