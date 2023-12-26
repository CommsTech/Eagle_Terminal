import tkinter as tk
from tkinter import ttk

class Custom_Connection:
           
    def configure_custom_connection(self, parent):
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