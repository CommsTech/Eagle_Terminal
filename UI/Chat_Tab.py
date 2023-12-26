import tkinter as tk
from tkinter import ttk

class Chat_Tab(ttk.Frame):
  
    self.output_text_box = tk.Text(self, height=20, width=50)
    self.output_text_box.pack()
        
    self.input_text_box = tk.Text(self, height=5, width=50)
    self.input_text_box.pack()
        
    self.send_button = tk.Button(self, text="Send", command=self.send_message)
    self.send_button.pack()
        
    self.pack(fill=tk.BOTH, expand=True)  # Pack the frame to fill the parent space

    def send_message(self):
        message = self.input_text_box.get("1.0", tk.END).strip()
        
        if message:
            # Send message to GPT-4 and get response
            response = self.get_gpt4_response(message)
            
            # Display response in output text box
            self.output_text_box.insert(tk.END, f"User: {message}\n")
            self.output_text_box.insert(tk.END, f"GPT-4: {response}\n")
            
            # Clear input text box
            self.input_text_box.delete("1.0", tk.END)
    
    def get_gpt4_response(self, message):
        # Call GPT-4 API or model to get response
        # Replace this with your actual implementation
        
        # For demonstration purposes, simply return the reversed message
        return message[::-1]


    def create_ai_button(self):
        ai_question_entry = tk.Entry(self.tab)
        ai_question_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ai_input_button = tk.Button(text="Ask Chief", command=lambda: Chief.quick_prompt(ai_question_entry))
        ai_input_button.pack()
        output_text_box = tk.Text(self.tab)
        output_text_box.pack(fill=tk.BOTH, expand=True)
        ai_response = "Hello"
        output_text_box.insert(tk.END, "AI: " + ai_response + "\n")
        output_text_box.see(tk.END)