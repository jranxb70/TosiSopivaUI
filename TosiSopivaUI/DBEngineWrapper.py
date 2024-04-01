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
            #DBEngineWrapper._class_lib = ctypes.CDLL('..\\..\\TosiSopivaLaskutus\\out\\build\\x64-Debug\\bin\\engine.dll')  # Windows
            DBEngineWrapper._class_lib = ctypes.CDLL('.\\engine.dll')  # Windows            

    @staticmethod
    def get_dll():
        return DBEngineWrapper._class_lib

    def registerVeryConvenientUser(self, login, passwd, email):
        registerDBUser = DBEngineWrapper.get_dll().addDBUser
        registerDBUser.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        registerDBUser.restype = ctypes.c_int

        login = login.encode("utf-8")
        passwd = passwd.encode("utf-8")
        email = email.encode("utf-8")

        retCode = registerDBUser(login, passwd, email)   
        return retCode

    def getDBUser(self, login, password):
        getDBUser = DBEngineWrapper.get_dll().getDBUser
        getDBUser.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  
        getDBUser.restype = ctypes.c_int  

        login = login.encode("utf-8")
        password = password.encode("utf-8")                    
         
        retcode = getDBUser(login, password) 
        return retcode

    def selectAllInvoices(self, switch):                                 
        selectAllInvoices = DBEngineWrapper.get_dll().queryAllInvoices
        selectAllInvoices.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]    
        selectAllInvoices.restype = None

        # Create a pointer to a char buffer
        json_data_ptr = ctypes.c_char_p()

        selectAllInvoices(switch, ctypes.byref(json_data_ptr))

        cont = json_data_ptr.value
        detected_encoding = chardet.detect(cont)['encoding']
        print(f"Detected encoding: {detected_encoding}")        
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
         
        free_json_data.argtypes = [ctypes.c_int]
        free_json_data.restype = ctypes.c_int
        
        code = free_json_data(3)
        return json_dict       

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

    def queryInvoicesByCustomer(self, customer_id):

        queryInvoicesByCustomer = DBEngineWrapper.get_dll().queryInvoicesByCustomer
        queryInvoicesByCustomer.argtypes = []        
        json_data_ptr = ctypes.c_char_p()
        error_list_ptr = ctypes.POINTER(node_t)()        
        
        queryInvoicesByCustomer(customer_id, ctypes.byref(json_data_ptr), ctypes.byref(error_list_ptr))

        cont = json_data_ptr.value
        detected_encoding = chardet.detect(cont)['encoding']
        print(f"Detected encoding: {detected_encoding}")        
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
        free_json_data.restype = ctypes.c_int
        
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
        print(f"Detected encoding: {detected_encoding}")        
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
        free_json_data.restype = ctypes.c_int
        
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
        updateCustomer = DBEngineWrapper.get_dll().updateCustomer
        updateCustomer.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        updateCustomer.restype = None

        customer_id = ctypes.c_int(customer_id)

        customer_firstName = customer_firstName.encode("utf-8")
        customer_lastName = customer_lastName.encode("utf-8")
        customer_address = customer_address.encode("utf-8")
        customer_zip = customer_zip.encode("utf-8")
        customer_city = customer_city.encode("utf-8")
        customer_phone = customer_phone.encode("utf-8")
        customer_email = customer_email.encode("utf-8")

        updateCustomer(customer_id, customer_firstName, customer_lastName, customer_address, customer_zip, customer_city, customer_phone, customer_email)      
        
    def deleteCustomer(self, customer_id):
        deleteCustomer = DBEngineWrapper.get_dll().deleteCustomer 
        deleteCustomer.argtypes = [ctypes.c_int]
        deleteCustomer.restype = ctypes.c_int

        ret = deleteCustomer(customer_id)
        return ret        

    def addNewInvoice(self, **kwargs):

        # Define the required keys
        required_keys = ["customer_id", "invoice_date", "invoice_subtotal", "invoice_total", "invoice_tax", "bank_reference", "invoice_due_date", "invoice_lines"]

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
        print(f"Detected encoding: {detected_encoding}")        
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
        free_json_data.restype = ctypes.c_int
        
        code = free_json_data(1)
        
        free_sql_error_details()   
        return json_dict                

