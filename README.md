# manage_prompt

## Local development

Create a `.env` file in the project root and configure your PostgreSQL connection:

```dotenv
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/manage_prompts
```

The application loads this file automatically. Existing environment variables take
precedence. Startup fails with a clear error if `DATABASE_URL` is missing or empty.
Keep `.env` out of version control. The database and application tables must already
exist; startup does not create them.

After installing the Python dependencies below, start FastAPI from the project root:

```bash
.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

In a second terminal, start the frontend:

```bash
cd app/frontend
npm install
npm run dev
```

Open the URL printed by Vite. During development, Vite forwards `/prompts`
requests to FastAPI at `http://127.0.0.1:8000`.

## Progress — 2026-10-05

- Verified PostgreSQL connectivity and the presence of all five application tables
  and their expected columns in the local database.
- Added automatic `.env` loading and an explicit error for missing `DATABASE_URL`.
- Added prompt fetching on initial page load and a title/body registration form.
- Prompt API results and errors currently appear in the browser console.
- The gallery still displays sample data. Image upload and linking images to
  registered prompts remain the next steps.

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
