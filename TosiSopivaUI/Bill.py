import flet as ft
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

from DBEngineWrapper import DBEngineWrapper
engine = DBEngineWrapper()

global_bill = []
global_customer = []

def get_invoice(invoice):
    global global_bill
    global_bill = invoice
    
def get_customer():
    # c = conn.cursor()
    # c.execute("SELECT * FROM customer WHERE customer_id=?", (global_bill[1], ))
    global global_customer
    # global_customer = list(c.fetchone())
    global_customer = engine.getCustomer(global_bill[1])
    print(global_customer)
    conn.commit()
    

def generate_bill_pdf(filename):
    get_customer()
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(300, 750, f"INVOICE {global_bill[0]}")
    c.drawString(100, 730, f"Customer Name: {global_customer['customer_first_name']}")
    c.drawString(100, 710, f"Customer Surname: {global_customer['customer_last_name']}")
    c.drawString(100, 690, f"Address: {global_customer['customer_address']}")
    c.drawString(100, 670, f"Postal code: {global_customer['customer_zip']}")
    c.drawString(100, 650, f"City: {global_customer['customer_city']}")
    c.drawString(100, 630, f"Phone: {global_customer['customer_phone']}")
    c.drawString(100, 610, f"Email: {global_customer['customer_email']}")
    c.drawString(100, 590, "Items:")
    x = 570
    for i in range(5):
        c.drawString(100, x, "Item:")
        x-=20
    y_position = 490
    y_position -= 20
    c.drawString(100, y_position, "Total: ")
    c.save()
    
        
def generate_bill(e):
    page = e.page
    page.snack_bar = ft.SnackBar(ft.Text('Successful download!'))
    page.snack_bar.open = True
    generate_bill_pdf(f"{global_bill[2]}__{global_bill[6]}.pdf")
    page.update()
        