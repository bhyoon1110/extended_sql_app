# database_setup.py
import sqlite3
from datetime import date, timedelta
import random

conn = sqlite3.connect('app.db')
cur = conn.cursor()

# 테이블 생성
cur.executescript("""
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS sales;

CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dept_id INTEGER,
    salary REAL,
    FOREIGN KEY(dept_id) REFERENCES departments(id)
);

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id INTEGER,
    sale_date DATE,
    amount REAL,
    FOREIGN KEY(emp_id) REFERENCES employees(id)
);
""")

# 샘플 데이터 삽입
departments = [(1, 'HR'), (2, 'Engineering'), (3, 'Sales')]
employees = [
    (1, 'Alice', 2, 85000),
    (2, 'Bob',   2, 95000),
    (3, 'Carol', 1, 62000),
    (4, 'Dave',  3, 72000),
    (5, 'Eve',   3, 68000),
]
cur.executemany("INSERT INTO departments VALUES (?, ?)", departments)
cur.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", employees)

# Sales: 최근 30일치 랜덤 매출
base = date.today() - timedelta(days=30)
sales = []
for emp_id in range(1,6):
    for i in range(10):
        d = base + timedelta(days=random.randint(0,30))
        amt = round(random.uniform(500,2000),2)
        sales.append((emp_id, d.isoformat(), amt))
cur.executemany("INSERT INTO sales(emp_id, sale_date, amount) VALUES (?,?,?)", sales)

conn.commit()
conn.close()
print("Database initialized.")
