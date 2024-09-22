import tkinter as tk
from tkinter import ttk
from ssh.ssh_manager import SSHManager

class SSHTab(ttk.Frame):
    def __init__(self, parent):
        """Initialize a new instance of the class.
        
        Args:
            parent: The parent object or widget to which this instance is attached.
        
        """
        Creates a graphical user interface for SSH connection input.
        
        This method sets up labels and entry fields for hostname, port, username, and password,
        as well as a connect button. It uses the tkinter grid layout manager to organize the elements.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, it modifies the instance's attributes.
        """
        Returns:
            None: This method doesn't return anything.
        """
        super().__init__(parent)
        self.ssh_manager = SSHManager()
        self.create_connection_interface()

    def create_connection_interface(self):
        self.hostname_label = tk.Label(self, text="Hostname:")
        self.hostname_label.grid(column=0, row=0, sticky=tk.W)
        self.hostname_entry = tk.Entry(self)
        self.hostname_entry.grid(column=1, row=0)

        self.port_label = tk.Label(self, text="Port:")
        self.port_label.grid(column=0, row=1, sticky=tk.W)
        self.port_entry = tk.Entry(self)
        self.port_entry.grid(column=1, row=1)
        self.port_entry.insert(0, "22")

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(column=0, row=2, sticky=tk.W)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(column=1, row=2)

        self.password_label = tk.Label(self, text="Password:")
        """Establishes an SSH connection using provided credentials.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, but prints a status message.
        """        self.password_label.grid(column=0, row=3, sticky=tk.W)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(column=1, row=3)

        self.connect_button = tk.Button(self, text="Connect", command=self.connect_ssh)
        self.connect_button.grid(column=1, row=4)

    def connect_ssh(self):
        hostname = self.hostname_entry.get()
        port = int(self.port_entry.get())
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.ssh_manager.connect(hostname, port, username, password):
            print("Connected successfully.")
        else:
            print("Could not establish connection.")
