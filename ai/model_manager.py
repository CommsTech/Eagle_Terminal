"""Model Manager module for Eagle Terminal's AI system.

This module provides functionality to load, save, update, and manage the
AI model used for generating responses in Eagle Terminal.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List

import torch
from transformers import (
    AutoModel,
    AutoModelForCausalLM,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DistilBertForSequenceClassification,
    DistilBertTokenizer,
    GPT2LMHeadModel,
    GPT2Tokenizer,
    Trainer,
    TrainingArguments,
)

from utils.logger import logger

from .data_preprocessor import DataPreprocessor, SSHDataset


class ModelManager:
    """A class for managing the AI model used in Eagle Terminal.

    This class handles loading, saving, fine-tuning, and evaluating the
    model, as well as managing different versions of the model.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the ModelManager with the given configuration.

        Args:
            config (Dict[str, Any]): Configuration dictionary for the model manager.
        """
        self.config = config
        self.model = None
        self.tokenizer = None
        self.model_name = config.get(
            "model_name", "gpt2"
        )  # Default to GPT-2 if not specified
        self.max_length = config.get("max_length", 512)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model()

    def load_model(self):
        """Load the model and tokenizer."""
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
            self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
            self.model.to(self.device)

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                self.model.config.pad_token_id = self.tokenizer.pad_token_id

            print(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise

    async def fine_tune_async(self, train_texts: List[str], train_labels: List[int]):
        """Asynchronously fine-tune the model with the given training data.

        This method runs the fine-tuning process in a separate thread to avoid
        blocking the main event loop. It uses the synchronous `fine_tune` method
        to perform the actual fine-tuning.

        Args:
            train_texts (List[str]): A list of training text samples.
            train_labels (List[int]): A list of corresponding labels for the training samples.

        Returns:
            None
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.fine_tune, train_texts, train_labels)

    def fine_tune(self, train_texts: List[str], train_labels: List[int]):
        """Fine-tune the model with the given training data.

        Args:
            train_texts (List[str]): A list of training text samples.
            train_labels (List[int]): A list of corresponding labels for the training samples.
        """
        train_dataset = self._prepare_dataset(train_texts, train_labels)

        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=self.config["fine_tuning_epochs"],
            per_device_train_batch_size=self.config["batch_size"],
            learning_rate=self.config["learning_rate"],
            weight_decay=self.config.get("weight_decay", 0.01),
            logging_dir="./logs",
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
        )

        trainer.train()
        self.save_model()

    def _prepare_dataset(self, texts: List[str], labels: List[int]) -> SSHDataset:
        """Prepare the dataset for training or evaluation.

        Args:
            texts (List[str]): A list of text samples.
            labels (List[int]): A list of corresponding labels.

        Returns:
            SSHDataset: The prepared dataset.
        """
        encodings = self.preprocessor.preprocess(texts)
        return SSHDataset(encodings, labels)

    def evaluate(
        self, eval_texts: List[str], eval_labels: List[int]
    ) -> Dict[str, float]:
        """Evaluate the model on the given evaluation data.

        Args:
            eval_texts (List[str]): A list of evaluation text samples.
            eval_labels (List[int]): A list of corresponding labels for the evaluation samples.

        Returns:
            Dict[str, float]: A dictionary containing evaluation metrics.
        """
        eval_dataset = self._prepare_dataset(eval_texts, eval_labels)
        trainer = Trainer(model=self.model)
        results = trainer.evaluate(eval_dataset)
        return results

    def save_model(self):
        """Save the current model, tokenizer, and metadata."""
        save_directory = os.path.join(os.path.dirname(__file__), "saved_model")
        os.makedirs(save_directory, exist_ok=True)
        self.model.save_pretrained(save_directory)
        self.tokenizer.save_pretrained(save_directory)
        logger.info(f"Model saved to {save_directory}")

    def load_model_version(self, version: str):
        """Load a specific version of the model.

        Args:
            version (str): The version of the model to load.
        """
        path = f"./model_versions/{version}"
        if os.path.exists(path):
            self.model = AutoModelForSequenceClassification.from_pretrained(path)
            self.tokenizer = AutoTokenizer.from_pretrained(path)
            self.preprocessor = DataPreprocessor(self.tokenizer)
        else:
            raise ValueError(f"Model version {version} not found")

    def _get_next_version(self):
        """Get the next available version number for saving a new model
        version."""
        versions = [int(d) for d in os.listdir("./model_versions") if d.isdigit()]
        return str(max(versions) + 1) if versions else "1"

    def save_model_version(self, version: str):
        """Save the current model as a new version.

        Args:
            version (str): The version number to save the model as.
        """
        path = f"./model_versions/{version}"
        os.makedirs(path, exist_ok=True)
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)

        # Save version metadata
        metadata = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "config": self.config,
        }
        with open(os.path.join(path, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f)

    def list_model_versions(self):
        """List all available model versions.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing metadata for each model version.
        """
        versions = []
        for version in os.listdir("./model_versions"):
            metadata_path = os.path.join("./model_versions", version, "metadata.json")
            if os.path.exists(metadata_path):
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                versions.append(metadata)
        return versions

    def rollback_to_version(self, version: str):
        """Roll back to a specific version of the model.

        Args:
            version (str): The version to roll back to.
        """
        self.load_model_version(version)
        # Optionally, you can set this version as the current active version
        # self.current_version = version

    def update_config(self, new_config: Dict[str, Any]):
        """Update the configuration with new settings."""
        self.config.update(new_config)
        # Implement any necessary changes based on the updated config
        # For example, you might need to reload the model if certain parameters change

    def is_model_loaded(self):
        return self.model is not None and self.tokenizer is not None

    def unload_model(self):
        self.model = None
        self.tokenizer = None
        torch.cuda.empty_cache()
        logger.info("Model unloaded and CUDA cache cleared")
