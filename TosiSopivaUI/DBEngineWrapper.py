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


class DBEngineWrapper():
    _class_lib =None    
    def __init__(self):
        # Load the shared library
        if ctypes.sizeof(ctypes.c_void_p) == 4:
            DBEngineWrapper._class_lib = ctypes.CDLL('./engine.so')  # Linux
        else:
            DBEngineWrapper._class_lib = ctypes.CDLL('..\\..\\TosiSopivaLaskutus\\out\\build\\x64-Debug\\bin\\engine.dll')  # Windows
            # DBEngineWrapper._class_lib = ctypes.CDLL('.\\engine.dll')  # Windows            

    @staticmethod
    def get_dll():
        return DBEngineWrapper._class_lib
    
    def getCustomer(self, customer_id):
        
        getCustomerCharOut = DBEngineWrapper.get_dll().getCustomerCharOut
        release = DBEngineWrapper.get_dll().free_json_data      
        getCustomerCharOut.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
        getCustomerCharOut.restype = ctypes.c_int

        # Create a pointer to a char buffer
        json_data_ptr = ctypes.c_char_p()

        # Call the C function
        result = getCustomerCharOut(customer_id, ctypes.byref(json_data_ptr))
        
        cont = json_data_ptr.value
        detected_encoding = chardet.detect(cont)['encoding']
        customer_data = json.loads(json_data_ptr.value.decode(detected_encoding))
        release.argtypes = [ctypes.c_int]
        release.restype = ctypes.c_int
        tuppu = release(2)
                               
        return customer_data
    
    def addDBUser(self,login, password, email):
        addDBUserFunc = DBEngineWrapper.get_dll().addDBUser
        addDBUserFunc.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        addDBUserFunc.restype = ctypes.c_int

        # user_id = ctypes.c_int()
        login_encoded = login.encode("utf-8")
        password_encoded = password.encode("utf-8")
        email_encoded = email.encode("utf-8")

        result = addDBUserFunc(login_encoded, password_encoded, email_encoded)

        return result
    
    def getDBUser(self, login, user_password):
        getDBUserFunc = DBEngineWrapper.get_dll().getDBUser
        getDBUserFunc.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        getDBUserFunc.restype = ctypes.c_int

        login_encoded = login.encode("utf-8")
        password_encoded = user_password.encode("utf-8")

        access = getDBUserFunc(login_encoded, password_encoded)

        return access
    
    def queryInvoices(self, procedure_switch, start_date, end_date, sorting):
        queryInvoices = DBEngineWrapper.get_dll().queryInvoices
        queryInvoices.argtypes = [
        ctypes.c_long,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_long,
        ctypes.POINTER(ctypes.c_char_p)
        ]
        queryInvoices.restype = ctypes.c_int
        
        start_date_bytes = ctypes.c_char_p(start_date.encode('utf-8')) if start_date else None
        end_date_bytes = ctypes.c_char_p(end_date.encode('utf-8')) if end_date else None
    
    
        json_data_ptr = ctypes.c_char_p()
        result = queryInvoices(
            procedure_switch,
            start_date_bytes,
            end_date_bytes,
            sorting,
            ctypes.byref(json_data_ptr)
        )
    
    # Process the result
        if result != 0:
            print("Error:", result)
            return None
    
        cont = json_data_ptr.value
        detected_encoding = chardet.detect(cont)['encoding']
        # print(f"Detected encoding: {detected_encoding}")
    
        try:
            json_dict = json.loads(cont.decode(detected_encoding))
        except (json.JSONDecodeError, UnicodeDecodeError, Exception) as e:
            print(f"Error decoding JSON data: {e}")
            json_dict = {}
    
    # Free resources
        free_json_data = DBEngineWrapper.get_dll().free_json_data
        free_sql_error_details = DBEngineWrapper.get_dll().free_sql_error_details
        free_json_data.argtypes = [ctypes.c_int]
        free_json_data(1)
        free_sql_error_details()
    
        return json_dict
    

    def queryInvoicesByCustomer(self, customer_id):

        queryInvoicesByCustomer = DBEngineWrapper.get_dll().queryInvoicesByCustomer
        queryInvoicesByCustomer.argtypes = []        
        json_data_ptr = ctypes.c_char_p()
        error_list_ptr = ctypes.POINTER(node_t)()        
        
        queryInvoicesByCustomer(customer_id, ctypes.byref(json_data_ptr), ctypes.byref(error_list_ptr))

        cont = json_data_ptr.value
        detected_encoding = chardet.detect(cont)['encoding']
        # print(f"Detected encoding: {detected_encoding}")        
        try:
            # 'ISO-8859-1' or 'utf-8'           
            json_dict = json.loads(json_data_ptr.value.decode(detected_encoding))
        except json.JSONDecodeError:            
            pass
        except UnicodeDecodeError:
            pass                             
        except Exception:
            pass                

        free_json_data = DBEngineWrapper.get_dll().free_json_data
        free_sql_error_details = DBEngineWrapper.get_dll().free_sql_error_details
         
        free_json_data.argtypes = [ctypes.c_int]
        free_json_data = ctypes.c_int
        
        code = free_json_data(1)
        
        free_sql_error_details()   
        return json_dict        

    def queryCustomers(self):

        queryCustomers = DBEngineWrapper.get_dll().queryCustomers
        queryCustomers.argtypes = []        
        json_data_ptr = ctypes.c_char_p()
        error_list_ptr = ctypes.POINTER(node_t)()        
        try:
            queryCustomers(ctypes.byref(json_data_ptr), ctypes.byref(error_list_ptr))
        except Exception:
            pass        

        cont = json_data_ptr.value
        detected_encoding = chardet.detect(cont)['encoding']
        # print(f"Detected encoding: {detected_encoding}")        
        try:
            # 'ISO-8859-1' or 'utf-8'           
            json_dict = json.loads(json_data_ptr.value.decode(detected_encoding))
        except json.JSONDecodeError:            
            pass
        except UnicodeDecodeError:
            pass                             
        except Exception:
            pass                

        free_json_data = DBEngineWrapper.get_dll().free_json_data
        free_sql_error_details = DBEngineWrapper.get_dll().free_sql_error_details
         
        free_json_data.argtypes = [ctypes.c_int]
        free_json_data = ctypes.c_int
        
        code = free_json_data(1)
        
        free_sql_error_details()   
        return json_dict       

    def addCustomer(self, customer_firstName, customer_lastName, customer_address, customer_zip, customer_city, customer_phone, customer_email):

        addCustomer = DBEngineWrapper.get_dll().addCustomer
        addCustomer.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        addCustomer.restype = None

        customer_id = ctypes.c_int()  

        customer_firstName = customer_firstName.encode("utf-8")
        customer_lastName = customer_lastName.encode("utf-8")
        customer_address = customer_address.encode("utf-8")
        customer_zip = customer_zip.encode("utf-8")
        customer_city = customer_city.encode("utf-8")
        customer_phone = customer_phone.encode("utf-8")
        customer_email = customer_email.encode("utf-8")

        addCustomer(customer_firstName, customer_lastName, customer_address, customer_zip, customer_city, customer_phone, customer_email, customer_id)
        return customer_id.value
    
    def updateCustomer(self, customer_id, customer_firstName, customer_lastName, customer_address, customer_zip, customer_city, customer_phone, customer_email):
        updateCustomerFunc = DBEngineWrapper.get_dll().updateCustomer
        updateCustomerFunc.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        updateCustomerFunc.restype = None

        customer_firstName = customer_firstName.encode("utf-8")
        customer_lastName = customer_lastName.encode("utf-8")
        customer_address = customer_address.encode("utf-8")
        customer_zip = customer_zip.encode("utf-8")
        customer_city = customer_city.encode("utf-8")
        customer_phone = customer_phone.encode("utf-8")
        customer_email = customer_email.encode("utf-8")

        updateCustomerFunc(customer_id, customer_firstName, customer_lastName, customer_address, customer_zip, customer_city, customer_phone, customer_email)
        
    def deleteCustomer(self, customer_id):
        deleteCustomerFunc = DBEngineWrapper.get_dll().deleteCustomer
        deleteCustomerFunc.argtypes = [ctypes.c_long]
        deleteCustomerFunc.restype = None

        deleteCustomerFunc(customer_id)
        
    def addNewInvoice(self, **kwargs):

        # Define the required keys
        required_keys = ["customer_id", "invoice_date", "invoice_subtotal", "invoice_total", "invoice_tax", "bank_reference", "invoice_due_date", "invoice_lines"]

        # Check if all required keys are present
        for key in required_keys:
            if key not in kwargs:
                raise ValueError(f"Missing required key: {key}")
            
        # for key, value in kwargs.items():
        #     print(f"{key}: {value}")

        # Validate invoice_lines
        invoice_lines = kwargs.get("invoice_lines", [])
        if not invoice_lines:
            raise ValueError("invoice_lines must contain at least one item")

        for item in invoice_lines:
            required_item_keys = ["product_item_id", "quantity", "price", "product_description"]
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
            "invoice_due_date": "",            
            "invoice_lines": []
        }

        # Populate the new_invoice dictionary with values from kwargs
        for key, value in kwargs.items():
            new_invoice[key] = value

        addNewInvoiceData = DBEngineWrapper.get_dll().addNewInvoiceData
        addNewInvoiceData.argtypes = [ctypes.c_char_p, ctypes.c_int]
        addNewInvoiceData.restype = ctypes.c_int
        
        # Convert the JSON object to a string      
        json_str = json.dumps(new_invoice)
        enc = json_str.encode()
        l = len(json_str)        

        # Call the C function with the JSON data
        value = addNewInvoiceData(enc, l)
        return value

    def query_invoice_by_id(self, invoice_id):
        queryInvoiceById = DBEngineWrapper.get_dll().queryInvoiceById
        #queryInvoiceById.argtypes = [ ctypes.c_int ]
        queryInvoiceById.restype = None

        json_data_ptr = ctypes.c_char_p()
        error_list_ptr = ctypes.POINTER(node_t)()
        
        try:
            queryInvoiceById(invoice_id, ctypes.byref(json_data_ptr), ctypes.byref(error_list_ptr))
        except Exception:
            pass                        

        cont = json_data_ptr.value
        detected_encoding = chardet.detect(cont)['encoding']
        # print(f"Detected encoding: {detected_encoding}")        
        try:
            # 'ISO-8859-1' or 'utf-8'           
            json_dict = json.loads(json_data_ptr.value.decode(detected_encoding))
        except json.JSONDecodeError:            
            pass
        except UnicodeDecodeError:
            pass                             
        except Exception:
            pass                

        free_json_data = DBEngineWrapper.get_dll().free_json_data
        free_sql_error_details = DBEngineWrapper.get_dll().free_sql_error_details
         
        free_json_data.argtypes = [ctypes.c_int]
        free_json_data = ctypes.c_int
        
        code = free_json_data(1)
        
        free_sql_error_details()   
        return json_dict        
    
    def addInvoiceLine(self, open_database, invoice_id, product_item_id, invoiceline_quantity, invoiceline_price, product_description):
        addInvoiceLine = DBEngineWrapper.get_dll().addInvoiceLine
        addInvoiceLine.argtypes = [
            ctypes.c_bool,  #bool open_database
            ctypes.c_int,   #int invoice_id
            ctypes.c_int,   #int product_item_id
            ctypes.c_int,   #int invoiceline_quantity
            ctypes.c_double,#double invoiceline_price
            ctypes.c_char_p #char* product_description
        ]
        addInvoiceLine.restype = None
        product_item_id = product_item_id.encode('utf-8')
        invoiceline_quantity = invoiceline_quantity.encode('utf-8')
        invoiceline_price = invoiceline_price.encode('utf-8')
        product_description_bytes = product_description.encode('utf-8')
        
        addInvoiceLine(open_database, invoice_id, int(product_item_id), int(invoiceline_quantity), float(invoiceline_price), product_description_bytes)
        
    def get_company(self, company_id):
        getCompany = DBEngineWrapper.get_dll().getCompany

        getCompany.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
        getCompany.restype = None

        jsonStringCompany = ctypes.POINTER(ctypes.c_char)()
        getCompany(company_id, ctypes.byref(jsonStringCompany))

        json_string = jsonStringCompany.contents.value.decode()

        free_json_string = ctypes.CDLL("libc.so.6").free
        free_json_string.argtypes = [ctypes.c_void_p]
        free_json_string(jsonStringCompany)

        return json_string
        