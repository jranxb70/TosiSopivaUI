import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from time import gmtime, strftime
from DBEngineWrapper import DBEngineWrapper

import datetime


text_editor = None  # Global variable to hold the text editor widget
                  

class DocumentX(tk.Frame):
    def __init__(self, master=None, application=None, **kwargs):
        super().__init__(master, **kwargs)

        self.app = application
             
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

                        

class ApplicationX(tk.Tk):
    def __init__(self):
        super().__init__()

        self.engine = DBEngineWrapper()
        engine = self.engine        
        customer_data = engine.getCustomer(1)

        engine.queryInvoicesByCustomer()

        # Get the current date and time
        now = datetime.datetime.now()

        # Format the timestamp including milliseconds
        formatted_timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")               

        required_keys = ["customer_id", "invoice_date", "invoice_subtotal", "invoice_total", "invoice_tax", "bank_reference", "invoice_lines"]
        customer_id = 3
        invoice_tax_percent = 0.25 + 1      
        invoice_subtotal = 10.50
        invoice_total = invoice_subtotal * invoice_tax_percent
        invoice_tax = invoice_total - invoice_subtotal
        bank_reference = "10558"
        invoice_lines = []
        product_name = "product_name"
        quantity = "quantity"
        price = "price"
        productname = "Ale"
        product_quantity = 10
        product_price = 2.50
        invoice_lines.append({f"{product_name}": productname, f"{quantity}": product_quantity, f"{price}": product_price})

        engine.addNewInvoice(customer_id=customer_id, invoice_date=formatted_timestamp, invoice_subtotal=invoice_subtotal, invoice_total=invoice_total, invoice_tax=invoice_tax, bank_reference=bank_reference, invoice_lines=invoice_lines)

        address = "Tuppukoskentie 6"

        engine.addCustomer("Matti", "Aalto", address, "65300","Vaasa")        

        self.title('Invoice')
        self.geometry("350x220")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Add some documents
        for i in range(1):
            doc = DocumentX(self.notebook, application=self)
            self.notebook.add(doc, text=f"Document {i+1}")  


if __name__ == "__main__":
    app = ApplicationX()
    app.mainloop()
