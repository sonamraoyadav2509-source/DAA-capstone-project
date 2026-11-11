# Mini-Courier Planner — Login + Neon Blue Dashboard

## Database: SQLite (recommended for this desktop project)
You do **not** need MySQL Workbench, phpMyAdmin, XAMPP, or a database server. Python creates `courier_users.db` automatically on first run. SQLite is built into Python.

## Run in VS Code (Windows)
1. Extract this ZIP.
2. Open the `Mini_Courier_Planner_Login` folder in VS Code: File → Open Folder.
3. Open Terminal → New Terminal.
4. Run `python --version` to confirm Python is installed.
5. Install requirements: `python -m pip install -r requirements.txt`
6. Start the application: `python gui.py`

## First login
- User ID: `admin`
- Password: `Courier@123`

The login password is stored as a salted PBKDF2 hash in SQLite, not as plain text. This is a local desktop login, not a cloud login. Change the default credentials before using the app for real data.

## Main files
- `gui.py` — login screen, dashboard, logout
- `auth_db.py` — SQLite user database and password verification
- `courier_users.db` — generated automatically at first launch
- `algorithms/` — Merge Sort, Knapsack, Dijkstra, TSP
- `data/` — parcel and delivery network CSV files
- `utils.py` — data loading helpers
