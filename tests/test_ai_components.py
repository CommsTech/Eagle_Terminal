import pytest

from ai.model_manager import ModelManager
from ai.performance_optimizer import PerformanceOptimizer
from ai.response_generator import ResponseGenerator
from ai.security import SecurityManager


class TestModelManager:
    @pytest.fixture
    def model_manager(self):
        return ModelManager({"model_name": "distilbert-base-uncased"})

    def test_load_model(self, model_manager):
        model_manager.load_model()
        assert model_manager.model is not None
        assert model_manager.tokenizer is not None


class TestResponseGenerator:
    @pytest.fixture
    def response_generator(self):
        model_manager = ModelManager({"model_name": "distilbert-base-uncased"})
        model_manager.load_model()
        return ResponseGenerator(model_manager)

    def test_generate_response(self, response_generator):
        response = response_generator.generate_response("Hello, how are you?")
        assert isinstance(response, str)
        assert len(response) > 0


class TestSecurityManager:
    @pytest.fixture
    def security_manager(self):
        return SecurityManager()

    def test_sanitize_input(self, security_manager):
        sanitized = security_manager.sanitize_input("rm -rf /")
        assert "rm" not in sanitized


class TestPerformanceOptimizer:
    @pytest.fixture
    def performance_optimizer(self):
        return PerformanceOptimizer()

    def test_quantize_model(self, performance_optimizer):
        # This is a placeholder test. Actual implementation may vary.
        assert performance_optimizer.quantize_model() is not None
