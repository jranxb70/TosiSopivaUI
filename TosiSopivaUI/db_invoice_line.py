from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

tb = DataTable(
	columns=[
		DataColumn(Text("Invoice id")),
		DataColumn(Text("Product id")),
		DataColumn(Text("Quantity")),
		DataColumn(Text("Price")),
		DataColumn(Text("Description")),
    	DataColumn(Text("Actions")),
	],
	rows=[]
	)

def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM invoice_line WHERE id=?", (myid,))
		conn.commit()
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)

id_edit = Text()
invoice_id_edit = TextField(label="invoice id")
product_id_edit = TextField(label="product id")
quantity_edit = TextField(label="quantity")
price_edit = TextField(label="price")
product_description_edit = TextField(label="product_description")

def hidedlg(e):
	dlg.visible = False
	dlg.update()

def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE invoice_line SET invoice_id=?, product_id=?, quantity=?, price=?, product_description=?  WHERE id=?", (invoice_id_edit.value, product_id_edit.value,quantity_edit.value,price_edit.value,product_description_edit.value,  myid))
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
				invoice_id_edit,
				product_id_edit,
				quantity_edit,
				price_edit,
				product_description_edit,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	invoice_id_edit.value = data_edit['invoice_id']
	product_id_edit.value = data_edit['product_id']
	quantity_edit.value = data_edit['quantity']
	price_edit.value = data_edit['price']
	product_description_edit.value = data_edit['product_description']

	dlg.visible = True
	dlg.update()
 
def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS invoice_line(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		invoice_id INTEGER,
		product_id INTEGER,
		quantity INTEGER,
		price REAL,
		product_description TEXT)
		""")
	conn.commit()

def calldb():
	create_table()
	c = conn.cursor()
	c.execute("SELECT * FROM invoice_line")
	products = c.fetchall()
	if not products == "":
		keys = ['id', 'invoice_id','product_id', 'quantity', 'price', 'product_description']
		result = [dict(zip(keys, values)) for values in products]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(x['invoice_id'])),
                        DataCell(Text(x['product_id'])),
                        DataCell(Text(x['quantity'])),
                        DataCell(Text(x['price'])),
                        DataCell(Text(x['product_description'])),
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