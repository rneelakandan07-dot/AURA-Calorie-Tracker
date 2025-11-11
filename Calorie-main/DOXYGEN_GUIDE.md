# How to Create Code Documentation with Doxygen

This guide provides a step-by-step tutorial on using Doxygen to automatically generate professional-looking documentation for the Python GUI project. This documentation will include detailed information about classes and functions, as well as call graphs that visually represent how functions interact.

## What is Doxygen?

Doxygen is a powerful tool that scans your source code, reads specially-formatted comments, and generates a comprehensive documentation website (as well as other formats like PDF). It's a fantastic way to document a project for yourself, your team, and your professor.

## Prerequisites

Before you begin, you will need two key pieces of software:

1.  **Doxygen**: The documentation generator itself.
2.  **Graphviz**: A graph visualization tool that Doxygen uses to create diagrams, such as class hierarchies and call graphs.

---

### Step 1: Installation

You need to install both Doxygen and Graphviz. Here’s how to do it on common operating systems:

#### Windows
-   **Doxygen**: Download the installer from the [official Doxygen website](https://www.doxygen.nl/download.html).
-   **Graphviz**: Download the installer from the [official Graphviz website](https://graphviz.org/download/). **Important**: During installation, make sure to select the option "Add Graphviz to the system PATH".

#### macOS (using Homebrew)
If you don't have Homebrew, you can install it from [brew.sh](https://brew.sh/).
```bash
brew install doxygen
brew install graphviz
```

#### Linux (using apt - for Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install doxygen
sudo apt-get install graphviz
```

---

### Step 2: Create the Doxygen Configuration File

Doxygen is controlled by a configuration file, usually named `Doxyfile`.

1.  **Generate the file**: Open your terminal or command prompt, navigate to the root directory of your project, and run the following command:
    ```bash
    doxygen -g
    ```
    This will create a new file named `Doxyfile` in your project folder.

2.  **Edit the `Doxyfile`**: Open the `Doxyfile` in a text editor. You will need to change a few settings for a Python project. Use the search function (Ctrl+F) in your editor to find and modify these lines:

    -   **`PROJECT_NAME`**: Give your project a name.
        ```
        PROJECT_NAME           = "Python GUI Application"
        ```
    -   **`INPUT`**: Tell Doxygen where your source code is. For this project, it's just `main.py`.
        ```
        INPUT                  = .
        ```
        *(The `.` means the current directory)*

    -   **`OPTIMIZE_OUTPUT_FOR_C`**: Since this is Python, not C, turn this off.
        ```
        OPTIMIZE_OUTPUT_FOR_C  = NO
        ```

    -   **`OPTIMIZE_OUTPUT_JAVA_OR_IDL`**: This option works well for Python's object-oriented style.
        ```
        OPTIMIZE_OUTPUT_JAVA_OR_IDL = YES
        ```

    -   **`EXTRACT_ALL`**: This ensures Doxygen documents everything, even if it doesn't have special comments.
        ```
        EXTRACT_ALL            = YES
        ```

    -   **`RECURSIVE`**: Tells Doxygen to look for source files in subdirectories.
        ```
        RECURSIVE              = YES
        ```

    -   **Enable Call Graphs (using Graphviz)**: This is the most important part for visualizing how your code works.
        ```
        HAVE_DOT               = YES
        CALL_GRAPH             = YES
        CALLER_GRAPH           = YES
        ```

---

### Step 3: Run Doxygen to Generate Documentation

Once your `Doxyfile` is configured, generating the documentation is simple.

1.  Make sure you are in the project's root directory in your terminal.
2.  Run the following command:
    ```bash
    doxygen Doxyfile
    ```
    Doxygen will now scan your code and generate the documentation. By default, it will create a new folder named `html`.

---

### Step 4: View Your New Documentation

1.  Open the newly created `html` folder.
2.  Inside, you will find a file named `index.html`. Double-click this file to open it in your web browser.

You can now explore your documentation!
-   Click on the **"Classes"** tab to see a list of classes.
-   Click on the `App` class to see a detailed view of its methods (`__init__` and `update_message`).
-   When viewing a function, you will see **call graphs** and **caller graphs**, which show which functions are called by this function, and which functions call it.

That's it! You have successfully generated professional, interactive documentation for your Python project.
