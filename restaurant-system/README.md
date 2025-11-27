# Local Restaurant Order Dispatch System

This project implements a local-network restaurant ordering system with a Customer UI, Waiter UI, and a Flask-SocketIO backend. It uses real-time WebSocket communication and stores data in local JSON files.

## Project Structure

```
restaurant-system/
│
├── backend/
│   ├── server.py
│   └── orders.json            # auto-created if not present
│
├── customer_app/
│   ├── customer.py
│   └── customer_choices.json  # auto-created if not present
│
├── waiter_app/
│   └── waiter.py
│
├── requirements.txt
└── README.md
```

## Setup and Running

### Create Environment
```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Backend
```bash
python backend/server.py
```

### Run Customer UI
```bash
python customer_app/customer.py
```

### Run Waiter UI
```bash
python waiter_app/waiter.py
```
