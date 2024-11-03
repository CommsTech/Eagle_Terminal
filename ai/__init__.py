"""AI module for Eagle Terminal.

This module contains the core AI components used in Eagle Terminal,
including the Chief, KnowledgeManager, ModelManager, ResponseGenerator,
KeywordManager, DeviceManager, CommandAnalyzer, and CommandLearner
classes.
"""

from .chief import Chief
from .command_analyzer import CommandAnalyzer
from .command_learner import CommandLearner
from .device_manager import DeviceManager
from .keyword_manager import KeywordManager
from .knowledge_manager import KnowledgeManager
from .model_manager import ModelManager
from .response_generator import ResponseGenerator
from .security import SecurityManager

__all__ = [
    "Chief",
    "KnowledgeManager",
    "ModelManager",
    "ResponseGenerator",
    "KeywordManager",
    "DeviceManager",
    "CommandAnalyzer",
    "CommandLearner",
    "SecurityManager",
]
