import json
import os
from typing import Dict, List

import requests

from ai.chief import Chief


# Load secrets from a JSON file
def load_secrets() -> Dict[str, str]:
    secrets_path = os.path.join(
        os.path.dirname(__file__), "..", "open_webui_secrets.json"
    )
    if not os.path.exists(secrets_path):
        url = input("Enter the Open-Webui URL: ")
        jwt_token = input("Enter the JWT token: ")
        api_key = input("Enter the API key: ")
        secrets = {"url": url, "jwt_token": jwt_token, "api_key": api_key}
        with open(secrets_path, "w") as f:
            json.dump(secrets, f)
    else:
        with open(secrets_path, "r") as f:
            secrets = json.load(f)
    return secrets


# Function to interact with Open-Webui agents
def query_agents(prompt: str, secrets: Dict[str, str]) -> str:
    headers = {
        "Authorization": f"Bearer {secrets['jwt_token']}",
        "Content-Type": "application/json",
    }
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "mode": "chat",
        "character": "mixture",  # Assuming this targets the mixture of agents
    }
    response = requests.post(f"{secrets['url']}/api/chat", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["message"]
    else:
        return f"Error: {response.status_code} - {response.text}"


# List of prompts for different scenarios
prompts = [
    "What are the most common network troubleshooting commands for Linux systems?",
    "How do you diagnose slow network performance on a Windows server?",
    "Explain the process of setting up a VLAN on a Cisco switch.",
    "What steps would you take to troubleshoot a DNS resolution issue?",
    "How do you configure and test an IPsec VPN tunnel between two Palo Alto firewalls?",
    "Describe the process of load balancing web servers using NGINX.",
    "What commands would you use to investigate high CPU usage on a Linux server?",
    "How do you set up and manage a Docker container network?",
    "Explain the steps to configure BGP routing on a Juniper router.",
    "What are the best practices for securing a public-facing web server?",
]


def run_learning_session(chief: Chief):
    secrets = load_secrets()
    print("Starting Chief's learning session with Open-Webui agents...")

    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        agent_response = query_agents(prompt, secrets)
        print(f"Agent Response: {agent_response}")

        # Let Chief analyze and learn from the response
        chief_analysis = chief.analyze_and_learn(prompt, agent_response)
        print(f"Chief's Analysis: {chief_analysis}")

        # Optional: Ask Chief to generate a related question or command
        follow_up = chief.generate_follow_up(prompt, agent_response)
        print(f"Chief's Follow-up: {follow_up}")

        # Query agents with the follow-up
        follow_up_response = query_agents(follow_up, secrets)
        print(f"Agent Response to Follow-up: {follow_up_response}")

        # Let Chief learn from the follow-up interaction
        chief.analyze_and_learn(follow_up, follow_up_response)

    print("\nLearning session completed. Chief has updated its knowledge base.")


# This function can be called from within the application when needed
def start_learning_session(chief: Chief):
    run_learning_session(chief)


if __name__ == "__main__":
    # This block will only run if the script is executed directly
    print(
        "This script is not meant to be run directly. Please use it from within the Eagle Terminal application."
    )
