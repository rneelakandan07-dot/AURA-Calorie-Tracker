import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date
from ttkthemes import ThemedTk

# --- CLASS DEFINITIONS ---

class SummaryFrame(ttk.Frame):
    """
    A ttk.Frame that displays a summary of the user's daily nutritional intake.

    This frame shows the total calories consumed against the daily goal, a progress bar
    representing the calorie intake, and a breakdown of protein, carbohydrates, and fat.
    The summary is automatically updated when the application starts and whenever a new
    food item is logged.

    Attributes:
        calories_var (tk.StringVar): Holds the formatted string for calorie intake.
        protein_var (tk.StringVar): Holds the formatted string for protein intake.
        carbs_var (tk.StringVar): Holds the formatted string for carbohydrate intake.
        fat_var (tk.StringVar): Holds the formatted string for fat intake.
        progress_var (tk.DoubleVar): Holds the value for the calorie progress bar.
    """
    def __init__(self, container):
        super().__init__(container)
        self.calories_var = tk.StringVar(value='0 / 2000 kcal')
        self.protein_var = tk.StringVar(value='Protein: 0g')
        self.carbs_var = tk.StringVar(value='Carbs: 0g')
        self.fat_var = tk.StringVar(value='Fat: 0g')
        self.progress_var = tk.DoubleVar(value=0.0)
        ttk.Label(self, textvariable=self.calories_var, font=("Segoe UI", 16)).pack(pady=5)
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=250, mode='determinate', variable=self.progress_var)
        self.progress_bar.pack(pady=10, padx=10, fill='x')
        macro_frame = ttk.Frame(self)
        macro_frame.pack(pady=5, padx=10, fill='x')
        ttk.Label(macro_frame, textvariable=self.protein_var).pack(side='left', expand=True)
        ttk.Label(macro_frame, textvariable=self.carbs_var).pack(side='left', expand=True)
        ttk.Label(macro_frame, textvariable=self.fat_var).pack(side='left', expand=True)
        self.update_summary()

    def update_summary(self):
        """
        Fetches and displays the latest nutritional summary from the database.

        This method connects to the database, retrieves the user's daily calorie goal,
        and calculates the total calories, protein, carbohydrates, and fat consumed
        for the current day. It then updates the corresponding UI elements with the
        new values and adjusts the progress bar accordingly.
        """
        conn = None
        try:
            conn = sqlite3.connect('calorie_tracker.db'); cursor = conn.cursor(); today = date.today().isoformat(); user_id = 1
            cursor.execute("SELECT daily_calorie_goal FROM users WHERE user_id = ?", (user_id,)); result = cursor.fetchone()
            calorie_goal = result[0] if result else 2000
            cursor.execute('SELECT SUM(calories), SUM(protein_g), SUM(carbs_g), SUM(fat_g) FROM food_log WHERE user_id = ? AND entry_date = ?', (user_id, today))
            summary = cursor.fetchone()
            total_cal, total_pro, total_carb, total_fat = (summary[0] or 0, summary[1] or 0, summary[2] or 0, summary[3] or 0)
            self.calories_var.set(f'{total_cal:.0f} / {calorie_goal} kcal')
            self.protein_var.set(f'Protein: {total_pro:.1f}g'); self.carbs_var.set(f'Carbs: {total_carb:.1f}g'); self.fat_var.set(f'Fat: {total_fat:.1f}g')
            self.progress_var.set((total_cal / calorie_goal) * 100)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not update summary: {e}")
        finally:
            if conn: conn.close()

class AddNewFoodWindow(tk.Toplevel):
    """
    A Toplevel window for adding a new food item to the user's library.

    This window provides a form with entry fields for the food's name, calories,
    protein, carbohydrates, and fat. When the user saves the new food, it is
    added to the 'food_library' table and immediately logged for the current day
    in the 'food_log' table.

    Attributes:
        log_frame (DailyLogFrame): A reference to the daily log frame to refresh it.
        summary_frame (SummaryFrame): A reference to the summary frame to update it.
    """
    def __init__(self, master, log_frame, summary_frame):
        super().__init__(master)
        self.log_frame = log_frame; self.summary_frame = summary_frame
        self.title("Add New Food"); self.geometry("350x250")
        self.frame = ttk.Frame(self, padding="10"); self.frame.pack(fill="both", expand=True)

        ttk.Label(self.frame, text="Food Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.food_name_entry = ttk.Entry(self.frame); self.food_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame, text="Calories (per serving):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.calories_entry = ttk.Entry(self.frame); self.calories_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame, text="Protein (g):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.protein_entry = ttk.Entry(self.frame); self.protein_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame, text="Carbs (g):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.carbs_entry = ttk.Entry(self.frame); self.carbs_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame, text="Fat (g):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.fat_entry = ttk.Entry(self.frame); self.fat_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self.frame, text="Save Food", command=self.save_food).grid(row=5, column=1, padx=5, pady=10, sticky="e")

    def save_food(self):
        """
        Validates the user's input and saves the new food to the database.

        This method retrieves the data from the entry fields, validates that the
        required fields are filled and that the numerical fields contain valid
        numbers, and then inserts the new food item into both the 'food_library'
        and 'food_log' tables. After a successful save, it refreshes the daily
        log and summary frames and closes the window.
        """
        food_name=self.food_name_entry.get(); calories=self.calories_entry.get()
        protein=self.protein_entry.get() or '0'; carbs=self.carbs_entry.get() or '0'; fat=self.fat_entry.get() or '0'

        if not food_name or not calories:
            messagebox.showerror("Input Error", "Food name and calories are required.", parent=self); return
        try:
            base_calories=int(calories); base_protein=float(protein); base_carbs=float(carbs); base_fat=float(fat)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.", parent=self); return

        conn = None
        try:
            conn = sqlite3.connect('calorie_tracker.db'); cursor = conn.cursor(); user_id=1; today=date.today().isoformat()
            cursor.execute('INSERT OR IGNORE INTO food_library (user_id, food_name, calories, protein_g, carbs_g, fat_g) VALUES (?, ?, ?, ?, ?, ?)',
                           (user_id, food_name, base_calories, base_protein, base_carbs, base_fat))
            cursor.execute('INSERT INTO food_log (user_id, entry_date, quantity, food_name, calories, protein_g, carbs_g, fat_g) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                           (user_id, today, 1, food_name, base_calories, base_protein, base_carbs, base_fat))
            conn.commit()
            self.log_frame.load_log(); self.summary_frame.update_summary()
            self.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=self)
        finally:
            if conn: conn.close()

class DataEntryFrame(ttk.Frame):
    """
    A ttk.Frame for searching and logging food items from the user's library.

    This frame includes a search bar to find food items, a field for quantity,
    and buttons to add a selected food to the daily log or to open the window
    for adding a new food item. The search results are displayed in a listbox.

    Attributes:
        log_frame (DailyLogFrame): A reference to the daily log frame to refresh it.
        summary_frame (SummaryFrame): A reference to the summary frame to update it.
    """
    def __init__(self, container, log_frame, summary_frame):
        super().__init__(container)
        self.log_frame = log_frame; self.summary_frame = summary_frame
        self.columnconfigure(0, weight=3); self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Search for Food:").grid(row=0, column=0, padx=5, pady=(0,5), sticky="w")
        ttk.Label(self, text="Qty:").grid(row=0, column=1, padx=5, pady=(0,5), sticky="w")

        self.search_var = tk.StringVar(); self.search_var.trace_add("write", self.update_search_results)
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = ttk.Entry(self, textvariable=self.quantity_var, width=5)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.results_listbox = tk.Listbox(self, height=5)
        self.results_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Button(self, text="Add Selected", command=self.add_selected_food).grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        ttk.Button(self, text="Add New Food", command=self.open_new_food_window).grid(row=3, column=1, padx=5, pady=10, sticky="ew")

    def update_search_results(self, *args):
        """
        Updates the search results listbox as the user types in the search bar.

        This method is triggered whenever the content of the search entry changes.
        It queries the 'food_library' table for food names that match the search
        term and displays the results in the listbox.
        """
        search_term = self.search_var.get(); self.results_listbox.delete(0, 'end')
        if not search_term: return
        conn = None
        try:
            conn = sqlite3.connect('calorie_tracker.db'); cursor = conn.cursor()
            cursor.execute("SELECT food_name FROM food_library WHERE user_id = 1 AND food_name LIKE ?", (f'{search_term}%',))
            for row in cursor.fetchall():
                self.results_listbox.insert('end', row[0])
        except sqlite3.Error as e:
            print(f"Database search error: {e}")
        finally:
            if conn: conn.close()

    def add_selected_food(self):
        """
        Adds the selected food item from the search results to the daily log.

        This method retrieves the selected food and the specified quantity,
        calculates the nutritional values based on the quantity, and inserts
        a new record into the 'food_log' table. It then refreshes the daily
        log and summary frames.
        """
        try:
            quantity = float(self.quantity_var.get())
            if quantity <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid, positive quantity.")
            return

        indices = self.results_listbox.curselection()
        if not indices:
            messagebox.showwarning("No Selection", "Please select a food from the list.")
            return

        food_name = self.results_listbox.get(indices[0])
        conn = None
        try:
            conn = sqlite3.connect('calorie_tracker.db'); cursor = conn.cursor()
            cursor.execute("SELECT * FROM food_library WHERE user_id = 1 AND food_name = ?", (food_name,))
            food_data = cursor.fetchone()

            if not food_data:
                messagebox.showerror("Error", "Could not find details."); return

            _, user_id, name, base_cal, base_pro, base_carb, base_fat = food_data
            final_cal = (base_cal or 0) * quantity
            final_pro = (base_pro or 0) * quantity
            final_carb = (base_carb or 0) * quantity
            final_fat = (base_fat or 0) * quantity

            today = date.today().isoformat()
            cursor.execute('''INSERT INTO food_log (user_id, entry_date, quantity, food_name, calories, protein_g, carbs_g, fat_g)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (user_id, today, quantity, name, final_cal, final_pro, final_carb, final_fat))
            conn.commit()

            self.log_frame.load_log(); self.summary_frame.update_summary()
            self.search_var.set(""); self.quantity_var.set("1")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding entry: {e}")
        finally:
            if conn: conn.close()

    def open_new_food_window(self):
        """Opens the 'Add New Food' window as a modal dialog."""
        new_window = AddNewFoodWindow(self.master, self.log_frame, self.summary_frame)
        new_window.transient(self.master); new_window.grab_set()
        self.master.wait_window(new_window)

class DailyLogFrame(ttk.Frame):
    """
    A ttk.Frame that displays the food items logged for the current day.

    This frame uses a ttk.Treeview widget to present the logged food items in a
    tabular format, with columns for quantity, food name, calories, protein,
    carbohydrates, and fat. The log is automatically loaded when the application
    starts and is refreshed whenever a new food item is added.
    """
    def __init__(self, container):
        super().__init__(container)
        columns = ('quantity', 'food_name', 'calories', 'protein_g', 'carbs_g', 'fat_g')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', selectmode="browse")

        self.tree.heading('quantity', text='Qty'); self.tree.heading('food_name', text='Food')
        self.tree.heading('calories', text='Calories'); self.tree.heading('protein_g', text='Protein (g)')
        self.tree.heading('carbs_g', text='Carbs (g)'); self.tree.heading('fat_g', text='Fat (g)')

        self.tree.column('quantity', width=40, anchor='center'); self.tree.column('food_name', width=200)
        self.tree.column('calories', width=80, anchor='center'); self.tree.column('protein_g', width=80, anchor='center')
        self.tree.column('carbs_g', width=80, anchor='center'); self.tree.column('fat_g', width=80, anchor='center')

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew'); scrollbar.grid(row=0, column=1, sticky='ns')
        self.grid_rowconfigure(0, weight=1); self.grid_columnconfigure(0, weight=1)
        self.load_log()

    def load_log(self):
        """
        Clears the current log and loads the food entries for the current day.

        This method connects to the database, fetches all food log entries for
        the current user and date, and populates the Treeview widget with this
        data.
        """
        for item in self.tree.get_children(): self.tree.delete(item)
        conn = None
        try:
            conn = sqlite3.connect('calorie_tracker.db'); cursor = conn.cursor(); today = date.today().isoformat()
            cursor.execute('SELECT quantity, food_name, calories, protein_g, carbs_g, fat_g FROM food_log WHERE user_id = 1 AND entry_date = ?', (today,))
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not load log: {e}")
        finally:
            if conn: conn.close()

# --- MAIN APPLICATION CLASS ---
class CalorieTrackerApp(ThemedTk):
    """
    The main application class for the Calorie Tracker.

    This class initializes the main application window, sets up the theme, and
    arranges the different frames (Summary, Data Entry, and Daily Log) within
    the main window. It serves as the root of the Tkinter application.
    """
    def __init__(self):
        super().__init__()

        self.set_theme("arc")

        self.title("Aura's Calorie Management System"); self.geometry("900x600"); self.minsize(700, 500)

        main_frame = ttk.Frame(self, padding="10 10 10 10"); main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1); main_frame.columnconfigure(1, weight=1); main_frame.rowconfigure(1, weight=1)

        log_container = ttk.LabelFrame(main_frame, text="Today's Log")
        entry_container = ttk.LabelFrame(main_frame, text="Log an Entry")
        summary_container = ttk.LabelFrame(main_frame, text="Daily Summary")

        log_container.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        entry_container.grid(row=0, column=1, padx=10, pady=10, sticky="new")
        summary_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.summary_frame = SummaryFrame(summary_container)
        self.daily_log_frame = DailyLogFrame(log_container)
        self.data_entry_frame = DataEntryFrame(entry_container, self.daily_log_frame, self.summary_frame)

        self.summary_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.daily_log_frame.pack(fill="both", expand=True)
        self.data_entry_frame.pack(fill="x")

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    app = CalorieTrackerApp()
    app.mainloop()