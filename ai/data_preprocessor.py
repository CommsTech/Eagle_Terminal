"""Data Preprocessor module for Eagle Terminal's AI system.

This module provides functionality to preprocess text data for use in
machine learning models, including tokenization and dataset creation.
"""

import json
from typing import Any, Dict

import torch  # Add this import
from transformers import PreTrainedTokenizer


class DataPreprocessor:
    """A class for preprocessing text data for machine learning models.

    This class handles tokenization and encoding of text data, preparing
    it for use in transformer-based models.
    """

    def __init__(self, tokenizer: PreTrainedTokenizer):
        """Initialize the DataPreprocessor with a tokenizer.

        Args:
            tokenizer (PreTrainedTokenizer): The tokenizer to use for encoding text.
        """
        self.tokenizer = tokenizer

    def preprocess(self, text: str, max_length: int = 512) -> Dict[str, Any]:
        # Tokenize and prepare the input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=max_length,
        )
        return inputs


class SSHDataset(torch.utils.data.Dataset):
    """A custom Dataset class for SSH command data.

    This class creates a PyTorch Dataset from preprocessed SSH command
    data, making it easy to use with PyTorch DataLoaders.
    """

    def __init__(self, encodings, labels):
        """Initialize the SSHDataset with encodings and labels.

        Args:
            encodings: The preprocessed text encodings.
            labels: The corresponding labels for the encodings.
        """
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        """Get a single item from the dataset.

        Args:
            idx (int): The index of the item to retrieve.

        Returns:
            dict: A dictionary containing the item's encodings and label.
        """
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        """Get the length of the dataset.

        Returns:
            int: The number of items in the dataset.
        """
        return len(self.labels)
