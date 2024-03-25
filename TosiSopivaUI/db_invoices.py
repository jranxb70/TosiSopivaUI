from flet import *
import sqlite3
from Bill import get_invoice

conn = sqlite3.connect('invoice.db',check_same_thread=False)

def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS invoice(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
		invoice_date DATE,
		invoice_bankreference TEXT,
		invoice_subtotal REAL,
		invoice_tax REAL,
  		invoice_total REAL,
		invoice_due_date DATE)
		""")
	conn.commit()

tb = DataTable(
	columns=[
     	DataColumn(Text("id")),
		DataColumn(Text("Client")),
		DataColumn(Text("Date")),
		DataColumn(Text("Bank reference")),
		DataColumn(Text("Subotal")),
		DataColumn(Text("Tax")),
		DataColumn(Text("Total")),
		DataColumn(Text("Due date")),
		DataColumn(Text("Show")),
    	DataColumn(Text("Actions")),
	],
	rows=[]
	)

def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM invoice WHERE id=?", (myid,))
		conn.commit()
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)

id_edit = Text()
customer_id = TextField(label="customer id")
date = TextField(label="invoice date")
bank_reference = TextField(label="bank reference")
subtotal = TextField(label="subtotal")
tax = TextField(label="tax") 
total = TextField(label="total") 
due_date = TextField(label="due date")

def hidedlg(e):
	dlg.visible = False
	dlg.update()

def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE invoice SET customer_id=?, invoice_date=?, invoice_bankreference=?, invoice_subtotal=?, invoice_tax=?, invoice_total=?, invoice_due_date=? WHERE id=?",
            (customer_id.value, date.value, bank_reference.value, subtotal.value, tax.value, total.value, due_date.value,  myid))
		conn.commit()
		tb.rows.clear()	
		calldb()
		dlg.visible = False
		dlg.update()
		tb.update()
	except Exception as e:
		print(e)

dlg = Container(
	padding=10,
			content=Column([
				Row([
				Text("Edit Form",size=30,weight="bold"),
				IconButton(icon="close",on_click=hidedlg),
					],alignment="spaceBetween"),
				customer_id,
				date,
				bank_reference,
				subtotal,
				tax,
                total,
                due_date,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	customer_id.value = data_edit['customer_id']
	date.value = data_edit['invoice_date']
	bank_reference.value = data_edit['invoice_bankreference']
	subtotal.value = data_edit['invoice_subtotal']
	tax.value = data_edit['invoice_tax']
	total.value = data_edit['invoice_total']
	due_date.value = data_edit['invoice_due_date']

	dlg.visible = True
	dlg.update()
 
bill = DataTable(
	columns=[
     	DataColumn(Text("id")),
		DataColumn(Text("Client")),
		DataColumn(Text("Date")),
		DataColumn(Text("Bank reference")),
		DataColumn(Text("Subtotal")),
		DataColumn(Text("Tax")),
		DataColumn(Text("Total")),
		DataColumn(Text("Due date")),
	],
	rows=[]
	)

def show_detail(e):
	page = e.page
	my_id = int(e.control.data)
	c = conn.cursor()
	c.execute("SELECT * FROM invoice WHERE id=?", (my_id, ))
	invoice = list(c.fetchone())
	get_invoice(invoice)
	bill.rows.clear()
	bill.rows.append(
		DataRow(
            cells=[
                DataCell(Text(invoice[0])),
                DataCell(Text(invoice[1])),
                DataCell(Text(invoice[2])),
                DataCell(Text(invoice[3])),
                DataCell(Text(invoice[4])),
                DataCell(Text(invoice[5])),
                DataCell(Text(invoice[6])),
                DataCell(Text(invoice[7])),
            ],
        ),
	)
	conn.commit()
	page.go('/page_invoice_details')
 
def calldb():
	create_table()
	c = conn.cursor()
	c.execute("SELECT * FROM invoice")
	invoices = c.fetchall()
	if not invoices == "":
		keys = ['id', 'customer_id', 'invoice_date', 'invoice_bankreference', 'invoice_subtotal', 'invoice_tax', 'invoice_total', 'invoice_due_date']
		result = [dict(zip(keys, values)) for values in invoices]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(x['id'])),
                        DataCell(Text(x['customer_id'])),
                        DataCell(Text(x['invoice_date'])),
                        DataCell(Text(x['invoice_bankreference'])),
                        DataCell(Text(x['invoice_subtotal'])),
                        DataCell(Text(x['invoice_tax'])),
                        DataCell(Text(x['invoice_total'])),
                        DataCell(Text(x['invoice_due_date'])),
                        DataCell(IconButton(icon="REQUEST_PAGE",icon_color="blue",
                        		data=x['id'],
                        		on_click=show_detail
                        		),
        				),
                        DataCell(Row([
                        	IconButton(icon="EDIT",icon_color="blue",
                        		data=x,
                        		on_click=showedit
                        		),
                        	IconButton(icon="delete",icon_color="red",
                        		data=x['id'],
                        	on_click=showdelete
                        		),
                        	])),
                    ],
                ),

		)

calldb()

dlg.visible = False
mytable = Column([
	dlg,
	Row([tb],scroll="always")
	])