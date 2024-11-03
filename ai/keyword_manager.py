"""Keyword Manager module for Eagle Terminal's AI system.

This module provides functionality to manage and extract important
keywords from text using both predefined keywords and AI suggestions.
"""

from typing import Callable, List, Set


class KeywordManager:
    """A class for managing and extracting important keywords.

    This class allows adding and removing keywords, extracting important
    keywords from text, and retrieving knowledge associated with
    keywords.
    """

    def __init__(self, user_id: str):
        """Initialize the KeywordManager.

        Args:
            user_id (str): The ID of the user associated with this keyword manager.
        """
        self.user_id = user_id
        self.keywords: Set[str] = set()

    def add_keyword(self, keyword: str) -> None:
        """Add a new keyword to the manager.

        Args:
            keyword (str): The keyword to add.
        """
        self.keywords.add(keyword.lower())

    def remove_keyword(self, keyword: str) -> None:
        """Remove a keyword from the manager.

        Args:
            keyword (str): The keyword to remove.
        """
        self.keywords.discard(keyword.lower())

    def get_important_keywords(
        self, text: str, ai_function: Callable[[str], str]
    ) -> List[str]:
        """Extract important keywords from the given text.

        Args:
            text (str): The text to analyze.
            ai_function (Callable[[str], str]): Function to generate AI responses.

        Returns:
            List[str]: A list of important keywords found in the text.
        """
        words = text.lower().split()
        extracted_keywords = [word for word in words if word in self.keywords]

        if not extracted_keywords:
            ai_suggestion = ai_function(
                f"Suggest important keywords from this text: {text}"
            )
            extracted_keywords = ai_suggestion.lower().split()

        return extracted_keywords

    def get_knowledge(self, category: str) -> str:
        """Retrieve knowledge for a specific category.

        Args:
            category (str): The category of knowledge to retrieve.

        Returns:
            str: The knowledge associated with the category.
        """
        # Implement knowledge retrieval logic here
        if category in self.keywords:
            return f"Knowledge about {category}: This is an important keyword in the system."
        else:
            return f"No specific knowledge available for {category}."

    def get_all_keywords(self) -> List[str]:
        """Get all keywords stored in the manager.

        Returns:
            List[str]: A list of all keywords.
        """
        return list(self.keywords)

    def __repr__(self) -> str:
        """Return a string representation of the KeywordManager.

        Returns:
            str: A string representation of the KeywordManager.
        """
        return f"KeywordManager(user_id={self.user_id}, keywords={self.keywords})"


if __name__ == "__main__":
    # Example usage
    km = KeywordManager("user123")
    km.add_keyword("python")
    km.add_keyword("AI")

    print(km)
    print("All keywords:", km.get_all_keywords())

    SAMPLE_TEXT = "Commstech and Python are great for AI development"
    important_keywords = km.get_important_keywords(
        SAMPLE_TEXT, lambda x: "python ai development"
    )
    print("Important keywords:", important_keywords)

    print(km.get_knowledge("python"))
    print(km.get_knowledge("java"))
