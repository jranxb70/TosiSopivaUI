import tkinter as tk
import ctypes
import json

from tkinter import messagebox
from tkinter import filedialog


# Load the shared library
if ctypes.sizeof(ctypes.c_void_p) == 4:
    add_lib = ctypes.CDLL('./engine.so')  # Linux
else:
    add_lib = ctypes.CDLL('..\\..\\TosiSopivaLaskutus\\out\\build\\x64-Debug\\bin\\engine.dll')  # Windows

# Define the argument and return types of the function
add_lib.dbOpen.argtypes = [ctypes.c_char_p]
add_lib.dbOpen.restype = ctypes.c_int

# Call the C function 
result = add_lib.dbOpen(b"connectionstring.txt")
print("Result:", result)

if result == 1:
    add_lib.dbOpen.argtypes = [ctypes.c_char_p]
    working_dir_ptr = ctypes.c_char_p()

    add_lib.queryInvoicesByCustomer(73, ctypes.byref(working_dir_ptr))

    json_dict = json.loads(working_dir_ptr.value.decode('utf-8'))

    code = add_lib.free_json_data()

add_lib.dbClose()

text_editor = None  # Global variable to hold the text editor widget

def open_file():
    global text_editor
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        new_window = tk.Toplevel(root)

        #ind = file_path.rfind("/")
        split = file_path.split("/")
        length = len(split)
        fileName = split.pop(length - 1)                  
        # partsandaccessories = file_path.partition("/")
        # for element in partsandaccessories:
        #     if element.count("/") > 0 and len(element) > 1:      
        #         partsandaccessories = element.partition("/")                 
            #partsandaccessories.    
        new_window.title(fileName)
        new_window.geometry("400x300+{}+{}".format(root.winfo_rootx() + 50, root.winfo_rooty() + 50))        
        #new_window.geometry("400x300")  
        new_window.transient(root)       
        text_editor = tk.Text(new_window)
        text_editor.pack(fill=tk.BOTH, expand=True)        
                      
        if text_editor:
            with open(file_path, 'r', encoding="UTF-8") as file:
                content = file.read()
            text_editor.delete(1.0, tk.END)
            text_editor.insert(tk.END, content)
        else:
            messagebox.showerror("Error", "No document is currently open.")

def save_file():
    global text_editor
    if text_editor:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = text_editor.get(1.0, tk.END)
                file.write(content)
            messagebox.showinfo("Save", "File saved successfully.")
    else:
        messagebox.showerror("Error", "No document is currently open.")

def create_new_document():
    global text_editor
    new_window = tk.Toplevel(root)
    new_window.title("New Document")
    new_window.geometry("400x300")
    text_editor = tk.Text(new_window)
    text_editor.pack(fill=tk.BOTH, expand=True)

def copy_text():
    global text_editor
    if text_editor:
        text_editor.event_generate("<<Copy>>")

def cut_text():
    global text_editor
    if text_editor:
        text_editor.event_generate("<<Cut>>")

def paste_text():
    global text_editor
    if text_editor:
        text_editor.event_generate("<<Paste>>")

def show_help():
    messagebox.showinfo("Help", "Help information...")

# Create main window
root = tk.Tk()
root.title("Menu Example")

# Create menu bar
menu_bar = tk.Menu(root)

# Create File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=create_new_document)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Paste", command=paste_text)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Create Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_help)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Attach menu bar to root window
root.config(menu=menu_bar)

# Run the main event loop
root.mainloop()
