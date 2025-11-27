import os
import json
from datetime import datetime
from flask import Flask, request
from flask_socketio import SocketIO, emit

# Configuration
ORDERS_FILE = os.path.join(os.path.dirname(__file__), 'orders.json')
HOST = '0.0.0.0'
PORT = 5000

app = Flask(__name__)
# Allow all origins for local development
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

def load_orders():
    """Loads orders from orders.json."""
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'w') as f:
            json.dump([], f)
    with open(ORDERS_FILE, 'r') as f:
        return json.load(f)

def save_orders(orders):
    """Saves orders to orders.json."""
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)

@socketio.on("new_order")
def handle_new_order(data):
    """Handles new order events from customer clients."""
    print(f"Received new order: {data}")
    order = data
    order["timestamp"] = datetime.now().isoformat()

    orders = load_orders()
    orders.append(order)
    save_orders(orders)

    # Log to console
    table_num = order.get("table", "N/A")
    items = ", ".join(order.get("items", []))
    print(f"New order from Table {table_num}: {items}")

    # Broadcast to waiter clients
    emit("order_update", order, broadcast=True)

@app.route('/')
def index():
    return "Restaurant Order Dispatch Backend"

if __name__ == '__main__':
    print(f"Starting Flask-SocketIO server on {HOST}:{PORT}")
    socketio.run(app, host=HOST, port=PORT)
