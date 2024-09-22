import subprocess
import sys
from pathlib import Path
from gpt4all import GPT4All

class Chief:
    """
    A class that represents the Chief AI.

    Attributes:
        model_name (str): The name of the GPT4All model.
        model_path (Path): The path to the GPT4All model.
        model (GPT4All): An instance of the GPT4All model.
    """

    def __init__(self):
        """Initializes the GPT4All model with a specific configuration.
        
        Args:
            None
        
        Returns:
            None: This method initializes the object and doesn't return anything.
        """
        self.model_name = 'mistral-7b-instruct-v0.1.Q4_0.gguf'
        if 'Eagle_Terminal' in str(Path.cwd()):
            self.model_path = Path.cwd() / 'Chief' / 'Model'
            print('Loading GPT4ALL Model: ' + str(self.model_name))
        else:
            print('Model Not Found')
            print('check your path')
            print('current path is: ' + str(Path.cwd() / 'Chief' / 'Model'))
            pass
        self.model = GPT4All(model_name=str(self.model_path / self.model_name))
        system_prompt = "### System: Adopt a persona of a Senior Network Engineer named Chief. As a seasoned network operations engineer, " \
                        "your role is to assist and mentor new engineers in a variety of network-related tasks while ensuring the " \
                        "safety and stability of the network infrastructure. Your expertise lies in troubleshooting, configuring, " \
                        "and optimizing network devices via SSH. Your goal is to provide comprehensive guidance and support to " \
                        "ensure the smooth operation of connected devices, while adhering to best practices and avoiding actions " \
                        "that may compromise the network. Tap into your experience and knowledge to help new engineers navigate " \
                        "network challenges, resolve issues, and optimize network performance, always prioritizing the safety and " \
                        "integrity of the network."
        building_prompt = self.model.generate(system_prompt)
        print('Model Loaded: ' + str(self.model_name))
        print(building_prompt)
        pass

    def quick_prompt(self, ai_question_entry):
        """
        Generates a quick AI response based on the given question.

        Parameters:
            ai_question_entry (str): The user's question.

        Returns:
            str: The AI's response.

        Raises:
            None
        """
        ai_prompt = "### User: " + ai_question_entry
        ai_response = self.model.generate(ai_prompt, max_tokens=80, temp=0.3)
        return ai_response
        pass

# End of Class