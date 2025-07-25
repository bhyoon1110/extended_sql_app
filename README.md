# Extended SQL App (Deliverable #5)

## Overview
This is a Flask‑based web application that lets you run a variety of complex SQL queries against a SQLite database via a clean, user‑friendly web interface.

## Installation & Usage
```bash
git clone https://github.com/bhyoon1110/extended_sql_app.git
cd extended_sql_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python database_setup.py     # Initialize the database
python app.py                # Start the server (http://localhost:5000)
