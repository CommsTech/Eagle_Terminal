import tkinter as tk
from tkinter import ttk
from UI.Connection_Tab import ConnectionTab
from UI.ssh_tab import SSHTab

class MainWindow(ttk.Frame):
    def __init__(self, parent):
        """Initializes the main application window and sets up the tab control.
        
        Args:
            parent (tk.Tk): The parent window for this application.
        
        Returns:
            None: This method doesn't return anything.
        """
        super().__init__(parent)
        parent.title('EagleTerm_v0.2')

        self.tab_control = ttk.Notebook(self)

        connection_tab = ConnectionTab(parent=self.tab_control, notebook=self.tab_control)
        connection_tab_path = connection_tab.winfo_pathname(connection_tab.winfo_id())
        self.tab_control.add(connection_tab_path, text='Connections')

        self.create_new_tab_button = tk.Button(self, text='+', command=self.add_new_tab)
        self.create_new_tab_button.pack(side='left')
"""Adds a new SSH tab to the application interface.

Args:
    None

"""
Adds a new tab to the interface by creating a new SSH tab.

This method is a wrapper around the add_new_ssh_tab method, simplifying the process of adding a new tab with SSH functionality.

Args:
    self: The instance of the class containing this method.

Returns:
    None: This method doesn't return anything, it modifies the interface by adding a new tab.
"""
Returns:
    None: This method doesn't return anything, but it creates and displays a new SSH tab in the interface.
"""
"""Removes a tab from the tab control.

Args:
    index (int, optional): The index of the tab to be removed. If not provided, the currently selected tab will be removed.

Returns:
    None: This method doesn't return anything.
"""

        self.tab_control.pack(expand=True, fill='both')
        self.add_new_ssh_tab()
        self.tab_control.forget(1)
        self.tab_control.select(connection_tab)
        

    def add_new_ssh_tab(self):
        tab = SSHTab(self.tab_control)
        self.tab_control.add(tab, text='SSH Tab')
        self.tab_control.select(tab)

    def add_new_tab(self):
        self.add_new_ssh_tab()

    def remove_tab(self, index=None):
        if index is None:
            index = self.tab_control.index(self.tab_control.select())
        if len(self.tab_control.tabs()) > 1:
            self.tab_control.forget(index)
