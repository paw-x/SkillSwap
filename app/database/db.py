import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("skillswap.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE,
        name TEXT,
        bio TEXT,
        experience_level TEXT,
        language TEXT,
        registered_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_skills (
        user_id INTEGER,
        skill_id INTEGER,
        type TEXT CHECK(type IN ('teach', 'learn')),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(skill_id) REFERENCES skills(id),
        PRIMARY KEY(user_id, skill_id, type)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_1_id INTEGER,
        user_2_id INTEGER,
        skill_id INTEGER,
        status TEXT CHECK(status IN ('pending', 'confirmed', 'done')) DEFAULT 'pending',
        scheduled_for TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_1_id) REFERENCES users(id),
        FOREIGN KEY(user_2_id) REFERENCES users(id),
        FOREIGN KEY(skill_id) REFERENCES skills(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_user INTEGER,
        to_user INTEGER,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        comment TEXT,
        session_id INTEGER,
        FOREIGN KEY(from_user) REFERENCES users(id),
        FOREIGN KEY(to_user) REFERENCES users(id),
        FOREIGN KEY(session_id) REFERENCES sessions(id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
