# Calorie Tracker

This is a simple calorie tracker application built with Python's Tkinter library. It allows users to log their daily food intake, track their calorie consumption, and manage a personal food library.

## Features

- **Daily Calorie Tracking:** Log food items and monitor your daily calorie and macronutrient intake.
- **Visual Progress:** A progress bar provides a quick visual of your calorie consumption against your daily goal.
- **Food Library:** Add new food items to your personal library for quick and easy logging.
- **Search Functionality:** Easily find food items in your library with a simple search feature.
- **Data Persistence:** Your food library and daily logs are stored in a local SQLite database.

## Getting Started

### Prerequisites

- Python 3.x
- pandas
- ttkthemes

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/calorie-tracker.git
   cd calorie-tracker/calorie_tracker
   ```

2. **Install the required packages:**
   ```bash
   pip install pandas ttkthemes
   ```

### Setup

1. **Initialize the database:**
   Run the `database_setup.py` script to create the `calorie_tracker.db` file and set up the necessary tables.
   ```bash
   python database_setup.py
   ```

2. **Populate the food library (optional):**
   The `import_data.py` script can be used to import a list of Indian food items from the included `Indian_Food_Nutrition_Processed.csv` file.
   ```bash
   python import_data.py
   ```

### Usage

Run the `main.py` script to launch the application.
```bash
python main.py
```

- **Log an Entry:**
  - Search for a food item in the "Search for Food" bar.
  - Select the desired food from the results.
  - Enter the quantity and click "Add Selected."

- **Add a New Food:**
  - Click the "Add New Food" button.
  - Fill in the details for the new food item and click "Save Food."
  - The new food will be added to your library and logged for the current day.
