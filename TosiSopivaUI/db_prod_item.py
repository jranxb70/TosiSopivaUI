from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

tb = DataTable(
	columns=[
		DataColumn(Text("Product ID")),
		DataColumn(Text("SKU")),
		DataColumn(Text("In stock")),
		DataColumn(Text("Product image")),
		DataColumn(Text("Price")),
    	DataColumn(Text("Actions")),
	],
	rows=[]
	)

def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM product_item WHERE id=?", (myid,))
		conn.commit()
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)

id_edit = Text()
product_id_edit = TextField(label="product id")
sku_edit = TextField(label="sku")
qty_in_stock_edit = TextField(label="quantity")
product_image_edit = TextField(label="image")
price_edit = TextField(label="price")

def hidedlg(e):
	dlg.visible = False
	dlg.update()

def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE product_item SET product_id=?, sku=?, qty_in_stock=?, product_image=?, price=? WHERE id=?", (product_id_edit.value, sku_edit.value, qty_in_stock_edit.value, product_image_edit.value, price_edit.value, myid))
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
				product_id_edit,
				sku_edit,
				qty_in_stock_edit,
				product_image_edit,
				price_edit,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	product_id_edit.value = data_edit['product_id']
	sku_edit.value = data_edit['sku']
	qty_in_stock_edit.value = data_edit['qty_in_stock']
	product_image_edit.value = data_edit['product_image']
	price_edit.value = data_edit['price']

	dlg.visible = True
	dlg.update()
 
def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS product_item(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		product_id INTEGER,
		sku TEXT,
		qty_in_stock INTEGER,
        product_image TEXT,
        price TEXT)
		""")
	conn.commit()

def calldb():
	create_table()
	c = conn.cursor()
	c.execute("SELECT * FROM product_item")
	products = c.fetchall()
	if not products == "":
		keys = ['id', 'product_id', 'sku', 'qty_in_stock', 'product_image', 'price']
		result = [dict(zip(keys, values)) for values in products]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(x['product_id'])),
                        DataCell(Text(x['sku'])),
                        DataCell(Text(x['qty_in_stock'])),
                        DataCell(Text(x['product_image'])),
                        DataCell(Text(x['price'])),
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