import tkinter as tk
from tkinter import ttk

class Custom_Connection:
           
    def configure_custom_connection(self, parent):
        """
        Configures a custom connection by creating a new window for user input.
        
        Args:
            parent (tk.Tk): The parent window for the custom connection dialog.
        
        Returns:
            None: This method doesn't return anything, it creates a new window and handles the connection configuration.
        """
        custom_window = tk.Toplevel(self.parent)
        custom_window.title("Custom Connection")
        
        # Create and pack the labels and entry fields
        ttk.Label(custom_window, text="Device Label:").pack()
        device_label_entry = ttk.Entry(custom_window)
        device_label_entry.pack()
        
        ttk.Label(custom_window, text="Connection Type:").pack()
        connection_type_var = tk.StringVar(value="SSH")
        """
        Saves a new device's information and creates a corresponding button.
        
        Args:
            None
        
        Returns:
            None: This function doesn't return a value, but it performs the following actions:
                - Appends the device information to the devices list
                - Creates a button for the device in the UI
                - Appends the device information to the 'devices.csv' file
                - Closes the custom window used for input
        
        """        connection_type_dropdown = ttk.Combobox(custom_window, textvariable=connection_type_var, values=["SSH", "Serial"])
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