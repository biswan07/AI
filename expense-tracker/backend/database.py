import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'expenses.db')

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            credit REAL DEFAULT 0,
            debit REAL DEFAULT 0,
            person TEXT NOT NULL,
            provider TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def get_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_expense(expense_data):
    """Insert a new expense into the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO expenses (date, description, category, credit, debit, person, provider)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        expense_data['date'],
        expense_data['description'],
        expense_data['category'],
        expense_data.get('credit', 0),
        expense_data.get('debit', 0),
        expense_data['person'],
        expense_data.get('provider', 'Unknown')
    ))

    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()
    return expense_id

def get_all_expenses():
    """Get all expenses from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return expenses

def get_expenses_by_date_range(start_date, end_date):
    """Get expenses within a date range."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM expenses
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
    ''', (start_date, end_date))

    expenses = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return expenses

def delete_all_expenses():
    """Delete all expenses (for testing)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses')
    conn.commit()
    conn.close()

# Initialize database on import
init_db()
