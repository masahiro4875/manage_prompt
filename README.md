# manage_prompt

## Python development setup

Install the application and development dependencies into the virtual environment:

```bash
python -m pip install -r requirements-dev.txt
```

Format the Python source and tests with Black:

```bash
python -m black app tests
```

Check formatting without changing files:

```bash
python -m black --check app tests
```

When this project is opened in VS Code, install the recommended extensions. Saving
a Python file then formats it automatically with the Black executable in `.venv`.
