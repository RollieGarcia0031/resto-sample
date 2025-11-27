import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import socketio
import json
import os
import threading

# Configuration
BACKEND_URL = 'http://localhost:5000'
CUSTOMER_CHOICES_FILE = os.path.join(os.path.dirname(__file__), 'customer_choices.json')

# Initialize Socket.IO client
sio = socketio.Client()

def load_customer_choices():
    """Loads customer choices from customer_choices.json."""
    if not os.path.exists(CUSTOMER_CHOICES_FILE):
        with open(CUSTOMER_CHOICES_FILE, 'w') as f:
            json.dump([], f) # Initialize as empty list
    with open(CUSTOMER_CHOICES_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return [] # Return empty list if file is empty or invalid JSON

def save_customer_choice(choice):
    """Appends a customer choice to customer_choices.json."""
    choices = load_customer_choices()
    choices.append(choice)
    with open(CUSTOMER_CHOICES_FILE, 'w') as f:
        json.dump(choices, f, indent=2)


class CustomerApp:
    def __init__(self, master):
        self.master = master
        master.title("Customer Order App")
        master.geometry("400x300")
        master.resizable(False, False)

        # Styling
        master.option_add('*Font', 'Arial 12')
        master.option_add('*Background', '#f0f0f0')

        self.sio_connected = False
        self.connect_sio()

        self.create_widgets()

    def connect_sio(self):
        try:
            sio.connect(BACKEND_URL)
            self.sio_connected = True
            print("Socket.IO connected for customer.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to backend: {e}")
            self.sio_connected = False
            print(f"Socket.IO connection failed: {e}")

    def create_widgets(self):
        # Table Number
        self.table_label = tk.Label(self.master, text="Table Number:")
        self.table_label.pack(pady=(20, 5))
        self.table_entry = tk.Entry(self.master, width=20)
        self.table_entry.pack(pady=5)

        # Item Selection
        self.item_label = tk.Label(self.master, text="Select Item:")
        self.item_label.pack(pady=5)
        
        self.menu_items = ["Burger", "Pizza", "Pasta", "Salad", "Drink"]
        self.selected_item = tk.StringVar(self.master)
        self.selected_item.set(self.menu_items[0]) # default value

        self.item_dropdown = ttk.OptionMenu(self.master, self.selected_item, self.menu_items[0], *self.menu_items)
        self.item_dropdown.pack(pady=5)

        # Send Order Button
        self.send_button = tk.Button(self.master, text="Send Order", command=self.send_order, bg='#4CAF50', fg='white', relief='raised')
        self.send_button.pack(pady=20)

    def send_order(self):
        table_num_str = self.table_entry.get()
        selected_item = self.selected_item.get()

        if not table_num_str:
            messagebox.showwarning("Input Error", "Table Number cannot be empty.")
            return
        
        try:
            table_num = int(table_num_str)
            if table_num <= 0:
                messagebox.showwarning("Input Error", "Table Number must be a positive integer.")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Table Number must be a valid integer.")
            return

        order_data = {
            "table": table_num,
            "items": [selected_item]
        }

        if self.sio_connected:
            sio.emit("new_order", order_data)
            save_customer_choice(order_data) # Save to local customer choices
            messagebox.showinfo("Order Sent", f"Order for Table {table_num} ({selected_item}) sent successfully!")
            self.table_entry.delete(0, tk.END) # Clear table number
            self.selected_item.set(self.menu_items[0]) # Reset item selection
        else:
            messagebox.showerror("Connection Error", "Not connected to the backend. Please restart the app.")

@sio.event
def connect():
    print("Customer: Connected to server!")

@sio.event
def disconnect():
    print("Customer: Disconnected from server!")

def run_customer_app():
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()
    sio.disconnect() # Disconnect SocketIO when Tkinter window is closed

if __name__ == '__main__':
    # Run the SocketIO client in a separate thread to not block Tkinter's mainloop
    # Although for simple emit, it usually doesn't block.
    # We still need to ensure disconnection on app close.
    
    # Ensure customer_choices.json exists and is valid
    load_customer_choices()
    
    run_customer_app()
