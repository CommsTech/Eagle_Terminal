"""Chief AI module for Eagle Terminal.

This module contains the Chief class, which serves as the main interface
for AI-powered features in Eagle Terminal, including natural language
processing, command suggestions, and system analysis.
"""

import asyncio
import json
import logging
from functools import lru_cache
from typing import Any, Dict, List

import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from utils.logger import logger

from .ai_prompts import CHIEF_SYSTEM_PROMPT
from .command_analyzer import CommandAnalyzer
from .command_learner import CommandLearner
from .command_suggester import CommandSuggester
from .data_preprocessor import DataPreprocessor
from .device_manager import DeviceManager
from .error_handler import error_handler
from .evaluation_metrics import calculate_metrics, calculate_perplexity
from .keyword_extractor import KeywordExtractor
from .keyword_manager import KeywordManager
from .knowledge_manager import KnowledgeManager
from .model_manager import ModelManager
from .performance_optimizer import PerformanceOptimizer
from .response_generator import ResponseGenerator
from .security import SecurityManager


class Chief:
    """Main class for managing AI-powered features in Eagle Terminal."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logger
        self.model_manager = ModelManager(config)
        self.data_preprocessor = DataPreprocessor(self.model_manager.tokenizer)
        self.response_generator = ResponseGenerator(
            self.model_manager, self.data_preprocessor
        )
        self.command_history = []
        self.command_learner = None  # Initialize this in the async method

    async def initialize(self):
        try:
            await self._initialize_components()
        except Exception as e:
            self.logger.error(f"Failed to initialize Chief: {str(e)}")
            self.model_manager = None
            self.data_preprocessor = None
            self.response_generator = None

    async def _initialize_components(self):
        if self.model_manager and self.model_manager.is_model_loaded():
            # Initialize other components
            self.knowledge_manager = KnowledgeManager(self.config.get("user_id"))
            self.keyword_manager = KeywordManager(self.config.get("user_id"))
            self.device_manager = DeviceManager()
            self.command_analyzer = CommandAnalyzer()
            self.command_suggester = CommandSuggester()
            self.security_manager = SecurityManager()
            self.performance_optimizer = PerformanceOptimizer()
            self.keyword_extractor = KeywordExtractor()
            self.command_learner = CommandLearner()
            await self.command_learner.create_table()

            # Enhanced NLP components
            self.ner_pipeline = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                device=self.model_manager.device,
            )
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis", device=self.model_manager.device
            )
            self.sentence_transformer = SentenceTransformer(
                "paraphrase-MiniLM-L6-v2"
            ).to(self.model_manager.device)

            self.logger.info("Chief components initialized successfully")
        else:
            self.logger.warning(
                "Chief components not initialized due to missing model manager or unloaded model"
            )

    def is_functional(self):
        return (
            self.model_manager is not None
            and self.model_manager.is_model_loaded()
            and self.response_generator is not None
        )

    def load_models(self):
        """Load all necessary AI models."""
        self.model_manager.load_model()
        self.logger.info(f"Loaded AI model: {self.model_manager.model_name}")

    @error_handler.handle_error
    async def analyze_command_output(
        self, command: str, output: str, os_type: str
    ) -> Dict[str, Any]:
        try:
            context = {
                "command": command,
                "output": output,
                "os_type": os_type,
                "command_history": self.command_history[-5:],
            }
            prompt = (
                f"Analyze the command '{command}' and its output. "
                f"Provide a concise summary of the information shown, "
                f"highlighting any important details or potential issues."
            )
            analysis = await self.response_generator.generate_response_async(
                prompt, context
            )
            self.command_history.append(command)
            return {"basic_analysis": analysis}
        except Exception as e:
            self.logger.error(f"Error analyzing command output: {str(e)}")
            return {"basic_analysis": f"Error analyzing command output: {str(e)}"}

    async def suggest_next_command(
        self, command_history: List[str], device_info: Dict[str, str]
    ) -> str:
        try:
            context = {
                "command_history": command_history[-5:],
                "device_info": device_info,
            }
            prompt = (
                f"Suggest a single, concise Linux command to run next based on this context: {context}. "
                f"Also, provide a brief explanation of why this command is suggested."
            )
            suggestion = await self.response_generator.generate_response_async(
                prompt, context
            )
            return suggestion
        except Exception as e:
            self.logger.error(f"Error suggesting next command: {str(e)}")
            return "Unable to suggest next command due to an error."

    async def _async_pipeline(self, pipeline, input_text):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, pipeline, input_text)

    async def _async_encode(self, text):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.sentence_transformer.encode, [text]
        )

    async def direct_interaction(self, query: str, device_info: Dict[str, Any]) -> str:
        try:
            context = {
                "query": query,
                "device_info": device_info,
                "command_history": self.command_history[-5:],
            }
            prompt = f"Respond to the user query: {query}"
            response = await self.response_generator.generate_response_async(
                prompt, context
            )
            return response
        except Exception as e:
            self.logger.error(f"Error in direct interaction: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"

    async def _get_command_help(self, command: str) -> str:
        # This method would typically run the command with --help or -h flag
        # For demonstration, we'll return a mock help text for 'ip a'
        if command.startswith("ip a"):
            return (
                "Usage: ip [ OPTIONS ] OBJECT { COMMAND | help }\n"
                "ip addr { add | del } IFADDR dev IFNAME\n"
                "IFADDR := PREFIX | ADDR peer PREFIX [ broadcast ADDR ] [ anycast ADDR ]\n"
                "          [ label LABEL ] [ scope SCOPE-ID ]\n"
                "SCOPE-ID := [ host | link | global | NUMBER ]\n"
            )
        return "No help information available for this command."
