from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

tb = DataTable(
	columns=[
		DataColumn(Text("Value")),
		DataColumn(Text("Variation ID")),
    	DataColumn(Text("Actions")),
	],
	rows=[]
	)

def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM variation_option WHERE id=?", (myid,))
		conn.commit()
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)

id_edit = Text()
variation_value_edit = TextField(label="variation value")
variation_id_edit = TextField(label="variation_id ")

def hidedlg(e):
	dlg.visible = False
	dlg.update()

def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE variation_option SET variation_value=?, variation_id=? WHERE id=?", (variation_value_edit.value, variation_id_edit.value, myid))
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
				variation_value_edit,
				variation_id_edit,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	variation_value_edit.value = data_edit['variation_value']
	variation_id_edit.value = data_edit['variation_id']

	dlg.visible = True
	dlg.update()
 
def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS variation_option(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		variation_value TEXT,
		variation_id INTEGER)
		""")
	conn.commit()

def calldb():
	create_table()
	c = conn.cursor()
	c.execute("SELECT * FROM variation_option")
	products = c.fetchall()
	if not products == "":
		keys = ['id', 'variation_value', 'variation_id']
		result = [dict(zip(keys, values)) for values in products]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(x['variation_value'])),
                        DataCell(Text(x['variation_id'])),
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