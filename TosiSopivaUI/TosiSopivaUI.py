import tkinter as tk
from tkinter import ttk, messagebox

import ctypes
import json

from tkinter import messagebox
from tkinter import filedialog

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



result = 0
if result == 1:
    add_lib.addCustomer.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(node_t))]                              
    add_lib.addCustomer.restype = None    
   
    customer_id = ctypes.c_int()
    # add_lib.addCustomer("Esko".encode('utf-8'), "Viitala".encode('utf-8'), "Hietaharjunkatu 77".encode('utf-8'), "60200".encode('utf-8'), "SEINAJOKI".encode('utf-8'), ctypes.byref(customer_id))
    
    #add_lib.dbOpen.argtypes = [ctypes.c_char_p]
    json_data_ptr = ctypes.c_char_p()
    error_list_ptr = ctypes.POINTER(node_t)()    

    add_lib.queryInvoicesByCustomer(1, ctypes.byref(json_data_ptr), ctypes.byref(error_list_ptr))

    print("Natiivi intiaani error: {}".format(error_list_ptr.contents.val.native_error))
    print(error_list_ptr.contents.val.message)

    b = error_list_ptr.contents.val.message     

    json_dict = json.loads(json_data_ptr.value.decode('utf-8'))

    code = add_lib.free_json_data()
    add_lib.free_sql_error_details()   


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
        self.save_()               

    def save(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        messagebox.showinfo("Saved", f"Saved data: {data}")    

    def save_(self):
        self.app.add_lib.addCustomer.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.POINTER(node_t))]                              
        self.app.add_lib.addCustomer.restype = None    
   
        customer_id = ctypes.c_int()  
 
        json_data_ptr = ctypes.c_char_p()
        error_list_ptr = ctypes.POINTER(node_t)()    

        self.app.add_lib.queryInvoicesByCustomer(1, ctypes.byref(json_data_ptr), ctypes.byref(error_list_ptr))

        print("Natiivi intiaani error: {}".format(error_list_ptr))


        # Define the C function signature
        addNewInvoiceData = self.app.add_lib.addNewInvoiceData
        addNewInvoiceData.argtypes = [ctypes.c_char_p, ctypes.c_int]
        addNewInvoiceData.restype = None

        # Create a sample JSON object

        sample_json = {
            "customer_id": 1, 
            "invoice_date": "2017-01-10 17:00:05.00000", 
            "invoice_subtotal": 33.760000, 
            "invoice_total": 42.200000, 
            "invoice_tax": 8.440000, 
            "bank_reference" : "10731", 
            "invoice_lines" : 
            [
                {
                    "product_name": "kalja", 
                    "quantity": 6, 
                    "price": 1.05
                }, 
                {
                    "product_name": "siideri", 
                    "quantity": 8, 
                    "price": 3.40
                }, 
                {
                    "product_name": "lonkero",
                    "quantity": 12, 
                    "price": 2.25
                }
            ]
        }

        # Convert the JSON object to a string
        json_str = json.dumps(sample_json)

        enc = json_str.encode()
        l = len(json_str)        

        # Call the C function with the JSON data
        addNewInvoiceData(enc, l)           

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

        code = self.app.add_lib.free_json_data()
        self.app.add_lib.free_sql_error_details()                     

class ApplicationX(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Invoice')
        self.geometry("350x220")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Load the shared library
        if ctypes.sizeof(ctypes.c_void_p) == 4:
            self.add_lib = ctypes.CDLL('./engine.so')  # Linux
        else:
            self.add_lib = ctypes.CDLL('..\\..\\TosiSopivaLaskutus\\out\\build\\x64-Debug\\bin\\engine.dll')  # Windows

        # Add some documents
        for i in range(1):
            doc = DocumentX(self.notebook, application=self)
            self.notebook.add(doc, text=f"Document {i+1}")    

    def getEngine(self):
        return self.add_lib        



class Document(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        #self.grid(sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")        

        style = ttk.Style(self)
        style.configure("Bordered.TButton", borderwidth=2, relief="solid")

        # Create text fields for invoicing data
        fields = ["Name", "Address", "City", "Date", "Invoice Number", "Price", "Quantities"]
        self.entries = {}
        for field in fields:
            self.create_field(field)

        # Create a save button
        #self.
        #save_button = ttk.Button(self, text="Save", style="Bordered.TButton", command=self.save)
        #save_button.pack(pady=10, side="left")  # Add padding on the x-axis
       # self.save_button.config(relief="solid", borderwidth=1)  # Add outline

        # Create a save button
        save_button = ttk.Button(self, text="Save", style="Bordered.TButton", command=self.save)
        #save_button.grid(row=8, column=0, pady=10, sticky="w")  # Place the button in the 8th row and 0th column, with some padding on the y-axis and stick to the west (left) side
     

    def create_field(self, field_name):
        frame = ttk.Frame(self)
        #frame.pack(pady=5)  # Add some vertical space between the fields
        label = ttk.Label(frame, text=field_name+":", width=15, anchor='e')
        #label.pack(side="left")
        label.config(relief="solid", borderwidth=1)  # Add outline
        entry = ttk.Entry(frame)
        #entry.pack(side="left", fill='x', expand=True)

        self.entries[field_name] = entry

    def save(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        messagebox.showinfo("Saved", f"Saved data: {data}")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Invoicing Application")
        self.geometry("800x600")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Add some documents
        for i in range(2):
            doc = Document(self.notebook)
            self.notebook.add(doc, text=f"Document {i+1}")

if __name__ == "__main__":
    app = ApplicationX()
    app.mainloop()
