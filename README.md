# Eagle Terminal

Eagle Terminal is an all-in-one SSH client and network diagnostic tool, designed to provide a comprehensive solution for network administrators and IT professionals.

## Recent Updates

- Improved asynchronous operations for better performance and responsiveness
- Enhanced error handling and logging
- Upgraded SSH connection handling with asyncssh
- Separated Chief's AI analysis output into a dedicated area for better visibility
- Implemented a more robust file browser for remote systems
- Added Local AI configuration dialog
- Improved theme management for consistent UI across the application
- Enhanced session management with better connection and disconnection handling
- Implemented quick connect functionality for faster SSH connections

## Features

Currently implemented:
- Multi-protocol support:
  - SSH (Secure Shell) with asyncssh
  - Serial connections
- AI-powered assistance:
  - Efficient AI model (DistilBERT) for terminal operations
  - Command suggestions and explanations based on context
  - Output analysis and insights for system information
  - Troubleshooting recommendations
  - Continuous learning from user interactions and device outputs
- Built-in knowledge base:
  - Local note-taking system (wiki-style)
  - Integration of device-specific notes with AI recommendations
- Advanced terminal management:
  - Multi-tab interface for managing multiple connections
  - Split-screen view for simultaneous sessions
  - Improved file browser for remote systems
  - Customizable themes and layouts
- Improved error handling and logging
- Enhanced settings management with import/export functionality
- Optimized AI model loading and usage
- Quick connect functionality for rapid SSH connections
- Customizable themes and layouts
- Plugin system for extensibility
- Continuous learning from user interactions
- Asynchronous operations for improved responsiveness

Planned features:
- Telnet support
- RDP (Remote Desktop Protocol) support

## Installation

### For End Users

1. Download the latest release from our [releases page](https://github.com/CommsNet/Eagle_Terminal/releases).
2. Run the installer appropriate for your operating system.
3. Follow the on-screen instructions to complete the installation.

### For Developers

#### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Qt 5.15 or higher (for PyQt5)

#### Steps

1. Clone the repository:
   ```
   https://git.commsnet.org/commstech/eagle_terminal.git
   ```

   GitHub repo (not always current)
   ```
   git clone https://github.com/CommsTech/Eagle_Terminal.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python Eagle_Terminal.py
   ```

## Usage

1. Launch Eagle Terminal
2. Use the "New Connection" or "Quick Connect" feature to start a new SSH or Serial session
3. Enter the connection details
4. Once connected, use the terminal as you would any other SSH or Serial client
5. Utilize the AI-powered features for command suggestions and system analysis

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

Eagle Terminal is licensed under the Business Source License 1.1 (BSL 1.1). See the [LICENSE](LICENSE) file for details.

## Contact

For questions, suggestions, or support, please open an issue on the GitHub repository or contact the maintainer at [support@commsnet.org].

## File Structure
