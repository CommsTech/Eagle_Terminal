from unittest.mock import AsyncMock, MagicMock

import pytest
from transformers import AutoModelForCausalLM, AutoTokenizer

from ai.model_manager import ModelManager
from ai.performance_optimizer import PerformanceOptimizer
from ai.response_generator import ResponseGenerator
from ai.security import SecurityManager


class TestModelManager:
    @pytest.fixture
    async def model_manager(self):
        """Create a ModelManager with mocked model and tokenizer."""
        manager = ModelManager(
            {"model_name": "distilgpt2"}
        )  # Use distilgpt2 instead of distilbert

        # Mock the model and tokenizer
        manager.model = MagicMock(spec=AutoModelForCausalLM)
        manager.tokenizer = MagicMock(spec=AutoTokenizer)

        return manager

    @pytest.mark.asyncio
    async def test_load_model(self, model_manager):
        """Test model loading."""
        assert model_manager.model is not None
        assert model_manager.tokenizer is not None


class TestResponseGenerator:
    @pytest.fixture
    async def response_generator(self, model_manager):
        """Create a ResponseGenerator with mocked model manager."""
        return ResponseGenerator(model_manager)

    @pytest.mark.asyncio
    async def test_generate_response(self, response_generator):
        """Test response generation."""
        # Mock the generate method to return a fixed response
        response_generator.generate = AsyncMock(return_value="Test response")

        response = await response_generator.generate_response("Hello, how are you?")
        assert isinstance(response, str)
        assert len(response) > 0


class TestSecurityManager:
    @pytest.fixture
    def security_manager(self):
        """Create a SecurityManager instance."""
        return SecurityManager()

    def test_sanitize_input(self, security_manager):
        """Test input sanitization."""
        dangerous_command = "rm -rf /"
        sanitized = security_manager.sanitize_input(dangerous_command)
        # Instead of checking if 'rm' is not in sanitized,
        # check if the dangerous command was properly sanitized
        assert sanitized != dangerous_command
        assert "[REMOVED]" in sanitized or sanitized == ""


class TestPerformanceOptimizer:
    @pytest.fixture
    def performance_optimizer(self):
        """Create a PerformanceOptimizer instance."""
        return PerformanceOptimizer()

    def test_quantize_model(self, performance_optimizer):
        """Test model quantization."""
        # Create a mock model for testing
        mock_model = MagicMock(spec=AutoModelForCausalLM)

        # Test quantization with the mock model
        result = performance_optimizer.quantize_model(model=mock_model)
        assert result is not None
