from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eagle-terminal",
    version="1.0.0",
    author="CommsTech",
    author_email="support@commsnet.org",
    description="An advanced, AI-assisted SSH/Serial client with Ansible support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CommsTech/Eagle_Terminal",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Business Source License 1.1 (BSL-1.1)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt5>=5.15.4",
        "qasync>=0.23.0",
        "asyncssh>=2.11.0",
        "paramiko>=2.7.2",
        "transformers>=4.18.0",
        "torch>=1.10.0",
        "scikit-learn>=0.24.2",
        "numpy>=1.21.0",
        "requests>=2.26.0",
    ],
    entry_points={
        "console_scripts": [
            "eagle-terminal=Eagle_Terminal:run_main",
        ],
    },
)
