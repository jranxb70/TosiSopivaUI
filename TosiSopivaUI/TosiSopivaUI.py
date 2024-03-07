import flet as ft
from ctypes import Structure, c_char_p, POINTER, c_int, CDLL
import ctypes
import json
import chardet

class SQLErrorDetails(Structure):
    _fields_ = [("sqlstate", c_char_p * 6),
                ("native_error", ctypes.c_int),
                ("message", c_char_p * 512),  # SQL_MAX_MESSAGE_LENGTH
                ("message_len", ctypes.c_short)]

class node_t(Structure):
    pass

node_t._fields_ = [("val", SQLErrorDetails),
                   ("next", POINTER(node_t))]

class DBEngineWrapper:
    # DBEngineWrapper code here without GUI related code
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

    pass

def main(page: ft.Page):
    page.title = "Customer Information"
    page.vertical_alignment = ft.MainAxisAlignment.START

    engine = DBEngineWrapper()

    # UI Elements
    customer_id_input = ft.TextField(label="Enter Customer ID", width=300)
    fetch_button = ft.ElevatedButton(text="Fetch Customer Info", on_click=lambda e: fetch_customer_info(page, engine, customer_id_input.value))
    customer_info_text = ft.Text("", size=20)

    page.add(customer_id_input, fetch_button, customer_info_text)

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