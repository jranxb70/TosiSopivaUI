from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

tb = DataTable(
	columns=[
		DataColumn(Text("name")),
		DataColumn(Text("quantity")),
		DataColumn(Text("price")),
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
name_edit = TextField(label="name")
quantity_edit = TextField(label="quantity", input_filter=InputFilter(
            allow=True,
            regex_string=r"[0-9]",
            replacement_string="",
        ))
price_edit = TextField(label="price", input_filter=InputFilter(
            allow=True,
            regex_string=r"[0-9,.]",
            replacement_string="",
        ))

def hidedlg(e):
	dlg.visible = False
	dlg.update()

def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE product SET name=?, quantity=?, price=? WHERE id=?", (name_edit.value, quantity_edit.value, price_edit.value, myid))
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
				name_edit,
				quantity_edit,
				price_edit,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	name_edit.value = data_edit['name']
	quantity_edit.value = data_edit['quantity']
	price_edit.value = data_edit['price']

	dlg.visible = True
	dlg.update()
 
def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS product(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT,
		quantity INTEGER,
		price INTEGER)
		""")
	conn.commit()

def calldb():
	create_table()
	c = conn.cursor()
	c.execute("SELECT * FROM product")
	products = c.fetchall()
	if not products == "":
		keys = ['id', 'name', 'quantity', 'price']
		result = [dict(zip(keys, values)) for values in products]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(x['name'])),
                        DataCell(Text(x['quantity'])),
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