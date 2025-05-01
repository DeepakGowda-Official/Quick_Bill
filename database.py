import sqlite3

def get_connection():
    conn = sqlite3.connect('users.db')
    return conn

def create_table():
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            username TEXT PRIMARY KEY,
                            password TEXT NOT NULL,
                            role TEXT NOT NULL)''')
        conn.commit()

def create_user(username, password, role):
    with get_connection() as conn:
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()

def get_user(username):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, password, role FROM users WHERE username = ?", (username,))
        return cur.fetchone()


create_table()
