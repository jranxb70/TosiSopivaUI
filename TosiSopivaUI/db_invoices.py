from flet import *
import sqlite3
from Bill import get_invoice

conn = sqlite3.connect('invoice.db',check_same_thread=False)

def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS invoice(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
		invoice_date DATE,
		invoice_subtotal REAL,
		invoice_total REAL,
		invoice_tax REAL,
		bank_reference TEXT,
        invoice_lines TEXT)
		""")
	conn.commit()

tb = DataTable(
	columns=[
     	DataColumn(Text("id")),
		DataColumn(Text("Client")),
		DataColumn(Text("Date")),
		DataColumn(Text("Subtotal")),
		DataColumn(Text("Total")),
		DataColumn(Text("Tax")),
		DataColumn(Text("Bank reference")),
		DataColumn(Text("invoice_lines")),
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
client_id = TextField(label="client_id")
invoice_date = TextField(label="invoice_date")
invoice_subtotal = TextField(label="invoice_subtotal")
invoice_total = TextField(label="invoice_total")
invoice_tax = TextField(label="invoice_tax") 
bank_reference = TextField(label="bank_reference") 
invoice_lines = TextField(label="invoice_lines") 

def hidedlg(e):
	dlg.visible = False
	dlg.update()

def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE invoice SET client_id=?, invoice_date=?, invoice_subtotal=?, invoice_total=?, invoice_tax=?, bank_reference=?, invoice_lines=? WHERE id=?",
            (client_id.value,invoice_date.value,invoice_subtotal.value, invoice_total.value, invoice_tax.value, bank_reference.value, invoice_lines.value, myid))
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
				client_id,
				invoice_date,
				invoice_subtotal,
				invoice_total,
				invoice_tax,
                bank_reference,
                invoice_lines,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	client_id.value = data_edit['client_id']
	invoice_date.value = data_edit['invoice_date']
	invoice_subtotal.value = data_edit['invoice_subtotal']
	invoice_total.value = data_edit['invoice_total']
	invoice_tax.value = data_edit['invoice_tax']
	bank_reference.value = data_edit['bank_reference']
	invoice_lines.value = data_edit['invoice_lines']

	dlg.visible = True
	dlg.update()
 
bill = DataTable(
	columns=[
     	DataColumn(Text("id")),
		DataColumn(Text("Client")),
		DataColumn(Text("Date")),
		DataColumn(Text("Subtotal")),
		DataColumn(Text("Total")),
		DataColumn(Text("Tax")),
		DataColumn(Text("Bank reference")),
		DataColumn(Text("invoice_lines")),
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
		keys = ['id', 'client_id', 'invoice_date', 'invoice_subtotal', 'invoice_total', 'invoice_tax', 'bank_reference', 'invoice_lines']
		result = [dict(zip(keys, values)) for values in invoices]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(x['id'])),
                        DataCell(Text(x['client_id'])),
                        DataCell(Text(x['invoice_date'])),
                        DataCell(Text(x['invoice_subtotal'])),
                        DataCell(Text(x['invoice_total'])),
                        DataCell(Text(x['invoice_tax'])),
                        DataCell(Text(x['bank_reference'])),
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