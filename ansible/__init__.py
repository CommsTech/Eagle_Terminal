"""Ansible integration module for Eagle Terminal.

This module provides functionality to interact with Ansible, including
playbook execution and ad-hoc command support.
"""

from .playbook_executor import AnsiblePlaybookExecutor

__all__ = ["AnsiblePlaybookExecutor"]
