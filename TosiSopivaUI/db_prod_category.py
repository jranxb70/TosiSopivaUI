from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

tb = DataTable(
	columns=[
		DataColumn(Text("Parent category id")),
		DataColumn(Text("Name")),
    	DataColumn(Text("Actions")),
	],
	rows=[]
	)

def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM product_category WHERE id=?", (myid,))
		conn.commit()
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)

id_edit = Text()
parent_category_id = TextField(label="parent category id")
name_edit = TextField(label="name")

def hidedlg(e):
	dlg.visible = False
	dlg.update()

def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE product_category SET parent_category_id=?, name=? WHERE id=?", (parent_category_id.value, name_edit.value, myid))
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
				parent_category_id,
				name_edit,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	parent_category_id.value = data_edit['parent_category_id']
	name_edit.value = data_edit['name']

	dlg.visible = True
	dlg.update()
 
def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS product_category(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		parent_category_id INTEGER,
		name TEXT)
		""")
	conn.commit()

def calldb():
	create_table()
	c = conn.cursor()
	c.execute("SELECT * FROM product_category")
	products = c.fetchall()
	if not products == "":
		keys = ['id', 'parent_category_id','name']
		result = [dict(zip(keys, values)) for values in products]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(x['parent_category_id'])),
                        DataCell(Text(x['name'])),
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