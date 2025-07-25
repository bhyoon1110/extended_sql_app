# app.py
from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__, static_folder='static', template_folder='templates')

DB = 'app.db'

def query(sql, params=()):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_query', methods=['POST'])
def run_query():
    qtype = request.form['qtype']
    queries = {
        'set_union': """
            SELECT name FROM employees WHERE dept_id=2
            UNION
            SELECT name FROM employees WHERE dept_id=3;
        """,
        'set_intersect': """
            SELECT name FROM employees WHERE salary > 70000
            INTERSECT
            SELECT name FROM employees WHERE dept_id=2;
        """,
        'set_except': """
            SELECT name FROM employees
            EXCEPT
            SELECT name FROM employees WHERE dept_id=1;
        """,
        'set_membership': """
            SELECT * FROM employees
            WHERE dept_id IN (SELECT id FROM departments WHERE name IN ('HR','Sales'));
        """,
            'set_comparison': """
            -- Find employees whose salary exceeds every department’s average
            SELECT *
            FROM employees
            WHERE salary > (
            SELECT MAX(avg_salary)
            FROM (
                SELECT AVG(salary) AS avg_salary
                FROM employees
                GROUP BY dept_id
            )
            );
        """,
        'with_subquery': """
            WITH dept_sales AS (
                SELECT e.dept_id, SUM(s.amount) AS total_sales
                FROM sales s JOIN employees e ON s.emp_id=e.id
                GROUP BY e.dept_id
            )
            SELECT d.name, ds.total_sales
            FROM dept_sales ds JOIN departments d ON ds.dept_id=d.id;
        """,
            'advanced_agg': """
            -- Department subtotals
            SELECT
            e.dept_id,
            SUM(s.amount)   AS dept_total,
            AVG(s.amount)   AS avg_sale,
            COUNT(*)        AS sale_count
            FROM sales s
            JOIN employees e ON s.emp_id = e.id
            GROUP BY e.dept_id

            UNION ALL

            -- Grand total across all departments
            SELECT
            NULL            AS dept_id,
            SUM(s.amount),
            AVG(s.amount),
            COUNT(*)
            FROM sales s
            JOIN employees e ON s.emp_id = e.id;
        """,

        'olap': """
            SELECT
              e.name,
              e.dept_id,
              s.sale_date,
              s.amount,
              RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS salary_rank,
              AVG(s.amount) OVER (PARTITION BY e.id ORDER BY s.sale_date ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS moving_avg_4
            FROM sales s
            JOIN employees e ON s.emp_id=e.id;
        """
    }
    sql = queries[qtype]
    df = query(sql)
    return render_template('results.html', table=df.to_html(classes='table table-striped', index=False))

if __name__ == '__main__':
    app.run(debug=True)
