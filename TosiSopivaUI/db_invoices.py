from flet import *
import sqlite3
from Bill import get_invoice
from views.page_invoice_line import get_id
from db_invoice_line import db_get_id

from DBEngineWrapper import DBEngineWrapper
engine = DBEngineWrapper()

conn = sqlite3.connect('invoice.db',check_same_thread=False)

# def create_table():
# 	c = conn.cursor()
# 	c.execute("""CREATE TABLE IF NOT EXISTS invoice(
# 		id INTEGER PRIMARY KEY AUTOINCREMENT,
#         customer_id INTEGER,
# 		invoice_date DATE,
# 		invoice_bankreference TEXT,
# 		invoice_subtotal REAL,
# 		invoice_tax REAL,
#   		invoice_total REAL,
# 		invoice_due_date DATE)
# 		""")
# 	conn.commit()

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
		DataColumn(Text("Outstanding balance")),
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
     	DataColumn(Text("ID")),
		DataColumn(Text("Client name")),
		DataColumn(Text("Client surname")),
		DataColumn(Text("Client phone")),
		DataColumn(Text("Bank reference")),
		DataColumn(Text("Date")),
		DataColumn(Text("Total")),
		DataColumn(Text("Due date")),
	],
	rows=[]
	)

def show_detail(e):
	page = e.page
	my_id = int(e.control.data)
	get_id(my_id)
	db_get_id(my_id)
	# c = conn.cursor()
	# c.execute("SELECT * FROM invoice WHERE id=?", (my_id, ))
	# invoice = list(c.fetchone())
	invoice = engine.query_invoice_by_id(my_id)
	get_invoice(invoice)
	bill.rows.clear()
	bill.rows.append(
		DataRow(
            cells=[
                DataCell(Text(invoice['invoice_id'])),
                DataCell(Text(invoice['first_name'])),
                DataCell(Text(invoice['last_name'])),
				DataCell(Text(invoice['phone'])),
                DataCell(Text(invoice['invoice_bank_reference'])),
                DataCell(Text(invoice['invoice_date'])),
                DataCell(Text(invoice['invoice_total'])),
                DataCell(Text(invoice['invoice_due_date'])),
            ],
        ),
	)
	conn.commit()
	page.go('/page_invoice_details')
 
def calldb():
	# create_table()
	# c = conn.cursor()
	# c.execute("SELECT * FROM invoice")
	# invoices = c.fetchall()
	# invoices = engine.query_invoice_by_id(1)
	invoices = engine.queryInvoices(1, "2024-03-01 0:00:00.0000000", "2024-03-31 0:00:00.0000000", 1)
	print(invoices)
	if not invoices == "":
		# for key, value in invoices.items():
		# print(f"{key}: {value}")
		# keys = ['id', 'customer_id', 'invoice_date', 'invoice_bankreference', 'invoice_subtotal', 'invoice_tax', 'invoice_total', 'invoice_due_date']
		# result = [dict(zip(keys, values)) for values in invoices]
		for invoice in invoices['invoices']:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(invoice['invoice_id'])),
                        DataCell(Text(invoice['customer_id'])),
                        DataCell(Text(invoice['invoice_date'])),
                        DataCell(Text(invoice['invoice_bankreference'])),
                        DataCell(Text(invoice['invoice_subtotal'])),
                        DataCell(Text(invoice['invoice_tax'])),
                        DataCell(Text(invoice['invoice_total'])),
                        DataCell(Text(invoice['invoice_due_date'])),
                        DataCell(Text(invoice['invoice_outstanding_balance'])),
                        DataCell(IconButton(icon="REQUEST_PAGE",icon_color="blue",
                        		data=invoice['invoice_id'],
                        		on_click=show_detail
                        		),
        				),
                        DataCell(Row([
                        	IconButton(icon="EDIT",icon_color="blue",
                        		data=invoice,
                        		on_click=showedit
                        		),
                        	IconButton(icon="delete",icon_color="red",
                        		data=invoice['invoice_id'],
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