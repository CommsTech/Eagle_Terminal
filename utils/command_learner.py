import sqlite3
from typing import List, Tuple


class CommandLearner:
    def __init__(self):
        """Initialize the database connection and create the table.
        
        This method is the constructor for the class. It establishes an in-memory SQLite database connection
        and calls the create_table method to set up the necessary table structure.
        
        Args:
            self: The instance of the class.
        
        Returns:
            None
        
        Raises:
            sqlite3.Error: If there's an issue connecting to the database or creating the table.
        """
        self.conn = sqlite3.connect(":memory:")
        self.create_table()

    def create_table(self):
        """Creates a table named 'commands' in the database if it doesn't already exist.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            sqlite3.Error: If there's an error executing the SQL statements.
        
        Note:
            This method creates a table with columns for id, command, context, and frequency.
            It also creates an index on the context and frequency columns for optimized queries.
        """
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
        """Adds or updates a command in the database with its context and increments its frequency.
        
        Args:
            command (str): The command to be added or updated in the database.
            context (str): The context associated with the command.
        
        Returns:
            None
        
        Raises:
            sqlite3.Error: If there's an issue with the database operation.
        """
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
        """Retrieve a list of suggested commands based on the given context.
        
        Args:
            context (str): The context for which to retrieve command suggestions.
            limit (int, optional): The maximum number of suggestions to return. Defaults to 5.
        
        Returns:
            List[Tuple[str, int]]: A list of tuples containing suggested commands and their frequencies,
            sorted by frequency in descending order.
        """
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
        """Closes the connection to the database.
        
        This method should be called when the connection is no longer needed to release
        resources and ensure proper cleanup.
        
        Returns:
            None: This method doesn't return anything.
        """
        self.conn.close()

    def save_to_disk(self, file_path: str):
        """Saves the current database to a file on disk.
        
        Args:
            file_path (str): The path where the database file will be saved.
        
        Returns:
            None
        
        Raises:
            sqlite3.Error: If there's an error during the database backup process.
        """
        disk_conn = sqlite3.connect(file_path)
        with disk_conn:
            self.conn.backup(disk_conn)
        disk_conn.close()

    def load_from_disk(self, file_path: str):
        """Loads data from a SQLite database file on disk into the current in-memory database.
        
        Args:
            file_path (str): The path to the SQLite database file to be loaded.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            sqlite3.Error: If there's an error connecting to or backing up the database.
        """
        disk_conn = sqlite3.connect(file_path)
        disk_conn.backup(self.conn)
        disk_conn.close()
