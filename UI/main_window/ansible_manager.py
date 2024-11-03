import json
import os

import ansible_runner

from utils.logger import logger


class AnsibleManager:
    def __init__(self, inventory_path=None):
        self.runner = None
        self.inventory_path = inventory_path or "/etc/ansible/hosts"

    def run_playbook(self, playbook_path, inventory_path=None, extra_vars=None):
        try:
            inventory = inventory_path or self.inventory_path
            self.runner = ansible_runner.run(
                playbook=playbook_path, inventory=inventory, extravars=extra_vars
            )
            return self.runner.status, self.runner.rc
        except Exception as e:
            logger.error(f"Error running Ansible playbook: {str(e)}")
            return "failed", -1

    def get_output(self):
        if self.runner:
            return self.runner.stdout.read()
        return None

    def cancel_run(self):
        if self.runner:
            self.runner.cancel()

    def list_playbooks(self, playbook_dir):
        playbooks = []
        for file in os.listdir(playbook_dir):
            if file.endswith(".yml") or file.endswith(".yaml"):
                playbooks.append(file)
        return playbooks

    def get_inventory(self):
        try:
            with open(self.inventory_path, "r") as f:
                return f.read()
        except IOError as e:
            logger.error(f"Error reading inventory file: {str(e)}")
            return None

    def update_inventory(self, new_inventory):
        try:
            with open(self.inventory_path, "w") as f:
                f.write(new_inventory)
        except IOError as e:
            logger.error(f"Error updating inventory file: {str(e)}")

    def get_task_status(self):
        if self.runner:
            return self.runner.status
        return None
