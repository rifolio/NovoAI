# Bachelor Project Collaboration Repo
---
## Created by:
- **Vladyslav Horbatenko** - [GitHub](https://github.com/rifolio)
- **Salar Komeyshi** - [GitHub](https://github.com/SalarKo)
---

![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)

## Basic Rules for GitHub Maintenance

### 1. Cloning the Repository

To begin, clone the repository:

```bash
git clone https://github.com/rifolio/NovoAI.git
```

Navigate into the cloned directory:

```bash
cd NovoAI
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

### 2. Creating and Merging a Feature Branch

To ensure proper version control, follow these steps:

1. **Pull the latest changes from `main` and create a new branch:**

   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature-branch-name
   ```

2. **Make necessary changes and commit them:**

   ```bash
   git add .
   git commit -m "Descriptive commit message"
   ```

3. **Push the branch to GitHub:**

   ```bash
   git push origin feature-branch-name
   ```

4. **Create a Pull Request (PR) on GitHub:**

   - Navigate to the repository on GitHub.
   - Click on "Compare & pull request".
   - Ensure the base branch is `main` and the compare branch is `feature-branch-name`.
   - Provide a meaningful title and description for the PR.
   - Request a review from a team member.

5. **After approval, merge the PR into `main` and delete the branch:**

   ```bash
   git checkout main
   git pull origin main
   git branch -d feature-branch-name
   ```

---

### 3. Coding Style Guide

- **Class Names:** Use `CamelCase`
- **Variable & Function Names:** Use `snake_case`
- **Constants:** Use `UPPER_SNAKE_CASE`
- **Indentation:** Use **4 spaces**
- **Line Length:** Keep lines **under 79 characters** where possible
- **Docstrings:** Use triple quotes for function/method documentation

Example:

```python
class SampleClass:
    def __init__(self, sample_value):
        self.sample_value = sample_value  # Snake case for variables

    def get_value(self):
        """Returns the stored value."""
        return self.sample_value
```

---

### 4. Commit Message Guidelines

- Use clear, concise commit messages.
- Follow the format:

  ```
  [Type] Short Description

  Longer description if necessary. Explain why the change was made and how it impacts the codebase.
  ```

  **Example:**

  ```
  [Fix] Corrected API response handling

  Fixed an issue where the API response was not being correctly parsed, causing a failure in user authentication.
  ```

---

### 5. Other Best Practices

- **Never push directly to `main`**; always use feature branches and PRs.
- **Keep PRs small** and focused on a single feature or fix.
- **Pull `main` before starting new work** to avoid merge conflicts.
- **Run tests before pushing changes** to ensure stability.

---

Following these guidelines will help maintain a clean, efficient, and collaborative codebase.
