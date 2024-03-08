
# _Success_(return == 0)
# DB_ENGINE_LIBRARY_EXPORT int getWorkingDir(
# 	_Out_   char**				pWorkingDir);

# DB_ENGINE_LIBRARY_EXPORT int getConnectionString(
# 	_Inout_ char**				workingDirectory,
# 	_In_	char*				fileName,
# 	_Out_	char**				connectionString);

import ctypes
import json
import chardet

from DBEngineWrapper import DBEngineWrapper

from ctypes import Structure, c_char_p, c_int, POINTER

class DllUtility():
	def __init__(self):
		getWorkingDir = DBEngineWrapper.get_dll().getWorkingDir		
				
		getWorkingDir.argtypes = [POINTER(c_char_p)]
		getWorkingDir.restype = c_int

		working_dir_ptr = c_char_p()	

		# Call the function
		result = getWorkingDir(ctypes.byref(working_dir_ptr))

		if result == 0:
			working_dir = working_dir_ptr.value.decode('utf-8')
			print(f"Working directory: {working_dir}")
		else:
			print("Error calling getWorkingDir")

		getConnectionString = DBEngineWrapper.get_dll().getConnectionString		
				
		getConnectionString.argtypes = [POINTER(c_char_p), c_char_p, POINTER(c_char_p)]
		getConnectionString.restype = c_int

		#working_dir_ptr = c_char_p()
		#filename = c_char_p()		
		connection_string_ptr = c_char_p()
        # Set the filename
		filename = b"connectionstring.txt"  # Assign the desired filename here			

		# Call the function
		result = getConnectionString(ctypes.byref(working_dir_ptr), filename, ctypes.byref(connection_string_ptr))

		if result == 0:
			detected_encoding = chardet.detect(connection_string_ptr.value)['encoding']
			print(f"Detected encoding: {detected_encoding}")  			
            # Decode the byte sequence using UTF-8
			try:	
				self.connection_string = connection_string_ptr.value.decode(detected_encoding)
				print(f"Connection string: {self.connection_string}")
			except UnicodeDecodeError:
				print("Error decoding connection string (invalid UTF-8 sequence)")
			else:
				print("Error calling getConnectionString")	
		
		freeGlobalVariable = DBEngineWrapper.get_dll().freeGlobalVariable
		freeGlobalVariable.argtypes	= [c_int]
		freeGlobalVariable.restype = c_int
		result = freeGlobalVariable(1)		
		result = freeGlobalVariable(2)		

	def get_database_name(self):
		# Extract the value after "Database="
		db_start = self.connection_string.find("Database=")
		if db_start != -1:
			db_end = self.connection_string.find(";", db_start)
			if db_end != -1:
				return self.connection_string[db_start + len("Database="):db_end]
		return None

	def get_server_name(self):
		# Extract the value after "Server="
		server_start = self.connection_string.find("Server=")
		if server_start != -1:
			server_end = self.connection_string.find(";", server_start)
			if server_end != -1:
				return self.connection_string[server_start + len("Server="):server_end]
		return None
	
	def get_user_name(self):
		# Extract the value after "Uid="
		uid_start = self.connection_string.find("Uid=")
		if uid_start != -1:
			uid_end = self.connection_string.find(";", uid_start)
			if uid_end != -1:
				return self.connection_string[uid_start + len("Uid="):uid_end]
		return None			
	
		
				