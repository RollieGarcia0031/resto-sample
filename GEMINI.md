= Restaurant Order Dispatch System
:author: Auto-Generated Specification
:version: 1.0
:doctype: book
:toc: left
:toclevels: 4

== Project Title
*Local Restaurant Order Dispatch System*  
Real-time offline communication between Customer UI and Waiter UI using Python.

== Project Summary
Generate a fully working Python project that implements a local-network restaurant ordering system featuring:

* Customer Tkinter UI
* Waiter Tkinter UI
* Local backend using Flask + Flask-SocketIO
* Real-time WebSocket communication
* Order storage in a JSON file
* Customer choice logging in a JSON file
* No external APIs or internet connectivity required
* Fully portable and runnable on any device using Python `venv` + `pip`

The system must allow:
* Customer sends order (table number + items)
* Backend stores and broadcasts updates
* Waiter sees real-time incoming orders
* All orders stored locally

== Project Structure

The following directory structure must be generated exactly:

----
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
----

== Requirements

=== Python
Use **Python 3.10+**.

=== Package Management

The system must use:

* `venv` for virtual environment
* `pip` for dependency installation
* `requirements.txt` for dependency tracking

=== Dependencies
The project must include the following packages:

----
flask
flask-socketio
python-socketio
eventlet
tk
----

These should be listed in the root-level `requirements.txt`.

== Backend Specification (`server.py`)

The backend must:

. Use *Flask* and *Flask-SocketIO* with `eventlet`.
. Run on:
+
----
host: 0.0.0.0
port: 5000
----
. Listen for a WebSocket event: `"new_order"`.
. When an order is received:
.. Add a timestamp field in ISO format.
.. Save the order in `orders.json` (append).
.. Broadcast the order to all waiter clients using `"order_update"`.
. Automatically create `orders.json` with an empty list `[]` if not present.
. Log each received order in the console in the format:
+
----
New order from Table X: item1, item2
----

=== Order JSON Format
----
{
  "table": 4,
  "items": ["Burger"],
  "timestamp": "<ISO datetime>"
}
----

== Customer UI Specification (`customer.py`)

The Customer App must:

* Use Tkinter for UI.
* Connect to backend WebSocket at:
+
----
ws://localhost:5000
----
* Provide UI components:
** Entry for table number
** Radio button or dropdown menu for item selection
** “Send Order” button
* On sending an order:
** Validate table number (must not be empty)
** Create an order object
** Save to `customer_choices.json` in append mode (one JSON object per line)
** Emit `"new_order"` event
** Display a confirmation popup

Additionally:

* Auto-create `customer_choices.json` if missing.
* Show an error popup for invalid input (e.g., missing or non-numeric table number).

== Waiter UI Specification (`waiter.py`)

The Waiter App must:

* Use Tkinter for UI.
* Connect to backend WebSocket on startup.
* Listen for `"order_update"` events.
* For each incoming order, append a line to a Tkinter Listbox in the format:
+
----
Table X: item1, item2
----
* Display a title label:
+
**Incoming Orders**

Updates must appear in real-time with no user action.

== System Behavior Summary

=== Customer Flow
. Customer selects menu item.
. Customer enters table number.
. Customer clicks “Send Order”.
. Order saved locally to `customer_choices.json`.
. Order sent to backend.

=== Backend Flow
. Receives `"new_order"` event.
. Adds timestamp.
. Saves order to `orders.json`.
. Broadcasts `"order_update"` to all connected waiter apps.

=== Waiter Flow
. Receives `"order_update"`.
. Displays formatted order text in Listbox.
. Waiter sees table + items instantly.

== Example Interaction

=== Customer Sends
----
{
   "table": 3,
   "items": ["Pasta"]
}
----

=== Backend Logs
----
New order from Table 3: Pasta
----

=== Waiter Sees
----
Table 3: Pasta
----

== Additional Implementation Details

* Logging should be present in backend + frontends.
* JSON files must be auto-created if missing.
* UI padding and readable fonts must be used.
* All code must be clearly commented.

== Running the Project

=== Create Environment
----
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
----

=== Run Backend
----
python backend/server.py
----

=== Run Customer UI
----
python customer_app/customer.py
----

=== Run Waiter UI
----
python waiter_app/waiter.py
----

== Constraints

* Local network only (no external APIs).
* Tkinter must be the only UI framework.
* JSON must be used for storage (no SQL).
* Flask-SocketIO must be used for real-time communication.
* Codebase must be clean, modular, and readable.

== End of Specification
*This completes the automated project generation instructions.*
