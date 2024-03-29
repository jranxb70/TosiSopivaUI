import flet as ft
from flet import *
from flet_route import Routing, path
from views.home import Home
from views.page_reg import page_reg
from views.page_auth import page_auth
from views.page_all_clients import page_all_clients
from views.page_all_products import page_all_products
from views.temp_nav import temp_nav

def main(page: ft.Page):
    app_routes = [
        
        path(url="/", clear= True,view=Home),
        path(url="/page_reg",clear= True, view=page_reg),
        path(url="/page_auth",clear= True, view=page_auth),
        path(url="/page_all_clients",clear= True, view=page_all_clients),
        path(url="/page_all_products",clear= True, view=page_all_products),
        path(url="/temp_nav",clear= True, view=temp_nav),
    ]
    
    Routing(page=page, app_routes=app_routes)
  
    
    page.go(page.route)
    
#if __name__ == '__main__':
    #ft.app(target=main)
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from DBEngineWrapper import DBEngineWrapper
from BankReferenceCalc import BankReferenceCalc
from DllUtility import DllUtility

from datetime import datetime


text_editor = None  # Global variable to hold the text editor widget
                  

class Document(tk.Frame):
    def __init__(self, master=None, application=None, **kwargs):
        super().__init__(master, **kwargs)

        self.app = application

        eng = self.app.get_engine()

        c = eng.getCustomer(3)             
             
        fields = {}

        fields['firstname_label'] = ttk.Label(text='First name:')
        fields['firstname'] = ttk.Entry()

        fields['lastname_label'] = ttk.Label(text='Last name:')
        fields['lastname'] = ttk.Entry(show="*")

        fields['address_label'] = ttk.Label(text='Address:')
        fields['address'] = ttk.Entry()

        fields['zip_label'] = ttk.Label(text='Zip:')
        fields['zip'] = ttk.Entry(show="*")      

        fields['city_label'] = ttk.Label(text='City:')
        fields['city'] = ttk.Entry(show="*")            

        self.entries = {}
        
        for field in fields.values():
            if (isinstance(field, ttk.Label)):     
                field.pack(anchor=tk.W, padx=20, pady=0, fill=tk.X)            
            if (isinstance(field, ttk.Entry)):     
                field.pack(anchor=tk.W, padx=20, pady=5, fill=tk.X)

        ttk.Button(text='Save', command=self.save).pack(anchor=tk.W, padx=20, pady=5)

        self.entries['firstname'] =  fields['firstname']
        self.entries['lastname'] =   fields['lastname']
        self.entries['address'] =  fields['address']
        self.entries['zip'] =   fields['zip']               
        self.entries['city'] =   fields['city']   
             

    def save(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        messagebox.showinfo("Saved", f"Saved data: {data}")    

                        

class Application(tk.Tk):

    def get_engine(self):
        return self.engine            
    
    def __init__(self):
        super().__init__()

        self.engine = DBEngineWrapper()

        diagnose = DllUtility()
        
        db = diagnose.get_database_name()
        user = diagnose.get_user_name()
        server = diagnose.get_server_name()

        invoice = self.query_invoice_by_id(1)      

        customers = self.query_customers()  
        
        customer_id = self.add_customer("Pasi", "Männistö", "Pajuluomantie 4", "60100", "Seinäjoki", "964-120229", "pasi.mannisto@geramail.com")

        customer_data = self.query_customer(customer_id)

        insult = self.add_new_invoice(customer_id)

        json_data = self.query_invoices_by_customer(customer_id)
        print(json_data);        

        self.title('Invoice')
        self.geometry("350x220")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Add some documents
        for i in range(1):
            doc = Document(self.notebook, application=self)
            self.notebook.add(doc, text=f"Document {i+1}")
               
    def query_customer(self, customer_id):
        engine = self.engine        
        customer_data = engine.getCustomer(customer_id)
        return customer_data

    def query_customers(self):
        engine = self.engine        
        customer_data = engine.queryCustomers()
        return customer_data  

    def query_invoice_by_id(self, invoice_id):
        engine = self.engine                      
        return engine.query_invoice_by_id(invoice_id)

    def query_invoices_by_customer(self, customer_id):
        engine = self.engine            
        return engine.queryInvoicesByCustomer(customer_id)

    def modify_timestamp2(self, original_time):
        # Parse the original timestamp
        time_stamp =  original_time.strftime("%Y-%m-%d %H:%M:%S.%f")        
        dt = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S.%f")
        #mic = dt.microsecond
        #dt = dt.replace(microsecond=0)
             
        # Format the timestamp with 7 digits of fractional seconds
        modified_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        modified_timestamp = modified_timestamp + '000'

        # NOTE: fractions are in microseconds in python
        # Sql Server ODBC driver requires the fractions to be nanoseconds
        # However, Sql Server won't accept the precision that is below 0,1 microseconds
        # Therefore three zeros are concut at the end of fractions here       

        return modified_timestamp      

    def add_new_invoice(self, customer_id):
        engine = self.engine                      
        # Get the current date and time

        now = datetime.now()

        # Format the timestamp including milliseconds
        formatted_timestamp = self.modify_timestamp2(now)
        
        print(f"Modified timestamp: {formatted_timestamp}")        

        product_item_id = "product_item_id"
        #product_name = "product_name"
        quantity = "quantity"
        price = "price"

        product_description = "product_description"
        productDescription  = "Olut Ale 0,33l 4,3%"
        
        #productname = "Ale"
        productItemId = 2        
        product_quantity = 10
        product_price = 2.50                   

        invoice_tax_percent = 0.25 + 1      
        invoice_subtotal = product_quantity * product_price
        invoice_total = invoice_subtotal * invoice_tax_percent
        invoice_tax = invoice_total - invoice_subtotal
        
        bankreference = 1000
        bankreference = bankreference + customer_id   
        
        bank_reference = f"{BankReferenceCalc.calc_new_reference(bankreference)}"

        invoice_due_date = "2024-04-10"#formatted_timestamp""
        
        invoice_lines = []

        invoice_lines.append({f"{product_item_id}": productItemId, f"{quantity}": product_quantity, f"{price}": product_price, f"{product_description}": productDescription})

        return engine.addNewInvoice(customer_id=customer_id, invoice_date=formatted_timestamp, invoice_subtotal=invoice_subtotal, invoice_total=invoice_total, invoice_tax=invoice_tax, bank_reference=bank_reference, invoice_due_date=invoice_due_date, invoice_lines=invoice_lines)          

    def add_customer(self, first_name, last_name, address, zip, city, phone, email):
        engine = self.engine

        customer_id = engine.addCustomer(first_name, last_name, address, zip, city, phone, email)    
        return customer_id                                


if __name__ == "__main__":
     app = Application()
     app.mainloop()
