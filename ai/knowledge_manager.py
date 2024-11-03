"""Knowledge Manager module for Eagle Terminal's AI system.

This module provides functionality to manage and retrieve relevant
knowledge for AI-powered responses and learning.
"""

from typing import Dict, List


class KnowledgeManager:
    """A class for managing and retrieving knowledge for AI-powered responses.

    This class handles storing, retrieving, and updating knowledge in
    various categories, as well as managing conversation history.
    """

    def __init__(self, user_id: str):
        """Initialize the KnowledgeManager.

        Args:
            user_id (str): The ID of the user associated with this knowledge manager.
        """
        self.user_id = user_id
        self.conversation_history: List[str] = []
        self.knowledge_base: Dict[str, str] = {}

    def get_relevant_knowledge(self, query: str) -> str:
        """Retrieve relevant knowledge based on the given query.

        Args:
            query (str): The query to search for relevant knowledge.

        Returns:
            str: The relevant knowledge found.
        """
        relevant_knowledge = []
        query_words = set(query.lower().split())

        for category, knowledge in self.knowledge_base.items():
            if any(word in knowledge.lower() for word in query_words):
                relevant_knowledge.append(f"{category}: {knowledge}")

        if relevant_knowledge:
            return "\n".join(relevant_knowledge)
        else:
            return f"No relevant knowledge found for query: {query}"

    def get_knowledge(self, category: str) -> str:
        """Retrieve knowledge for a specific category.

        Args:
            category (str): The category of knowledge to retrieve.

        Returns:
            str: The knowledge associated with the category.
        """
        return self.knowledge_base.get(category, "")

    def learn(self, category: str, information: str) -> None:
        """Add new information to the knowledge base.

        Args:
            category (str): The category of the information.
            information (str): The information to add.
        """
        if category in self.knowledge_base:
            self.knowledge_base[category] += f"\n{information}"
        else:
            self.knowledge_base[category] = information

    def clear_conversation_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []

    def get_all_knowledge(self) -> Dict[str, str]:
        """Retrieve all knowledge from the knowledge base.

        Returns:
            Dict[str, str]: A dictionary containing all knowledge categories and their information.
        """
        return self.knowledge_base

    def set_all_knowledge(self, knowledge: Dict[str, str]) -> None:
        """Set the entire knowledge base.

        Args:
            knowledge (Dict[str, str]): A dictionary containing all knowledge categories and their information.
        """
        self.knowledge_base = knowledge

    def __repr__(self) -> str:
        """Return a string representation of the KnowledgeManager.

        Returns:
            str: A string representation of the KnowledgeManager.
        """
        return (
            f"KnowledgeManager(user_id={self.user_id}, "
            f"categories={list(self.knowledge_base.keys())})"
        )
