import flet as ft
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

global_bill = []

def get_invoice(invoice):
    global global_bill
    global_bill = invoice
    
def get_customer():
	c = conn.cursor()
	c.execute("SELECT * FROM clients WHERE id=?", (0, ))
	invoice = list(c.fetchone())
	get_invoice(invoice)
	conn.commit()
    

def generate_bill_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, f"INVOICE {global_bill[0]}")
    c.drawString(100, 730, "Customer Name: ")
    c.drawString(100, 710, "Items:")
    y_position = 690
    y_position -= 20
    c.drawString(100, y_position, "Total: ")
    c.save()
    
        
def generate_bill(e):
    page = e.page
    page.snack_bar = ft.SnackBar(ft.Text('Successful download!'))
    page.snack_bar.open = True
    generate_bill_pdf(f"{global_bill[2]}__{global_bill[6]}.pdf")
    page.update()
        