import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from time import gmtime, strftime

import datetime
import ctypes
import json
import chardet

from ctypes import Structure, c_char_p, POINTER

class SQLErrorDetails(Structure):
    _fields_ = [("sqlstate", c_char_p * 6),
                ("native_error", ctypes.c_int),
                ("message", c_char_p * 512),#SQL_MAX_MESSAGE_LENGTH),
                ("message_len", ctypes.c_short)]

class node_t(Structure):
    pass

node_t._fields_ = [("val", SQLErrorDetails),
                   ("next", POINTER(node_t))]


text_editor = None  # Global variable to hold the text editor widget

class DBEngineWrapper():
    def __init__(self):
        # Load the shared library
        if ctypes.sizeof(ctypes.c_void_p) == 4:
            self.add_lib = ctypes.CDLL('./engine.so')  # Linux
        else:
            self.add_lib = ctypes.CDLL('..\\..\\TosiSopivaLaskutus\\out\\build\\x64-Debug\\bin\\engine.dll')  # Windows 

    def getEngine(self):
        return self.add_lib     

    def getCustomer(self, customer_id):
        
        getCustomerCharOut = self.add_lib.getCustomerCharOut
        release = self.add_lib.free_json_data      
        getCustomerCharOut.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
        getCustomerCharOut.restype = ctypes.c_int

        # Create a pointer to a char buffer
        json_data_ptr = ctypes.c_char_p()

        # Call the C function
        result = getCustomerCharOut(customer_id, ctypes.byref(json_data_ptr))
        
        customer_data = json.loads(json_data_ptr.value.decode())
        release.argtypes = [ctypes.c_int]
        release.restype = ctypes.c_int
        tuppu = release(2)                        
        return customer_data

    def queryInvoicesByCustomer(self):

        queryInvoicesByCustomer = self.add_lib.queryInvoicesByCustomer
        queryInvoicesByCustomer.argtypes = []        
        json_data_ptr = ctypes.c_char_p()
        error_list_ptr = ctypes.POINTER(node_t)()        
        
        queryInvoicesByCustomer(1, ctypes.byref(json_data_ptr), ctypes.byref(error_list_ptr))

        #print("Natiivi intiaani error: {}".format(error_list_ptr))            

        cont = json_data_ptr.value
        detected_encoding = chardet.detect(cont)['encoding']
        print(f"Detected encoding: {detected_encoding}")        
        try:
            theBlockOfFlats = json_data_ptr.value.decode(detected_encoding) # 'ISO-8859-1' or 'utf-8'           
            json_dict = json.loads(theBlockOfFlats)
        except json.JSONDecodeError:            
            pass
        except UnicodeDecodeError:
            pass                             
        except Exception:
            pass                

        free_json_data = self.add_lib.free_json_data
        free_sql_error_details = self.add_lib.free_sql_error_details
         
        free_json_data.argtypes = [ctypes.c_int]
        free_json_data = ctypes.c_int
        code = free_json_data(1)
        free_sql_error_details()   

    def addCustomer(self, customer_firstName, customer_lastName, customer_address, customer_zip, customer_city):

        addCustomer = self.add_lib.addCustomer
        addCustomer.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        addCustomer.restype = None

        customer_id = ctypes.c_int()  

        customer_firstName = customer_firstName.encode("utf-8")
        customer_lastName = customer_lastName.encode("utf-8")
        customer_address = customer_address.encode("utf-8")
        customer_zip = customer_zip.encode("utf-8")
        customer_city = customer_city.encode("utf-8")

        addCustomer(customer_firstName, customer_lastName, customer_address, customer_zip, customer_city, customer_id)

    def addNewInvoice(self, **kwargs):

        # Define the required keys
        required_keys = ["customer_id", "invoice_date", "invoice_subtotal", "invoice_total", "invoice_tax", "bank_reference", "invoice_lines"]

        # Check if all required keys are present
        for key in required_keys:
            if key not in kwargs:
                raise ValueError(f"Missing required key: {key}")
            
        for key, value in kwargs.items():
            print(f"{key}: {value}")

        # Validate invoice_lines
        invoice_lines = kwargs.get("invoice_lines", [])
        if not invoice_lines:
            raise ValueError("invoice_lines must contain at least one item")

        for item in invoice_lines:
            required_item_keys = ["product_name", "quantity", "price"]
            for item_key in required_item_keys:
                if item_key not in item:
                    raise ValueError(f"Missing required key in invoice_lines item: {item_key}")
         
        # Create a new invoice dictionary
        new_invoice = {
            "customer_id": -1,
            "invoice_date": "",
            "invoice_subtotal": None,
            "invoice_total": None,
            "invoice_tax": None,
            "bank_reference": "",
            "invoice_lines": []
        }

        # Populate the new_invoice dictionary with values from kwargs
        for key, value in kwargs.items():
            new_invoice[key] = value

        addNewInvoiceData = self.add_lib.addNewInvoiceData
        addNewInvoiceData.argtypes = [ctypes.c_char_p, ctypes.c_int]
        addNewInvoiceData.restype = None
        
        # Convert the JSON object to a string      
        json_str = json.dumps(new_invoice)
        enc = json_str.encode()
        l = len(json_str)        

        # Call the C function with the JSON data
        addNewInvoiceData(enc, l)                                      

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

    def getEngine(self):
        return self.add_lib        


if __name__ == "__main__":
    app = ApplicationX()
    app.mainloop()


    # muutos