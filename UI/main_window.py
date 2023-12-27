import tkinter as tk
from tkinter import ttk
from UI.Connection_Tab import ConnectionTab
from UI.ssh_tab import SSHTab

class MainWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.title('EagleTerm_v0.2')

        self.tab_control = ttk.Notebook(self)

        connection_tab = ConnectionTab(parent=self.tab_control, notebook=self.tab_control)
        connection_tab_path = connection_tab.winfo_pathname(connection_tab.winfo_id())
        self.tab_control.add(connection_tab_path, text='Connections')

        self.create_new_tab_button = tk.Button(self, text='+', command=self.add_new_tab)
        self.create_new_tab_button.pack(side='left')

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
