"""Response Generator module for Eagle Terminal's AI system."""

import asyncio
import json
import re
import traceback
from functools import lru_cache
from typing import Any, Dict, List

import torch

from .cache import Cache
from .data_preprocessor import DataPreprocessor


class ResponseGenerator:
    """A class for generating responses using a pre-trained language model."""

    def __init__(self, model_manager, data_preprocessor: DataPreprocessor):
        """Initialize the ResponseGenerator with a model manager.

        Args:
            model_manager: The model manager object containing the language model.
            data_preprocessor: The data preprocessor object for preprocessing input data.
        """
        self.model_manager = model_manager
        self.cache = Cache()
        self.data_preprocessor = data_preprocessor
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    async def generate_response_async(
        self, prompt: str, context: Dict[str, Any]
    ) -> str:
        """Asynchronously generate a response based on the given prompt.

        Args:
            prompt (str): The input prompt for generating a response.
            context (Dict[str, Any]): The context for generating a response.

        Returns:
            str: The generated response.
        """
        try:
            if context.get("command") == "ip a":
                return self.analyze_ip_a_output(context.get("output", ""))

            # For other commands, use the AI model
            hashable_context = json.dumps(context, sort_keys=True)
            return self.get_cached_response(prompt, hashable_context)
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def analyze_ip_a_output(self, output: str) -> str:
        interfaces = re.findall(r"\d+: (\w+):", output)
        analysis = f"Network Interfaces: {len(interfaces)}\n\n"

        for interface in interfaces:
            analysis += f"Interface: {interface}\n"
            if interface == "lo":
                analysis += "- Loopback interface\n"
            elif interface.startswith("eth"):
                analysis += "- Ethernet interface\n"
            elif interface.startswith("wlan"):
                analysis += "- Wireless interface\n"
            elif interface == "docker0":
                analysis += "- Docker bridge interface\n"

            ip_addresses = re.findall(
                rf"{interface}.*?inet\s([\d.]+)", output, re.DOTALL
            )
            if ip_addresses:
                analysis += f"- IPv4 address: {ip_addresses[0]}\n"

            ip6_addresses = re.findall(
                rf"{interface}.*?inet6\s([\w:]+)", output, re.DOTALL
            )
            if ip6_addresses:
                analysis += f"- IPv6 address: {ip6_addresses[0]}\n"

            analysis += "\n"

        return analysis.strip()

    @lru_cache(maxsize=100)
    def get_cached_response(self, prompt: str, context_hash: str) -> str:
        # This method will cache responses based on the prompt and a hash of the context
        context = json.loads(context_hash)
        return self.generate_response(prompt, context)

    def generate_response(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate a response based on the given prompt and parameters.

        Args:
            prompt (str): The input prompt for generating a response.
            context (Dict[str, Any]): The context for generating a response.

        Returns:
            str: The generated response.
        """
        combined_input = (
            f"Command: {context.get('command', '')}\n"
            f"Output: {context.get('output', '')[:500]}...\n"  # Truncate long outputs
            f"OS Type: {context.get('os_type', '')}\n"
            f"Recent Commands: {', '.join(context.get('command_history', [])[-3:])}\n\n"
            f"Task: {prompt}\n"
            f"Response:"
        )

        inputs = self.model_manager.tokenizer(
            combined_input,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model_manager.model.generate(
                **inputs,
                max_new_tokens=150,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7,
            )

        response = self.model_manager.tokenizer.decode(
            outputs[0], skip_special_tokens=True
        )
        return self.clean_up_response(response)

    def clean_up_response(self, response: str) -> str:
        """Clean up the generated text by removing extra spaces and performing
        other cleanup tasks.

        Args:
            text (str): The text to clean up.

        Returns:
            str: The cleaned up text.
        """
        response = response.split("Response:", 1)[-1].strip()
        return response

    def generate_dynamic_response(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate a dynamic response based on the given prompt and
        parameters.

        Args:
            prompt (str): The input prompt for generating a response.
            context (Dict[str, Any]): The context for generating a response.

        Returns:
            str: The generated dynamic response.
        """
        return self.generate_response(prompt, context)

    def generate_multiple_responses(
        self,
        prompt: str,
        context: Dict[str, Any],
        num_responses: int = 3,
    ) -> List[str]:
        """Generate multiple responses for the given prompt.

        Args:
            prompt (str): The input prompt for generating responses.
            context (Dict[str, Any]): The context for generating responses.
            num_responses (int): The number of responses to generate.

        Returns:
            List[str]: A list of generated responses.
        """
        return [self.generate_response(prompt, context) for _ in range(num_responses)]

    def analyze_whoami(self, output: str) -> str:
        return f"The 'whoami' command shows the current user. The output indicates that the current user is '{output.strip()}'."

    def suggest_ip_command(self) -> str:
        return "To see your current IP address, you can use the following command:\n\nip addr show\n\nThis command will display information about all network interfaces, including their IP addresses."
