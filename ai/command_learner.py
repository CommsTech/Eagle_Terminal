"""Command Learner module for Eagle Terminal's AI system.

This module provides functionality to learn from executed commands and
suggest new commands based on historical data.
"""

import asyncio
from asyncio import Queue
from typing import List

import aiosqlite


class CommandLearner:
    """A class for learning and suggesting commands based on historical data.

    This class manages a SQLite database to store command history,
    frequencies, and contexts. It provides methods for adding commands,
    retrieving suggestions, and analyzing command patterns.
    """

    def __init__(self, max_history: int = 1000, db_path: str = ":memory:"):
        self.max_history = max_history
        self.command_history: List[str] = []
        self.db_path = db_path
        self.queue: Queue = Queue()
        asyncio.create_task(self.process_queue())

    async def create_table(self) -> None:
        """Create the commands table in the SQLite database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS commands
                (id INTEGER PRIMARY KEY, command TEXT, context TEXT, frequency INTEGER)
            """
            )
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_context_freq ON commands(context, frequency DESC)"
            )
            await db.commit()

    async def add_command(self, command: str, context: str) -> None:
        """Add a command to the learner."""
        await self.queue.put(("add", command, context))

        # Add to command history
        self.command_history.append(command)
        if len(self.command_history) > self.max_history:
            self.command_history.pop(0)

    async def process_queue(self) -> None:
        """Process the queue of commands to be added to the database."""
        while True:
            item = await self.queue.get()
            if item[0] == "add":
                _, command, context = item
                async with aiosqlite.connect(self.db_path) as db:
                    await db.execute(
                        "INSERT OR REPLACE INTO commands (command, context, frequency) VALUES (?, ?, COALESCE((SELECT frequency FROM commands WHERE command = ? AND context = ?) + 1, 1))",
                        (command, context, command, context),
                    )
                    await db.commit()
            self.queue.task_done()

    async def get_popular_commands(self, n: int = 5) -> List[str]:
        """Get the n most popular commands."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT command FROM commands GROUP BY command ORDER BY SUM(frequency) DESC LIMIT ?",
                (n,),
            ) as cursor:
                return [row[0] for row in await cursor.fetchall()]

    async def get_command_suggestions(
        self, partial_command: str, n: int = 5
    ) -> List[str]:
        """Get command suggestions based on a partial command."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT command FROM commands WHERE command LIKE ? GROUP BY command ORDER BY SUM(frequency) DESC LIMIT ?",
                (f"{partial_command}%", n),
            ) as cursor:
                return [row[0] for row in await cursor.fetchall()]

    async def get_context_for_command(self, command: str) -> List[str]:
        """Get the contexts in which a command has been used."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT DISTINCT context FROM commands WHERE command = ?", (command,)
            ) as cursor:
                return [row[0] for row in await cursor.fetchall()]

    def get_command_history(self) -> List[str]:
        """Get the command history."""
        return self.command_history

    async def learn(
        self, command: str, output: str, os_type: str, analysis: str
    ) -> None:
        """Learn from the command execution and its analysis."""
        context = (
            f"{os_type}:{output[:100]}"  # Use first 100 chars of output as context
        )
        await self.add_command(command, context)
        print(f"Learned from command: {command}")
        print(f"Analysis: {analysis}")

    async def cleanup(self, days: int = 30) -> None:
        """Clean up old commands from the database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM commands WHERE last_used < datetime('now', '-? days')",
                (days,),
            )
            await db.commit()
