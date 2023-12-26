try:
    import gpt4all
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gpt4all'])
    import gpt4all
from pathlib import Path
from gpt4all import GPT4All
import os


class Chief:
    def __init__(self):
        self.model_name = 'mistral-7b-instruct-v0.1.Q4_0.gguf'
        if 'Eagle_Terminal' in str(Path.cwd ()):
            self.model_path = Path.cwd() / 'Chief' / 'Model'
            print('Loading GPT4ALL Model: '+str(self.model_name))
        else:
            print('Model Not Found')
            print('check your path')
            print('current path is: '+str(Path.cwd() / 'Chief' / 'Model'))
            pass
        self.model = GPT4All(model_name=str(self.model_path / self.model_name))
        system_prompt = "### System: Adopt a persona of a Senior Network Engineer named Chief. A seasoned network operations engineer, your role is to assist and mentor new engineers in a variety of network-related tasks while ensuring the safety and stability of the network infrastructure. Your expertise lies in troubleshooting, configuring, and optimizing network devices via SSH. Your goal is to provide comprehensive guidance and support to ensure the smooth operation of connected devices, while adhering to best practices and avoiding actions that may compromise the network. Tap into your experience and knowledge to help new engineers navigate network challenges, resolve issues, and optimize network performance, always prioritizing the safety and integrity of the network."
        building_prompt = self.model.generate(system_prompt)
        print('Model Loaded: '+str(self.model_name))
        print(building_prompt)
        pass

    def quick_prompt(self, ai_question_entry):
        ai_prompt = "### User: " + ai_question_entry
#        print(ai_prompt)
        ai_response = self.model.generate(ai_prompt, max_tokens=80, temp=0.3)
#        print(ai_response)
        return ai_response
        pass
    def chat():
        with model.chat_session():
            response1 = self.model.generate(prompt='hello', temp=0)
            response2 = self.model.generate(prompt='write me a short poem', temp=0)
            response3 = self.model.generate(prompt='thank you', temp=0)
            print(model.current_chat_session)
            pass
    def generate(self):
        return self.model.generate()
