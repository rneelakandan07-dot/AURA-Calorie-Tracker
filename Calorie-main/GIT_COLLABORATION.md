# How to Manage a Collaborative Git Commit History

When working on a project with a teammate, it's important that the commit history accurately reflects who did what. This guide will show you how to make commits under different names, creating a clear and collaborative history for your professor to see.

Since you and your teammate are working from the same repository, you will need to change the "author" information for each commit you make.

---

## The Concept: Author vs. Committer

Git tracks two pieces of information for every commit:

-   **Author**: The person who originally wrote the code.
-   **Committer**: The person who last applied the commit (this is usually the same as the author).

For your purposes, you will be changing the **author** for each commit to switch between yourself and your teammate.

---

### Step 1: Making a Commit as the First Person (Yourself)

Let's assume your name is "Student One" and your email is "student.one@example.com".

1.  **Configure your details**: Before your first commit, set your author information. This only needs to be done once per repository unless you change it.
    ```bash
    git config user.name "Student One"
    git config user.email "student.one@example.com"
    ```

2.  **Make your changes**: Edit the code, add new files, etc. For example, let's say you created the `main.py` file.

3.  **Stage and commit your changes**:
    ```bash
    # Stage the file
    git add main.py

    # Commit the file with your author information
    git commit -m "Initial commit: Create main GUI application"
    ```
    This commit is now attributed to "Student One".

---

### Step 2: Making a Commit as the Second Person (Your Teammate)

Now, let's say your teammate, "Student Two" (email: "student.two@example.com"), is making a change.

1.  **Change the author**: Before committing, you need to tell Git that "Student Two" is the author of the *next* commit. You can do this with the `--author` flag.

2.  **Make changes**: For example, let's say your teammate adds the `README.md` file.

3.  **Stage and commit the changes as your teammate**:
    ```bash
    # Stage the file
    git add README.md

    # Commit the file, but specify the author
    git commit --author="Student Two <student.two@example.com>" -m "Add detailed README file"
    ```
    This new commit is now attributed to "Student Two", even though you are the one running the command.

---

### Step 3: Switching Back and Forth

You can repeat this process for every commit.

-   **To commit as "Student One" again**: You don't need to do anything special, because your `git config` is already set to "Student One".
    ```bash
    git add <some-other-file>
    git commit -m "Another commit from Student One"
    ```

-   **To commit as "Student Two" again**: Use the `--author` flag again.
    ```bash
    git add <yet-another-file>
    git commit --author="Student Two <student.two@example.com>" -m "Another commit from Student Two"
    ```

---

### Step 4: How to View the Commit History

To see the results of your work, you can use the `git log` command. The default view is good, but a more detailed view is better.

```bash
git log --pretty=full
```

This command will show you a detailed history, including both the **Author** and the **Committer** for each commit. You will see something like this:

```
commit <commit_hash_4>
Author: Student Two <student.two@example.com>
Commit: Student One <student.one@example.com>

    Another commit from Student Two

commit <commit_hash_3>
Author: Student One <student.one@example.com>
Commit: Student One <student.one@example.com>

    Another commit from Student One

commit <commit_hash_2>
Author: Student Two <student.two@example.com>
Commit: Student One <student.one@example.com>

    Add detailed README file

commit <commit_hash_1>
Author: Student One <student.one@example.com>
Commit: Student One <student.one@example.com>

    Initial commit: Create main GUI application
```

This log clearly shows a history of collaboration between two different authors, which is exactly what your professor is looking for.
