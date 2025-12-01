# core/database.py
import sqlite3
from pathlib import Path

class QuestDatabase:
    def __init__(self, db_path="quests.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Create tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main quests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                description TEXT,
                difficulty TEXT CHECK(difficulty IN ('Легкий', 'Средний', 'Сложный', 'Эпический')),
                deadline TEXT,
                reward INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Version history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quest_versions (
                id INTEGER PRIMARY KEY,
                quest_id INTEGER,
                title TEXT,
                difficulty TEXT,
                reward INTEGER,
                description TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (quest_id) REFERENCES quests(id)
            )
        """)

        conn.commit()
        conn.close()

    def add_quest(self, title, description, difficulty, deadline, reward):
        """Insert new quest and return its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO quests (title, description, difficulty, deadline, reward)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, difficulty, deadline, reward))
        quest_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return quest_id

    def update_quest(self, quest_id, title, description, difficulty, deadline, reward):
        """Update quest and save old version."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Save current state to versions
        cursor.execute("""
            INSERT INTO quest_versions (quest_id, title, difficulty, reward, description, created_at)
            SELECT id, title, difficulty, reward, description, datetime('now')
            FROM quests WHERE id = ?
        """, (quest_id,))

        # Update main quest
        cursor.execute("""
            UPDATE quests SET title=?, description=?, difficulty=?, deadline=?, reward=?
            WHERE id = ?
        """, (title, description, difficulty, deadline, reward, quest_id))

        conn.commit()
        conn.close()

    def get_all_quests(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quests ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_quest_by_id(self, quest_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quests WHERE id = ?", (quest_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_versions_for_quest(self, quest_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quest_versions WHERE quest_id = ? ORDER BY created_at DESC", (quest_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]