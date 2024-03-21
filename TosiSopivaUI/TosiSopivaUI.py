# import flet as ft
# import json
# from DBEngineWrapper import DBEngineWrapper

# def create_customer_ui(customer_data):
#     # Main container for all customers
#     customers_container = ft.Column(spacing=10)

#     for customer in customer_data["customers"]:
#         # Individual container for each customer's information
#         customer_info = ft.Column(spacing=5)  # Adjusted spacing for visual separation

#         # Dynamically adding customer details
#         customer_details = [
#             f"Customer ID: {customer.get('customer_id', '')}",
#             f"First Name: {customer.get('first_name', '')}",
#             f"Last Name: {customer.get('last_name', '')}",
#             f"Address: {customer.get('address', '')}",
#             f"ZIP: {customer.get('zip', '')}",
#             f"City: {customer.get('city', '')}"
#         ]

#         for detail in customer_details:
#             customer_info.controls.append(ft.Text(value=detail))

#         # Add the customer info to the main container
#         customers_container.controls.append(customer_info)

#         # Add a simple text separator for visual separation between entries if not the last item
#         if customer != customer_data["customers"][-1]:
#             separator = ft.Text(value="----------", text_align="center")
#             customers_container.controls.append(separator)

#     return customers_container



# def main(page: ft.Page):
#     page.title = "Customer Information"
#     page.vertical_alignment = ft.MainAxisAlignment.START

#     engine = DBEngineWrapper()

#     # UI Elements
#     customer_id_input = ft.TextField(label="Enter Customer ID", width=300)
#     fetch_button = ft.ElevatedButton(text="Fetch Customer Info", on_click=lambda e: fetch_customer_info(page, engine, customer_id_input.value))
#     customer_info_text = ft.Text("", size=20)

#     page.add(customer_id_input, fetch_button, customer_info_text)
#     fetch_all_button = ft.ElevatedButton(text="Fetch All Customers", on_click=lambda e: fetch_all_customers(page, engine))
#     all_customers_container = ft.Column()

#     page.add(fetch_all_button, all_customers_container)

# def fetch_all_customers(page: ft.Page, engine: DBEngineWrapper):
#     customer_data = engine.queryCustomers()
#     if "error" in customer_data:
#         all_customers_info = customer_data["error"]
#         page.add(ft.Text(all_customers_info, size=20))
#     else:
#         customer_ui = create_customer_ui(customer_data)
#         page.controls[-1] = customer_ui  # This line replaces the last control with the new customer UI
#         page.update()
    
# def fetch_customer_info(page: ft.Page, engine: DBEngineWrapper, customer_id: str):
#     try:
#         customer_id_int = int(customer_id)
#         customer_data = engine.getCustomer(customer_id_int)
#         customer_info = json.dumps(customer_data, indent=2)
#     except ValueError:
#         customer_info = "Invalid Customer ID. Please enter a valid number."
#     except Exception as e:
#         customer_info = f"Error fetching customer info: {str(e)}"
    
#     page.controls[-1].value = customer_info  # Assumes the last control is the Text widget for displaying customer info
#     page.update()

# # Replace 'if __name__ == "__main__":' block with this call to start the Flet app
# ft.app(target=main)

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
    customer_info_container = ft.Column()  # Use a Column to dynamically display customer info

    page.add(customer_id_input, fetch_button, customer_info_container)
    fetch_all_button = ft.ElevatedButton(text="Fetch All Customers", on_click=lambda e: fetch_all_customers(page, engine))
    all_customers_container = ft.Column()

    page.add(fetch_all_button, all_customers_container)

def fetch_all_customers(page: ft.Page, engine: DBEngineWrapper):
    customer_data = engine.queryCustomers()
    if "error" in customer_data:
        page.controls[-1].controls = [ft.Text(customer_data["error"], size=20)]
    else:
        all_customers_container = page.controls[-1]  # Assumes the last control is the container for all customers
        all_customers_container.controls.clear()  # Clear existing customer buttons if any
        for customer in customer_data["customers"]:
            # We use a lambda function to capture the current customer ID and use it in the on_click event
            customer_btn = ft.ElevatedButton(
                text=f"ID: {customer['customer_id']} - {customer['first_name']} {customer['last_name']}",
                on_click=lambda e, cid=customer['customer_id']: fetch_customer_info(page, engine, str(cid))
            )
            all_customers_container.controls.append(customer_btn)
        page.update()


def fetch_customer_info(page: ft.Page, engine: DBEngineWrapper, customer_id_str):
    customer_id = int(customer_id_str)  # Convert customer ID from string to integer
    customer_data = engine.getCustomer(customer_id)
    customer_info_container = page.controls[2]  # Assumes the third control is for displaying customer info
    customer_info_container.controls.clear()  # Clear existing info if any
    
    # Display customer details
    if "error" not in customer_data:
        customer_details = f"""
        ID: {customer_data.get('customer_id', 'N/A')}\n
        First Name: {customer_data.get('customer_firstName', 'N/A')}\n
        Last Name: {customer_data.get('customer_lastName', 'N/A')}\n
        Address: {customer_data.get('customer_address', 'N/A')}\n
        ZIP: {customer_data.get('customer_zip', 'N/A')}\n
        City: {customer_data.get('customer_city', 'N/A')}
        """
        customer_info_container.controls.append(ft.Text(customer_details))
    else:
        customer_info_container.controls.append(ft.Text("Customer information could not be fetched.", size=20))

    page.update()


ft.app(target=main)
