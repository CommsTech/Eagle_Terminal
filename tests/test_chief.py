import unittest
from unittest.mock import MagicMock
import pytest
from ai.chief import Chief
from ai.command_analyzer import CommandAnalyzer
from ai.command_learner import CommandLearner

class TestChief(unittest.TestCase):
    def setUp(self):
        config = {"model_name": "distilgpt2", "max_length": 512}
        self.chief = Chief(config=config)
        self.chief.command_analyzer = MagicMock(spec=CommandAnalyzer)
        self.chief.command_learner = MagicMock(spec=CommandLearner)
        self.chief.response_generator = MagicMock()

    def test_analyze_command_output(self):
        command = "ls -l"
        output = "total 0\n-rw-r--r-- 1 user group 0 May 1 12:00 file.txt"
        os_type = "linux"
        expected_analysis = "Command executed: ls -l\nThe command executed successfully."
        self.chief.command_analyzer.analyze_command_output.return_value = expected_analysis

        analysis = self.chief.analyze_command_output(command, output, os_type)
        self.assertEqual(analysis, expected_analysis)
        self.chief.command_analyzer.analyze_command_output.assert_called_once_with(
            command, output, os_type
        )

    def test_suggest_next_command(self):
        command_history = ["ls", "cd /home", "pwd"]
        device_info = {"os": "Linux", "distribution": "Ubuntu"}
        expected_suggestion = "Suggested command: pwd\n\nExplanation: This command shows the current working directory."
        
        self.chief.command_learner.suggest_next_command = MagicMock(return_value="pwd")
        self.chief.command_analyzer.explain_command.return_value = (
            "This command shows the current working directory."
        )

        suggestion = self.chief.suggest_next_command(command_history, device_info)
        self.assertEqual(suggestion, expected_suggestion)
        self.chief.command_learner.suggest_next_command.assert_called_once_with(
            command_history, device_info
        )
