import csv
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, Scrollbar, Text, Entry
try:
    import paramiko
    import serial
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'paramiko', 'pyserial'])
    import paramiko
    import serial
from serial.tools.list_ports import comports
from functools import partial

class ConnectionTab:
    def __init__(self, parent, notebook):
        self.parent = notebook
        self.notebook = notebook
        self.tab = ttk.Frame(self.parent)
        self.notebook.add(self.tab, text="Connections")
        self.devices = self.read_devices_file('devices.csv')
        self.create_userpass_widgets()
        self.create_ssh_widgets()
        self.create_serial_widgets()

    def create_userpass_widgets(self):
        self.username_label = ttk.Label(self.tab, text="Username:")
        self.username_label.pack()

        self.username_entry = ttk.Entry(self.tab)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(self.tab, text="Password:")
        self.password_label.pack()

        self.password_entry = ttk.Entry(self.tab, show="*")
        self.password_entry.pack(pady=5)

    def read_devices_file(self, filename):
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
        for device in self.devices:
            # Create the device widget
            device_widget = ttk.Frame(self.tab)
            device_widget.pack()

            device_label = device['device_label']
            connection_type = device['connection_type']
            host = device['host']

            if connection_type == 'SSH':
                button_text = f"{device_label} - {connection_type} {host}"
                self.create_button(self.tab, button_text, self.select_connection, connection_type=connection_type, host=host)

    def create_serial_widgets(self):
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
        
            def send_command(output_text, command_entry, ssh_client):
                command = command_entry.get()
                while command:
                    stdin, stdout, stderr = ssh_client.exec_command(command)
                    output = stdout.read().decode("utf-8")
                    output_text.insert(tk.END, output)
                    command_entry.delete(0, tk.END)
                    command = command_entry.get()
        
            command_entry.bind("<Return>", lambda event: send_command(output_text, command_entry, ssh_client))
            self.parent.mainloop()
            ssh_client.close()
        else:
            print("Invalid connection type")

    def configure_custom_connection(self):
        custom_window = tk.Toplevel(self.parent)
        custom_window.title("Custom Connection")
        custom_window.mainloop()

    def set_username_placeholder(self, event):
        if not self.username_entry.get():
            self.username_entry.insert(0, "Username")

    def set_password_placeholder(self, event):
        if not self.password_entry.get():
            self.password_entry.insert(0, "Password")


class SSHTab:  
    def __init__(self, parent):
        self.parent = parent
        self.tab = ttk.Frame(self.parent)
        self.parent.add(self.tab, text="SSH")
        entries = [
            ("Host:", ttk.Entry),
            ("Username:", ttk.Entry),
            ("Password:", partial(ttk.Entry, show="*"))
        ]
        for label, entry_constructor in entries:
            ttk.Label(self.tab, text=label).pack()
            entry_constructor(self.tab).pack()
    
        self.connect_button = ttk.Button(self.tab, text="Connect", command=self.connect_ssh)
        self.connect_button.pack()
        self.close_button = ttk.Button(self.tab, text="X", command=self.close_tab)
        self.close_button.pack(side="right")
        
    def connect_ssh(self):
        host = self.host_entry.get()
        username = self.user_entry.get()
        password = self.password_entry.get()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, username=username, password=password)
        ssh_session_tab = ttk.Frame(self.parent)
        self.parent.add(ssh_session_tab, text=f"SSH - {host}")
        ssh_output = Text(ssh_session_tab)
        ssh_output.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(ssh_session_tab, command=ssh_output.yview)
        scrollbar.pack(side="right", fill="y")
        ssh_output.configure(yscrollcommand=scrollbar.set)
        channel = ssh_client.invoke_shell()
    
        def send_input(event):
            input_text = input_entry.get()
            ssh_channel.send(input_text + "\n")
            input_entry.delete(0, tk.END)
    
        ssh_input = Entry(ssh_session_tab)
        ssh_input.pack(fill="x")
        ssh_input.bind("<Return>", send_input)
    
        def receive_output():
            if channel.recv_ready():
                output = channel.recv(1024).decode()
                ssh_output.insert("end", output)
                ssh_output.see("end")
            ssh_output.after(100, receive_output)
        receive_output()
    
        def close_ssh_tab():
            ssh_client.close()
    
        close_button = ttk.Button(ssh_session_tab, text="Close", command=close_ssh_tab)
        close_button.pack()
    def close_tab(self):
        pass

class SerialTab:
    
    def __init__(self, parent):
        self.parent = parent
        self.tab = ttk.Frame(self.parent)
        self.parent.add(self.tab, text="Serial")
        self.create_port_widgets()
        self.create_baud_widgets()
        self.create_connect_button()
        
    def create_port_widgets(self):
        self.port_label = ttk.Label(self.tab, text="Port:")
        self.port_label.grid(row=0, column=0, sticky="w")
        self.port_combobox = ttk.Combobox(self.tab, values=[port.device for port in comports()])
        self.port_combobox.grid(row=0, column=1, sticky="w")
    
    def create_baud_widgets(self):
        self.baud_label = ttk.Label(self.tab, text="Baud Rate:")
        self.baud_label.grid(row=1, column=0, sticky="w")
        self.baud_entry = ttk.Entry(self.tab)
        self.baud_entry.grid(row=1, column=1, sticky="w")
    
    def create_connect_button(self):
        self.connect_button = ttk.Button(self.tab, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=2, column=0, columnspan=2, sticky="w")
        
    def connect_serial(self):
        port = self.port_combobox.get()
        baud_rate = int(self.baud_entry.get())
        
        try:
            ser = serial.Serial(port, baud_rate)
            # Code to handle the established serial connection
            print("Serial connection established successfully.")
            
            # Create a new tab for the Serial session
            serial_session_tab = ttk.Frame(self.parent)
            self.parent.add(serial_session_tab, text=f"Serial - {port}")
            
            # Create a Text widget to display terminal-like output
            serial_output = Text(serial_session_tab)
            serial_output.pack(fill="both", expand=True)
            
            # Create a Scrollbar for the Text widget
            scrollbar = ttk.Scrollbar(serial_session_tab, command=serial_output.yview)
            scrollbar.pack(side="right", fill="y")
            
            # Configure the Text widget to use the Scrollbar
            serial_output.configure(yscrollcommand=scrollbar.set)
            
            # Function to send command
            def send_command(event):
                command = serial_input.get()
                ser.write(command.encode() + b'\n')
                serial_input.delete("1.0", "end")
            
            # Create an Entry widget to input commands
            serial_input = Entry(serial_session_tab)
            serial_input.pack(fill="x")
            serial_input.bind("<Return>", send_command)
            
            # Function to receive output
            def receive_output():
                output = ser.readline().decode()
                serial_output.insert("end", output)
                serial_output.see("end")
                serial_output.after(100, receive_output)
            
            # Start receiving output
            receive_output()
            
            # Perform serial communication...
            # e.g. read/write data to the device
            
            # Close the Serial connection when the tab is closed
            def close_serial_tab():
                ser.close()
            
            # Add a close button to the tab
            close_button = ttk.Button(serial_session_tab, text="Close", command=close_serial_tab)
            close_button.pack()
            
        except serial.SerialException as e:
            print("Error: Failed to establish serial connection:", str(e))
    
    def close_tab(self):
        pass

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
    ssh_tab = SSHTab(notebook)
    serial_tab = SerialTab(notebook)
    

    # Add the tabs to the notebook
    notebook.add(connection_tab.tab, text="Connections")
    notebook.add(ssh_tab.tab, text="SSH")
    notebook.add(serial_tab.tab, text="Serial")
    

    root.mainloop()
