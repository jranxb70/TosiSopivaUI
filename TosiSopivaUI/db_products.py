from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

tb = DataTable(
	columns=[
		DataColumn(Text("Category")),
		DataColumn(Text("Name")),
		DataColumn(Text("Description")),
    	DataColumn(Text("actions")),
	],
	rows=[]
	)

def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM product WHERE id=?", (myid,))
		conn.commit()
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)

id_edit = Text()
category_id_edit = TextField(label="category id")
trade_name_edit = TextField(label="name")
product_description_edit = TextField(label="description")

def hidedlg(e):
	dlg.visible = False
	dlg.update()

def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE product SET category_id=?, trade_name=?, product_description=? WHERE id=?", (category_id_edit.value, trade_name_edit.value, product_description_edit.value, myid))
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
				category_id_edit,
				trade_name_edit,
				product_description_edit,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	category_id_edit.value = data_edit['category_id']
	trade_name_edit.value = data_edit['trade_name']
	product_description_edit.value = data_edit['product_description']

	dlg.visible = True
	dlg.update()
 
def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS product(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		category_id INTEGER,
		trade_name TEXT,
		product_description TEXT)
		""")
	conn.commit()

def calldb():
	create_table()
	c = conn.cursor()
	c.execute("SELECT * FROM product")
	products = c.fetchall()
	if not products == "":
		keys = ['id', 'category_id', 'trade_name', 'product_description']
		result = [dict(zip(keys, values)) for values in products]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(x['category_id'])),
                        DataCell(Text(x['trade_name'])),
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