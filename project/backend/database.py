import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "registrations.db")


def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create the registrations table if it does not exist."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            field TEXT NOT NULL,
            experience TEXT NOT NULL,
            status TEXT DEFAULT 'Confirmed',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_registration(name, email, field, experience):
    """Save a new registration."""

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO registrations
            (name, email, field, experience)
            VALUES (?, ?, ?, ?)
        """, (name, email, field, experience))

        conn.commit()

        return True, "Registration saved successfully."

    except sqlite3.IntegrityError:
        return False, "This email is already registered."

    finally:
        conn.close()


def get_registration_by_email(email):
    """Find a registration using email."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, field, experience, status, registered_at
        FROM registrations
        WHERE LOWER(email) = LOWER(?)
    """, (email,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "field": row[3],
            "experience": row[4],
            "status": row[5],
            "registered_at": row[6]
        }

    return None


def get_all_registrations():
    """Return all registrations."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, field, experience, status, registered_at
        FROM registrations
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    registrations = []

    for row in rows:
        registrations.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "field": row[3],
            "experience": row[4],
            "status": row[5],
            "registered_at": row[6]
        })

    return registrations