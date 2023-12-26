# Eagle_Terminal
Eagle Term: Python SSH/Serial Client for secure remote connections with multi-tab support.

**Note this is a Work in progress, Any help welcome!

Eagle Term is a versatile Python-based SSH/Serial Client that allows users to establish secure connections with remote devices using SSH or serial communication protocols. With its intuitive user interface and support for multiple connection tabs, Eagle Term offers a convenient and efficient way to manage and interact with multiple devices simultaneously. With the goal of predictive command input and LLM (Language Model) support, Eagle Term aims to enhance the user experience by providing intelligent command suggestions and language model integration. Whether you need to remotely access servers, network devices, or embedded systems, Eagle Term provides a seamless and reliable solution for secure remote communication. It offers features such as command execution, file transfer, and session management, making it an essential tool for network administrators, developers, and anyone working with remote devices.

## Getting Started
This document will guide you on how to install and use EagleTerm_v0.1

## Features
- Create and manage network connections
- Check the status of network devices
- Perform network operations such as ping and traceroute
- Utilizes the mistral-7b-instruct-v0.1.Q4_0.gguf gpt4all model

## Installation
1. Clone the repository: `git clone https://github.com/your-username/Eagle_Terminal.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Download the Model from https://gpt4all.io/models/gguf/mistral-7b-instruct-v0.1.Q4_0.gguf and move it into the /Chief/Model/ folder

## Usage
1. Run the application: `python Eagle_Terminal.py`
2. The main window will open, showing different tabs for managing network connections.
3. Navigate to the "Connections" tab to create and manage network connections.
4. Use the provided buttons and forms to add, edit, or delete network connections.
5. Perform network operations using the available options.
6. View the status of network devices and perform troubleshooting tasks.

## File Structure
- `Eagle_Terminal.py`: The main entry point of the application.
- `Chief/Chief_AI.py`: Contains the AI chat functionality.
- `Functions/device_status.py`: Implements network status checking functions.
- `ConnectionTab.py`: Defines the ConnectionTab class, responsible for managing network connections.
- `devices.csv`: CSV file containing the list of network devices.
- `requirements.txt`: Contains the required Python dependencies.

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any inquiries or questions, please contact commstech@commsnet.org.
