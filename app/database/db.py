import sqlite3
from datetime import datetime
from typing import Optional, List, Dict


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


class DBManager:
    @staticmethod
    def _get_connection():
        return sqlite3.connect("skillswap.db")

    # User methods
    @staticmethod
    def add_user(tg_id: int, name: str, bio: str, language: str, experience_level: str) -> Optional[int]:
        with DBManager._get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO users (tg_id, name, bio, language, experience_level)
                    VALUES (?, ?, ?, ?, ?)
                """, (tg_id, name, bio, language, experience_level))
                return cur.lastrowid
            except sqlite3.IntegrityError:
                return None

    @staticmethod
    def get_user(tg_id: int) -> Optional[Dict]:
        with DBManager._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
            result = cur.fetchone()
            if result:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, result))
            return None

    @staticmethod
    def update_user(tg_id: int, **kwargs) -> bool:
        with DBManager._get_connection() as conn:
            cur = conn.cursor()
            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            values = list(kwargs.values()) + [tg_id]
            cur.execute(f"UPDATE users SET {set_clause} WHERE tg_id = ?", values)
            return cur.rowcount > 0

    @staticmethod
    def delete_user(tg_id: int) -> bool:
        with DBManager._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE tg_id = ?", (tg_id,))
            return cur.rowcount > 0

    # Skill methods
    @staticmethod
    def add_skill(skill_name: str) -> int:
        with DBManager._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO skills (name) VALUES (?)", (skill_name,))
            conn.commit()
            cur.execute("SELECT id FROM skills WHERE name = ?", (skill_name,))
            return cur.fetchone()[0]

    @staticmethod
    def delete_skill(skill_id: int) -> bool:
        with DBManager._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM skills WHERE id = ?", (skill_id,))
            return cur.rowcount > 0

    # User-Skill methods
    @staticmethod
    def link_user_skill(tg_id: int, skill_name: str, skill_type: str) -> bool:
        with DBManager._get_connection() as conn:
            cur = conn.cursor()
            user = DBManager.get_user(tg_id)
            if not user:
                return False

            skill_id = DBManager.add_skill(skill_name)

            try:
                cur.execute("""
                    INSERT INTO user_skills (user_id, skill_id, type)
                    VALUES (?, ?, ?)
                """, (user['id'], skill_id, skill_type))
                return True
            except sqlite3.IntegrityError:
                return False

    @staticmethod
    def unlink_user_skill(tg_id: int, skill_name: str, skill_type: str) -> bool:
        with DBManager._get_connection() as conn:
            cur = conn.cursor()
            user = DBManager.get_user(tg_id)
            if not user:
                return False

            cur.execute("SELECT id FROM skills WHERE name = ?", (skill_name,))
            skill = cur.fetchone()
            if not skill:
                return False

            cur.execute("""
                DELETE FROM user_skills 
                WHERE user_id = ? 
                AND skill_id = ? 
                AND type = ?
            """, (user['id'], skill[0], skill_type))
            return cur.rowcount > 0

    # Session methods
    @staticmethod
    def create_session(user1_id: int, user2_id: int, skill_id: int) -> int:
        with DBManager._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO sessions (user_1_id, user_2_id, skill_id)
                VALUES (?, ?, ?)
            """, (user1_id, user2_id, skill_id))
            return cur.lastrowid


if __name__ == "__main__":
    init_db()
