import tkinter as tk
from tkinter import messagebox
import socketio
import threading

# Configuration
BACKEND_URL = 'http://localhost:5000'

# Initialize Socket.IO client
sio = socketio.Client()

class WaiterApp:
    def __init__(self, master):
        self.master = master
        master.title("Waiter Order Display")
        master.geometry("500x600")
        master.resizable(False, False)

        # Styling
        master.option_add('*Font', 'Arial 12')
        master.option_add('*Background', '#f0f0f0')

        self.create_widgets()
        self.connect_sio()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.master, text="Incoming Orders", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        self.title_label.pack(pady=10)

        # Frame for Listbox and Scrollbar
        list_frame = tk.Frame(self.master)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Listbox for orders
        self.order_listbox = tk.Listbox(list_frame, height=20, width=60, font=('Arial', 10), bd=2, relief='groove')
        self.order_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.order_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.order_listbox.config(yscrollcommand=scrollbar.set)

    def connect_sio(self):
        try:
            sio.connect(BACKEND_URL)
            print("Socket.IO connected for waiter.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to backend: {e}")
            print(f"Socket.IO connection failed: {e}")

    def add_order_to_listbox(self, order_data):
        table_num = order_data.get("table", "N/A")
        items = ", ".join(order_data.get("items", []))
        formatted_order = f"Table {table_num}: {items}"
        self.order_listbox.insert(tk.END, formatted_order)
        self.order_listbox.yview(tk.END) # Scroll to the bottom

@sio.event
def connect():
    print("Waiter: Connected to server!")

@sio.event
def disconnect():
    print("Waiter: Disconnected from server!")

@sio.on("order_update")
def handle_order_update(data):
    print(f"Waiter: Received order update: {data}")
    # Run this in the Tkinter main thread
    app.master.after(0, app.add_order_to_listbox, data)

def run_waiter_app():
    global app # Make app accessible to the sio.on decorator
    root = tk.Tk()
    app = WaiterApp(root)
    root.mainloop()
    sio.disconnect() # Disconnect SocketIO when Tkinter window is closed

if __name__ == '__main__':
    run_waiter_app()
