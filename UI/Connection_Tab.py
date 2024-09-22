import csv
import subprocess
import sys
import logging
import tkinter as tk
import Functions.device_status as device_status
from Chief.Chief_AI import Chief
from tkinter import ttk, messagebox, Scrollbar, Text, Entry
try:
    import paramiko
    import serial
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'paramiko', 'pyserial'])
    import paramiko
    import serial
from serial.tools.list_ports import comports


#logging.basicConfig(level=logging.DEBUG)

#define the commands file for quick access
commands_file = 'commands.csv'
Chief = Chief()

class ConnectionTab(ttk.Frame):
    def __init__(self, parent, notebook):
        """Initializes the Connections tab in the notebook.
        
        Args:
            parent (ttk.Notebook): The parent notebook widget.
            notebook (ttk.Notebook): The main notebook widget.
        
        Returns:
            None: This method doesn't return anything.
        """
        super().__init__(parent)
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
        # Define the Username Box
        ```
        """Creates and configures username and password input widgets for a user interface.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method does not return anything, it modifies the instance's attributes.
        """
        
        ```        self.username_label = ttk.Label(self.tab, text="Username:")
        self.username_label.pack()
        self.username_entry = ttk.Entry(self.tab)
        self.username_entry.pack(pady=5)
        # Define the Password Box
        self.password_label = ttk.Label(self.tab, text="Password:")
        self.password_label.pack()
        self.password_entry = ttk.Entry(self.tab, show="*")
        self.password_entry.pack(pady=5)

    def read_devices_file(self, filename):
        """Reads a CSV file containing device information and returns a list of devices.
        
        Args:
            filename (str): The path to the CSV file to be read.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents a device with its properties.
                  Returns an empty list if the file is not found or cannot be read.
        """        try:
            with open(filename) as file:
                reader = csv.DictReader(file)
                devices = list(reader)
                """
                Creates SSH widgets for each device in the device list.
                
                Args:
                    self: The instance of the class containing this method.
                
                Returns:
                    """
                    Selects and establishes a connection based on the provided connection type and parameters.
                    
                    Args:
                        self: The instance of the class containing this method.
                        **kwargs (dict): A dictionary of keyword arguments containing connection parameters.
                            Possible keys include:
                            - host (str): The hostname or IP address for SSH connection.
                            - connection_type (str): The type of connection ('Serial' or 'SSH').
                            - port (str): The port for Serial connection.
                            - baudrate (int): The baudrate for Serial connection.
                    
                    Returns:
                        None: This method doesn't return anything, but it performs the following actions:
                            - For Serial connection: Prints connection details.
                            - For SSH connection: Establishes an SSH connection, creates a new tab in the notebook
                              with an interactive terminal, and sets up the necessary GUI elements.
                            - For invalid connection types: Prints an error message.
                    """
                    None: This method doesn't return anything, it updates the GUI by creating widgets.
                """
                return devices
        except FileNotFoundError as e:
            error_message = f"Error: Failed to open '{filename}': {str(e)}"
            messagebox.showerror("File Not Found", error_message)
            return []

    def create_ssh_widgets(self):
        # Get the status for the current device
        for device in self.devices:
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
        """Creates serial connection widgets for devices with 'Serial' connection type.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, it creates buttons in the GUI.
        """        for row in self.devices:
            device_label = row['device_label']
            connection_type = row['connection_type']
            host = row['host']
            if connection_type == 'Serial':
                button_text = f"{device_label} - {connection_type} {host}"
                self.create_button(self.tab, button_text, self.select_connection, connection_type=connection_type, host=host)
    def create_button(self, parent, text, command, **kwargs):
        """Creates and packs a button widget with the specified text and command.
        
        Args:
            parent (tk.Widget): The parent widget to which the button will be added.
            text (str): The text to be displayed on the button.
            command (callable): The function to be called when the button is clicked.
            **kwargs: Additional keyword arguments to be passed to the command function.
        
        Returns:
            None: This method does not return anything, but it creates and packs a button widget.
        """
        button = ttk.Button(parent, text=text, command=lambda: command(**kwargs))
        button.pack()

    def select_connection(self, **kwargs):
        username = self.username_entry.get()
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
            """Sends a command to either an SSH client or an AI assistant and displays the output.
            
            Args:
                output_text (tk.Text): The text widget to display the command output.
                command_entry (tk.Entry): The entry widget containing the command to be sent.
                ssh_client (paramiko.SSHClient, optional): The SSH client to execute commands on. Defaults to None.
                ai_question_entry (str, optional): The entry for AI-related questions. Defaults to None.
            
            Returns:
                None: This function doesn't return anything, it updates the GUI directly.
            """            transport = ssh_client.get_transport()
            hostname = transport.getpeername()[0]
            ai_question_entry = None
##            if ai_question_entry:
##                ai_question_entry = command_entry.get()
##            ai_question_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
##            ai_input_button = tk.Button(ssh_session_tab, text="Ask Chief", command=lambda: send_command(output_text, command_entry=command_entry, ai_question_entry="Chief " + command_entry.get()))
##            ai_input_button.pack()
##            command_entry.focus_set()

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
        """
        Creates and packs a button for configuring a custom connection.
        
        Args:
            """Configures a custom connection by creating a dialog window for user input.
            
            Args:
                self: The instance of the class containing this method.
            
            Returns:
                None: This method doesn't return anything, but it creates a new window for custom connection configuration,
                adds the entered device information to the devices list, creates a new device button,
                appends the device information to a CSV file, and closes the custom window upon saving.
            """
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, it creates and packs a button in the GUI.
        """
        configure_button = ttk.Button(self.tab, text="Configure Custom Connection", command=self.configure_custom_connection)
        configure_button.pack()

    def configure_custom_connection(self):
        custom_window = tk.Toplevel(self.parent)
        custom_window.title("Custom Connection")
    
        # Create and pack the labels and entry fields
        ttk.Label(custom_window, text="Device Label:").pack()
        device_label_entry = ttk.Entry(custom_window)
        device_label_entry.pack()
    
        ttk.Label(custom_window, text="Connection Type:").pack()
        connection_type_var = tk.StringVar(value="SSH")
        """Saves a new device with the provided information.
        
        Args:
            None
        
        Returns:
            None: This function doesn't return anything, but it performs the following actions:
                - Appends the device information to the devices list
                - Creates a button for the device in the UI
                - Appends the device information to the 'devices.csv' file
                - Closes the custom window used for input
        """
        connection_type_dropdown = ttk.Combobox(custom_window, textvariable=connection_type_var, values=["SSH", "Serial"])
        connection_type_dropdown.pack()
    
        ttk.Label(custom_window, text="Host:").pack()
        host_entry = ttk.Entry(custom_window)
        host_entry.pack()
    
        # Function to save the device information
        def save_device():
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
            with open('devices.csv', 'a', newline='') as csvfile:
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

    def set_username_placeholder(self, event):
        """
        Sets a placeholder text for the username entry field.
        
        Args:
            self: The instance of the class containing this method.
            event: tkinter.Event: The event object triggered by the focus out event.
        
        Returns:
            None: This method doesn't return anything.
        """
        if not self.username_entry.get():
            self.username_entry.insert(0, "Username")

    def set_password_placeholder(self, event):
        """
        Sets a placeholder text in the password entry field if it's empty.
        
        Args:
            self: The instance of the class containing this method.
            event: The event object triggered by the user action (not used in the method body).
        
        Returns:
            None: This method doesn't return anything.
        """
        if not self.password_entry.get():
            self.password_entry.insert(0, "Password")

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    
    # Set the window title
    root.title("Eagle Terminal_v0.1")
    
    # Set the icon
    # root.iconbitmap("path_to_icon_file.ico")
    
    # Set the window size
    root.geometry("800x600")

    # Create a notebook widget to hold the tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Create the tabs
    connection_tab = ConnectionTab(root, notebook)


    # Add the tabs to the notebook
    notebook.add(connection_tab.tab, text="Connections")


    root.mainloop()