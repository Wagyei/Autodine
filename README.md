## Autodine Backend

This is the backend of **Autodine**, a chatbot-based food ordering system that processes customer orders by checking item feasibility and placing orders. The backend is built using **Django** and provides endpoints for checking inventory, placing orders, and retrieving order history.

### Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
  - [Check Feasibility](#check-feasibility)
  - [Place Order](#place-order)
  - [Retrieve Menu](#retrieve-menu)
  - [Order History](#order-history)
- [Testing](#testing)

---

### Features

- **Check Feasibility**: Verifies if the requested items are available in the inventory.
- **Place Order**: Processes the order, deducts inventory, and stores the order in history.
- **Order History**: Keeps track of all completed orders.
- **Menu Retrieval**: Provides the list of available menu items.

---

### Tech Stack

- **Backend Framework**: Django (Python)
- **Language**: Python 3.8+
- **Dependencies**: Flask, requests

---

### Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/autodine-backend.git
   cd autodine-backend
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**:

   ```bash
   python app.py
   ```

   The server should be running on `http://127.0.0.1:5000`.

---

### API Endpoints

#### Check Feasibility

- **Endpoint**: `/check_feasible_items/`
- **Method**: `POST`
- **Description**: Checks whether the requested items are available in inventory.
- **Request Body**:

  ```json
  {
    "items": {
      "Burger": {},
      "Fries": {}
    }
  }
  ```

- **Response**:

  ```json
  {
    "feasible": true,
    "unavailable_items": []
  }
  ```

#### Place Order

- **Endpoint**: `/order_items/`
- **Method**: `POST`
- **Description**: Places an order, deducts from inventory, and stores the order in history.
- **Request Body**:

  ```json
  {
    "items": {
      "Burger": {},
      "Fries": {}
    },
    "tip": 3.50
  }
  ```

- **Response**:

  ```json
  {
    "status": "success",
    "order_id": 1
  }
  ```

#### Retrieve Menu

- **Endpoint**: `/menu`
- **Method**: `GET`
- **Description**: Retrieves the available menu and item quantities.
- **Response**:

  ```json
  {
    "Burger": 9,
    "Fries": 19,
    "Chicken Sandwich": 10,
    "Bacon Cheeseburger": 8,
    ...
  }
  ```

#### Order History

- **Endpoint**: `/order_history`
- **Method**: `GET`
- **Description**: Retrieves the history of all placed orders.
- **Response**:

  ```json
  [
    {
      "items": {
        "Burger": {},
        "Fries": {}
      },
      "tip": 3.50,
      "status": "completed"
    }
  ]
  ```

---

### Testing

To test the API using `requests`, follow these steps:

1. **Test Feasibility**:

   ```python
   import requests

   feasibility_url = 'http://127.0.0.1:5000/check_feasible_items/'

   payload = {
       "items": {
           "Burger": {},
           "Fries": {}
       }
   }

   response = requests.post(feasibility_url, json=payload)
   print("Feasibility Response:", response.json())
   ```

2. **Test Place Order**:

   ```python
   order_url = 'http://127.0.0.1:5000/order_items/'

   order_payload = {
       "items": {
           "Burger": {},
           "Fries": {}
       },
       "tip": 3.50
   }

   response = requests.post(order_url, json=order_payload)
   print("Order Response:", response.json())
   ```

3. **Test Menu Retrieval**:

   ```python
   menu_url = 'http://127.0.0.1:5000/menu'

   response = requests.get(menu_url)
   print("Menu:", response.json())
   ```

---

### Future Enhancements

- Add user authentication for order management.
- Implement real-time inventory updates using websockets.
- Create a dashboard for admins to view orders and inventory in real-time.
