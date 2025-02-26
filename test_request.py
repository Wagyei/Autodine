
import requests
import random

# Define the URLs to which the POST requests will be sent
feasibility_url = 'http://127.0.0.1:8000/check_feasible_items/'  # URL to check feasibility
order_url = 'http://127.0.0.1:8000/order_items/'  # URL to place the order

# Define multiple payloads for different test cases
payloads = [
    {
        # Test case 1: Valid items with no modifications
        "Burger": {},    # Standard Burger
        "Fries": {}      # Standard Fries
    },
    {
        # Test case 2: Valid items with extra ingredients
        "Burger": {"Cheese": 2, "Tomato": "-7-"},     # Extra cheese on the burger
        "Fries": {}                  # Standard Fries
    },
    {
        # Test case 3: Valid items with missing ingredients
        "BLT Sandwich": {"Lettuce": 0, "Tomato": 1},  # No lettuce
        "Bacon Cheeseburger": {"Bacon": 0}            # No bacon
    },
    {
        # Test case 4: Non-existent items
        "Pizza": {},    # Item not on the menu
        "Vegan Burger": {}  # Non-existent item
    },
    {
        # Test case 5: Mixed valid and invalid items
        "Burger": {"Cheese": 1},      # Valid item with extra cheese
        "Pizza": {},                  # Non-existent item
        "Fries": {},                  # Valid item
        "Vegan Burger": {}            # Non-existent item
    },
    {
        # Test case 6: Valid item with an unusually large quantity of ingredients
        "Burger": {"Cheese": 10, "Lettuce": 5},  # Extra cheese and lettuce
        "Hot Dog": {"Ketchup": 3}                # Extra ketchup
    },
    {
        # Test case 7: Valid item with less than usual ingredients
        "Bacon Cheeseburger": {"Cheese": 0, "Bacon": 1},  # No cheese, single bacon
        "Fries": {}                                      # Standard Fries
    },
    {
        # Test case 8: Completely invalid items
        "Tacos": {},   # Non-existent item
        "Pasta": {}    # Non-existent item
    }
]

# Function to send POST requests with different payloads and handle responses
def test_payloads(payloads):
    for i, payload in enumerate(payloads, 1):
        print(f"Testing payload {i}...")

        try:
            # Step 1: Check if the items are feasible
            feasibility_response = requests.post(feasibility_url, json={'items': payload})

            # Check if the feasibility request was successful
            if feasibility_response.status_code == 200:
                feasibility_data = feasibility_response.json()

                # Check if all items are feasible
                all_feasible = all(item['feasible'] for item in feasibility_data.values())

                if all_feasible:
                    print(f"All items in payload {i} are feasible. Proceeding with the order...")

                    # Step 2: If feasible, place the actual order
                    order_response = requests.post(order_url, json={'items': payload, 'tip':round(random.uniform(0, 10), 2)})

                    if order_response.status_code == 201:  # Order successfully created and processed
                        print(f"Order placed successfully for payload {i}:")
                        data = eval(str(order_response.json()))
                        print(data["pretty_print"])
                    else:
                        print(f"Failed to place order for payload {i}: {order_response.status_code} {order_response.text}")

                else:
                    print(f"Some items in payload {i} are not feasible:", feasibility_data)

            else:
                # Print the error message if the feasibility check failed
                print(f"Error checking feasibility for payload {i}: {feasibility_response.status_code}, {feasibility_response.text}")

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that may occur during the request
            print(f"An error occurred with payload {i}: {e}")

# Run the tests
test_payloads(payloads)
