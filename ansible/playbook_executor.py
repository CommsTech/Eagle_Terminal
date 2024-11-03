"""Ansible Playbook Executor module for Eagle Terminal.

This module contains the AnsiblePlaybookExecutor class, which is
responsible for running Ansible playbooks and handling their output
within the Eagle Terminal environment.
"""

import os
import tempfile

from utils import logger

try:
    import ansible_runner
except ImportError:
    ansible_runner = None
    logger.warning(
        "ansible_runner is not installed. Ansible functionality will be limited."
    )


class AnsiblePlaybookExecutor:
    def run_playbook(self, playbook_path, host):
        if ansible_runner is None:
            return "Error: ansible_runner is not installed. Please install it to use this feature."

        with tempfile.TemporaryDirectory() as temp_dir:
            inventory_file = os.path.join(temp_dir, "inventory")
            with open(inventory_file, "w") as f:
                f.write(f"{host} ansible_connection=ssh\n")

            r = ansible_runner.run(
                private_data_dir=temp_dir,
                playbook=playbook_path,
                inventory=inventory_file,
                verbosity=3,
                json_mode=True,
            )

            output = []
            for event in r.events:
                if event["event"] == "runner_on_ok":
                    task = event["event_data"]["task"]
                    result = event["event_data"]["res"]
                    output.append(f"Task: {task}")
                    output.append(f"Result: {result}")
                    output.append("---")
                elif event["event"] == "runner_on_failed":
                    task = event["event_data"]["task"]
                    result = event["event_data"]["res"]
                    output.append(f"Task: {task}")
                    output.append(f"Failed: {result}")
                    output.append("---")

            return "\n".join(output)
