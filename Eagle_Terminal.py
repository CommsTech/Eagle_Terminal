import csv
import subprocess
import sys
import tkinter as tk
import Functions.device_status as device_status
from Chief.Chief_AI import Chief
from tkinter import ttk, messagebox, Scrollbar, Text, Entry
try:
    import paramiko
    import serial
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'paramiko', 'pyserial', 'psutil'])
    import paramiko
    import serial
    import psutil
from serial.tools.list_ports import comports

# Enable for debugging
#import logging
#logging.basicConfig(level=logging.DEBUG)

#define the commands file for quick access
commands_file = 'commands.csv'
Chief = Chief()

class ConnectionTab:
    def __init__(self, parent, notebook):
        """
        Initializes the Connections tab within the parent notebook.
        
        Args:
            parent (ttk.Notebook): The parent notebook widget.
            notebook (ttk.Notebook): The notebook widget to which this tab will be added.
        
        Returns:
            None: This method doesn't return anything.
        """
        self.parent = notebook
        self.notebook = notebook
        self.tab = ttk.Frame(self.parent)
        self.notebook.add(self.tab, text="Connections")
        self.devices = self.read_devices_file('devices.csv')
        self.create_userpass_widgets()
        self.create_ssh_widgets()
        self.create_serial_widgets()
        self.create_configure_button()

    def create_userpass_widgets(self):
        """
        Creates and packs username and password input widgets for the user interface.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, it modifies the instance attributes.
        """
        self.username_label = ttk.Label(self.tab, text="Username:")
        self.username_label.pack()

        self.username_entry = ttk.Entry(self.tab)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(self.tab, text="Password:")
        self.password_label.pack()

        self.password_entry = ttk.Entry(self.tab, show="*")
        self.password_entry.pack(pady=5)

    def read_devices_file(self, filename):
        """Reads device information from a CSV file.
        
        Args:
            filename (str): The path to the CSV file containing device information.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents a device with its properties.
                  Returns an empty list if the file is not found or cannot be read.
        """
        try:
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                devices = list(reader)
                return devices
        except FileNotFoundError as e:
            error_message = f"Error: Failed to open '{filename}': {str(e)}"
            messagebox.showerror("File Not Found", error_message)
            return []

    def create_ssh_widgets(self):
        # Get the status for the current device
        """Create SSH widgets for each device in the list.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, it creates and packs widgets directly.
        """        for device in self.devices:
            # Create the device widget
            device_widget = ttk.Frame(self.tab)
            device_widget.pack()
            device_label = device['device_label']
            connection_type = device['connection_type']
            host = device['host']
            status = device_status.get_status(host)

            if connection_type == 'SSH':
                button_text = f"{device_label} - {connection_type} {host} ({status['status']})"
                button = self.create_button(self.tab, button_text, self.select_connection, connection_type=connection_type, host=host)

    def create_serial_widgets(self):
        # Creates serial widgets based on the devices in the self.devices list.
        """Creates serial widgets for devices with 'Serial' connection type.
"""
Creates and packs a button widget with the specified text and command.

Args:
    """
    Selects and establishes a connection based on the provided connection type and parameters.
    
    Args:
        self: The instance of the class containing this method.
        **kwargs: dict: Additional keyword arguments for connection parameters.
    
    Returns:
        None: This method doesn't return a value, but it performs various actions based on the connection type.
    """
    parent (tk.Widget): The parent widget to which the button will be added.
    text (str): The text to be displayed on the button.
    command (callable): The function to be called when the button is clicked.
    **kwargs: Additional keyword arguments to be passed to the command function.

Returns:
    None: This method doesn't return anything, but creates and packs a button widget.
"""
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method does not return any value.
        """
        for row in self.devices:
            device_label = row['device_label']
            connection_type = row['connection_type']
            host = row['host']
            if connection_type == 'Serial':
                button_text = f"{device_label} - {connection_type} {host}"
                self.create_button(self.tab, button_text, self.select_connection, connection_type=connection_type, host=host)
    def create_button(self, parent, text, command, **kwargs):
        button = ttk.Button(parent, text=text, command=lambda: command(**kwargs))
        button.pack()

    def select_connection(self, **kwargs):
        username = self.username_entry.get()
        """Sends a command to either an SSH client or an AI assistant and displays the output.
        
        Args:
            output_text (tk.Text): The text widget to display the command output.
            command_entry (tk.Entry): The entry widget containing the command to be sent.
            ssh_client (paramiko.SSHClient, optional): The SSH client to execute commands on. Defaults to None.
            ai_question_entry (str, optional): The entry widget for AI-related questions. Defaults to None.
        
        Returns:
            None: This function doesn't return a value, it updates the GUI directly.
        """
        password = self.password_entry.get()
        host = kwargs.get("host")
        connection_type = kwargs.get("connection_type")

        if connection_type == "Serial":
            port = kwargs.get("port")
            baudrate = kwargs.get("baudrate")
            print(f"Selected Serial connection with port {port} and baudrate {baudrate}")
            print(f"Username: {username}")
            print(f"Password: {password}")
        elif connection_type == "SSH":
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host, username=username, password=password)
            ssh_session_tab = ttk.Frame(self.notebook)
            self.notebook.add(ssh_session_tab, text=f"SSH - {host}")
            output_text = tk.Text(ssh_session_tab)
            output_text.pack(fill=tk.BOTH, expand=True)
            command_entry = tk.Entry(ssh_session_tab)
            command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            send_button = tk.Button(ssh_session_tab, text="Send", command=lambda: send_command(output_text, command_entry, ssh_client))
            send_button.pack(side=tk.LEFT)
            transport = ssh_client.get_transport()
            hostname = transport.getpeername()[0]
            ai_question_entry = None

            def send_command(output_text, command_entry, ssh_client=None, ai_question_entry=None):
                command = command_entry.get()

                if not command:
                    return

                if "Chief" in command:
                    ai_question_entry = command
                    output_text.insert(tk.END, "User: " + ai_question_entry + "\n")
                    if ai_question_entry:
                        ai_response= Chief.quick_prompt(ai_question_entry)
                        output_text.insert(tk.END, "Chief: " + ai_response + "\n")
                else:
                    # Handle command
                    stdin, stdout, stderr = ssh_client.exec_command(command)
                    # Read the output in chunks
                    output = ""
                    for line in stdout:
                        output += line.strip() + "\n"
                    for line in stderr:
                        output += line.strip() + "\n"
                    output_text.insert(tk.END, hostname + output + "\n")

                output_text.see(tk.END)

                command_entry.delete(0, tk.END)
                command_entry.focus_set()

            command_entry.bind("<Return>", lambda event: send_command(output_text, command_entry, ssh_client, ai_question_entry))
            self.parent.mainloop()
            ssh_client.close()
        else:
            print("Invalid connection type")

    def create_configure_button(self):
        """Creates and configures a button for custom connection configuration.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, it creates and packs a button widget.
        """
        configure_button = ttk.Button(self.tab, text="Configure Custom Connection", command=self.configure_custom_connection)
        configure_button.pack()

    def configure_custom_connection(self):
        """Configures a custom connection by creating a new window for user input.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, but it creates a new window,
            adds the entered device to the devices list, creates a new button for the device,
            and saves the device information to a CSV file.
        """
        custom_window = tk.Toplevel(self.parent)
        custom_window.title("Custom Connection")

        # Create and pack the labels and entry fields
        ttk.Label(custom_window, text="Device Label:").pack()
        device_label_entry = ttk.Entry(custom_window)
        device_label_entry.pack()

        ttk.Label(custom_window, text="Connection Type:").pack()
        connection_type_var = tk.StringVar(value="SSH")
        connection_type_dropdown = ttk.Combobox(custom_window, textvariable=connection_type_var, values=["SSH", "Serial"])
        connection_type_dropdown.pack()

        ttk.Label(custom_window, text="Host:").pack()
        host_entry = ttk.Entry(custom_window)
        host_entry.pack()

        # Function to save the device information
        def save_device():
            """Saves a new device to the application's device list and CSV file.
            
            Args:
                None
            
            Returns:
                None: This function doesn't return anything, but it performs the following actions:
                    - Adds the device information to the devices list
                    - Creates a button for the device in the UI
                    - Appends the device information to the 'devices.csv' file
                    - Closes the custom window used for input
            """
            device_label = device_label_entry.get()
            connection_type = connection_type_var.get()
            host = host_entry.get()

            # Append the device information to the devices list
            self.devices.append({
                'device_label': device_label,
                'connection_type': connection_type,
                'host': host
            })

            # Create the device button
            button_text = f"{device_label} - {connection_type} {host}"
            self.create_button(self.tab, button_text, self.select_connection, connection_type=connection_type, host=host)

            # append the device information to the devices.csv file
            with open('devices.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['device_label', 'connection_type', 'host'])
                writer.writerow({
                    'device_label': device_label,
                    'connection_type': connection_type,
                    'host': host
                })
            # Close the custom window
            custom_window.destroy()
        # Create and pack the save button
        save_button = ttk.Button(custom_window, text="Save", command=save_device)
        save_button.pack()
    
        custom_window.mainloop()

    def set_username_placeholder(self):
        """Sets a placeholder text in the username entry field if it's empty.
        
        Args:
            self: The instance of the class containing this method.
"""Sets a placeholder text for the password entry field.

This method checks if the password entry field is empty and inserts the
placeholder text "Password" if it is.

Args:
    self: The instance of the class containing this method.

Returns:
    None: This method doesn't return anything.
"""
        
        Returns:
            None: This method doesn't return anything.
        """        if not self.username_entry.get():
            self.username_entry.insert(0, "Username")

    def set_password_placeholder(self):
        if not self.password_entry.get():
            self.password_entry.insert(0, "Password")

gui_closed = False



def close_python_subprocesses():
    """Terminates all running Python subprocesses.
    
    """Handles the closing of the GUI window and performs cleanup tasks.
    
    Args:
        None
    
    Returns:
        None: This function doesn't return anything, but it performs several side effects:
            - Terminates the Chief_AI.py program
            - Sets a global flag indicating the GUI is closed
            - Destroys the root window
            - Closes Python subprocesses
    """
    This function iterates through all running processes, identifies those with the name
    "python.exe", and attempts to terminate them.
    
    Args:
        None
    
    Returns:
        None: This function does not return any value.
    """
    for proc in psutil.process_iter():
        try:
            if proc.name() == "python.exe":
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Call the close_python_subprocesses function in your on_closing function
def on_closing():
    global gui_closed

    # Terminate the Chief_AI.py program
    subprocess.call(["python", "Chief/Chief_AI.py", "terminate"])

    # Perform any necessary cleanup or finalization tasks here
    # ...
    
    # Set the flag indicating GUI window is closed
    gui_closed = True

    # Stop the main event loop
    root.destroy()

    # Close the Python subprocesses
    close_python_subprocesses()

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()

    # Set the window title
    root.title("Eagle Terminal_v0.2")

    # Set the window size
    root.geometry("800x600")

    # Create a notebook widget to hold the tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Create the tabs
    connection_tab = ConnectionTab(root, notebook)

    # Add the tabs to the notebook
    notebook.add(connection_tab.tab, text="Connections")

    # Bind the close event to the on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the main event loop
    root.mainloop()

    # Check if the GUI window is closed
    if gui_closed:
        # Perform any necessary cleanup or finalization tasks here
        # ...

        print("Closing program...")

        # Exit the program
        sys.exit()
    # End-of-file (EOF)