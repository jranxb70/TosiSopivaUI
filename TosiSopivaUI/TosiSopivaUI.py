import flet as ft
import json
from DBEngineWrapper import DBEngineWrapper

def main(page: ft.Page):
    page.title = "Customer Information"
    page.vertical_alignment = ft.MainAxisAlignment.START

    engine = DBEngineWrapper()

    # UI Elements
    customer_id_input = ft.TextField(label="Enter Customer ID", width=300)
    fetch_button = ft.ElevatedButton(text="Fetch Customer Info", on_click=lambda e: fetch_customer_info(page, engine, customer_id_input.value))
    customer_info_text = ft.Text("", size=20)

    page.add(customer_id_input, fetch_button, customer_info_text)
    fetch_all_button = ft.ElevatedButton(text="Fetch All Customers", on_click=lambda e: fetch_all_customers(page, engine))
    all_customers_text = ft.Text("", size=20)

    page.add(fetch_all_button, all_customers_text)

def fetch_all_customers(page: ft.Page, engine: DBEngineWrapper):
    customer_data = engine.queryCustomers()
    if "error" in customer_data:
        all_customers_info = customer_data["error"]
    else:
        all_customers_info = json.dumps(customer_data, indent=2)
    
    # Find and update the Text control for displaying all customers. This assumes it's the last control.
    page.controls[-1].value = all_customers_info
    page.update()

def fetch_customer_info(page: ft.Page, engine: DBEngineWrapper, customer_id: str):
    try:
        customer_id_int = int(customer_id)
        customer_data = engine.getCustomer(customer_id_int)
        customer_info = json.dumps(customer_data, indent=2)
    except ValueError:
        customer_info = "Invalid Customer ID. Please enter a valid number."
    except Exception as e:
        customer_info = f"Error fetching customer info: {str(e)}"
    
    page.controls[-1].value = customer_info  # Assumes the last control is the Text widget for displaying customer info
    page.update()

# Replace 'if __name__ == "__main__":' block with this call to start the Flet app
ft.app(target=main)