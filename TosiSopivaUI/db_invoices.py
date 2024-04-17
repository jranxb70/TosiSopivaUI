from flet import *
import sqlite3

from flet_core import page
from Bill import get_invoice
from views.page_invoice_line import get_id
from msgboxes.msgbox_no_connection_string import dlg_modal
from db_invoice_line import db_get_id

from DllUtility import DllUtility
from DBEngineWrapper import DBEngineWrapper


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
	engine = DBEngineWrapper()	
	page = e.page
	my_id = int(e.control.data)
	get_id(my_id)
	db_get_id(my_id)
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
 
def add_invoice(customer_id, invoice_date, invoice_subtotal, invoice_total, invoice_tax, bank_reference, invoice_due_date, invoice_lines):
	engine = DBEngineWrapper()
	engine.addNewInvoice(customer_id=customer_id, invoice_date=invoice_date, invoice_subtotal=invoice_subtotal, invoice_total=invoice_total, invoice_tax=invoice_tax, bank_reference=bank_reference, invoice_due_date=invoice_due_date,invoice_lines=invoice_lines)			
 
def calldb():
	engine = DBEngineWrapper()	
	invoices = engine.queryInvoices(1, "2024-03-01 0:00:00.0000000", "2024-03-31 23:59:59.9999990", 1)
	print(invoices)
	if len(invoices) != 0:
		if not invoices == "":
			count = len(tb.rows)		
			tb.rows.clear()
			count = len(tb.rows)						
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

def start():
	utility = None
	db_connection_failed = False
	try:
		utility = DllUtility()
	except FileNotFoundError as e:
		print(e)
		db_connection_failed = True

	if not db_connection_failed:
		srv = utility.get_server_name()
		db = utility.get_database_name()
		user = utility.get_user_name()
		calldb()

dlg.visible = False
mytable = Column([
	dlg,
	Row([tb],scroll="always")
	])