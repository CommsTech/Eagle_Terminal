"""Command Suggester module for Eagle Terminal.

This module provides functionality to suggest commands for various
operating systems and network devices using a pre-trained language
model.
"""

import threading
from typing import List

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class CommandSuggester:
    """A class for suggesting commands based on context, OS type, and device
    type.

    This class uses a pre-trained language model to generate relevant
    command suggestions, explanations, and syntax information.
    """

    def __init__(self):
        """Initialize the CommandSuggester with a pre-trained language
        model."""
        self.model_name = "distilgpt2"  # Smaller version of GPT-2
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_thread = None
        self.is_model_loaded = False
        self.command_history = []
        self.command_embeddings = []

    def start_loading_model(self):
        """Start loading the model in a separate thread."""
        self.load_thread = threading.Thread(target=self._load_model)
        self.load_thread.start()

    def _load_model(self):
        """Load the pre-trained language model and tokenizer."""
        if self.model is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.model = torch.quantization.quantize_dynamic(
                self.model, {torch.nn.Linear}, dtype=torch.qint8
            )
            self.model.to(self.device)
            self.is_model_loaded = True

    def _ensure_model_loaded(self):
        """Ensure that the model is loaded before using it."""
        if self.load_thread and self.load_thread.is_alive():
            self.load_thread.join()  # Wait for the loading to complete if it's still ongoing

    def suggest_command(self, context: str, os_type: str, device_type: str) -> str:
        """Suggest a command based on the given context, OS type, and device
        type.

        Args:
            context (str): The context for the command suggestion.
            os_type (str): The type of operating system.
            device_type (str): The type of device.

        Returns:
            str: A suggested command.
        """
        self._ensure_model_loaded()
        prompt = f"OS: {os_type}\nDevice: {device_type}\nContext: {context}\nSuggested command:"
        return self._generate_text(prompt, max_length=100)

    def get_command_explanation(
        self, command: str, os_type: str, device_type: str
    ) -> str:
        """Get an explanation for the given command.

        Args:
            command (str): The command to explain.
            os_type (str): The type of operating system.
            device_type (str): The type of device.

        Returns:
            str: An explanation of the command.
        """
        self._ensure_model_loaded()
        prompt = (
            f"OS: {os_type}\nDevice: {device_type}\nCommand: {command}\nExplanation:"
        )
        return self._generate_text(prompt, max_length=200)

    def get_command_syntax(self, command: str, os_type: str, device_type: str) -> str:
        """Get the syntax for the given command.

        Args:
            command (str): The command to get syntax for.
            os_type (str): The type of operating system.
            device_type (str): The type of device.

        Returns:
            str: The syntax of the command.
        """
        self._ensure_model_loaded()
        prompt = f"OS: {os_type}\nDevice: {device_type}\nCommand: {command}\nSyntax:"
        return self._generate_text(prompt, max_length=150)

    def _generate_text(self, prompt: str, max_length: int) -> str:
        """Generate text using the pre-trained language model.

        Args:
            prompt (str): The input prompt for text generation.
            max_length (int): The maximum length of the generated text.

        Returns:
            str: The generated text.
        """
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True,
            )

        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text.split(prompt)[-1].strip()

    def suggest_multiple_commands(
        self, context: str, os_type: str, device_type: str, num_suggestions: int = 3
    ) -> List[str]:
        """Suggest multiple commands based on the given context, OS type, and
        device type.

        Args:
            context (str): The context for the command suggestions.
            os_type (str): The type of operating system.
            device_type (str): The type of device.
            num_suggestions (int): The number of command suggestions to generate.

        Returns:
            List[str]: A list of suggested commands.
        """
        return [
            self.suggest_command(context, os_type, device_type)
            for _ in range(num_suggestions)
        ]

    async def get_similar_commands(
        self, context_embedding: np.ndarray, top_n: int = 5
    ) -> List[str]:
        if not self.command_embeddings:
            return []

        similarities = np.dot(self.command_embeddings, context_embedding.T).flatten()
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        return [self.command_history[i] for i in top_indices]

    def add_command(self, command: str, embedding: np.ndarray):
        self.command_history.append(command)
        self.command_embeddings.append(embedding)
