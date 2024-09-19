## Eagle Terminal: Secure Remote Access and AI-Assisted Networking

Eagle Terminal is a Python-based application designed for establishing secure connections to remote devices via SSH or serial communication.  It provides a user-friendly interface for managing multiple connections, executing commands, and interacting with devices.

### Features:

* **Secure Remote Access:**  Connect to remote devices via SSH or serial protocols.  
* **Multiple Connections:**  Open and manage multiple connection tabs simultaneously for efficient device management.
* **Command Execution:**  Execute commands on remote devices through the terminal interface.
* **AI-Assisted Networking:**  Leverage an integrated language model (GPT-4All) for assistance with network tasks, troubleshooting, and command suggestions.

### Usage:

1. **Installation:**
   * Clone the repository: `git clone https://github.com/your-username/Eagle_Terminal.git`
   * Install dependencies: `pip install -r requirements.txt`
   * Download the GPT-4All model: `https://gpt4all.io/models/gguf/mistral-7b-instruct-v0.1.Q4_0.gguf` and move it into the `/Chief/Model/` folder.
2. **Run the Application:** `python Eagle_Terminal.py`
3. **Connection Management:**
   * Navigate to the "Connections" tab to create and manage connections.
   * Configure devices with their details (label, connection type, host).
4. **Remote Interaction:**
   * Connect to a device by clicking its button.
   * Enter commands in the terminal window and send them to the device.
   * Use the "Ask Chief" button to interact with the AI for network-related assistance.

### File Structure:

* **Eagle_Terminal.py:** Main application entry point.
* **Chief/Chief_AI.py:** AI chat functionality for network assistance.
* **Functions/device_status.py:** Functions to check device network status.
* **UI/Chat_Tab.py:** UI for the chat tab.
* **UI/Connection_Tab.py:** UI for managing connections.
* **UI/main_window.py:** Main window UI with tab control.
* **UI/ssh_tab.py:** UI for SSH connection tabs.
* **commands.csv:**  CSV file for common network commands.
* **devices.csv:** CSV file to store device connection information.
* **requirements.txt:** List of required Python packages.

### Contributing:

Contributions are welcome! Please open an issue or submit a pull request for suggestions, bug reports, or feature requests.

### License:

This project is licensed under the MIT License.