import sqlite3
from typing import List, Tuple


class CommandLearner:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS commands
        (id INTEGER PRIMARY KEY, command TEXT, context TEXT, frequency INTEGER)
        """
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_context_freq ON commands(context, frequency DESC)"
        )
        self.conn.commit()

    def add_command(self, command: str, context: str):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        INSERT OR REPLACE INTO commands (command, context, frequency)
        VALUES (?, ?, COALESCE((SELECT frequency FROM commands WHERE command = ? AND context = ?), 0) + 1)
        """,
            (command, context, command, context),
        )
        self.conn.commit()

    def get_suggestions(self, context: str, limit: int = 5) -> List[Tuple[str, int]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
        SELECT command, frequency FROM commands
        WHERE context = ?
        ORDER BY frequency DESC
        LIMIT ?
        """,
            (context, limit),
        )
        return cursor.fetchall()

    def close(self):
        self.conn.close()

    def save_to_disk(self, file_path: str):
        disk_conn = sqlite3.connect(file_path)
        with disk_conn:
            self.conn.backup(disk_conn)
        disk_conn.close()

    def load_from_disk(self, file_path: str):
        disk_conn = sqlite3.connect(file_path)
        disk_conn.backup(self.conn)
        disk_conn.close()
