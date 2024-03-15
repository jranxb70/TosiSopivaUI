from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

tb = DataTable(
	columns=[
     	DataColumn(Text("actions")),
		DataColumn(Text("name")),
		DataColumn(Text("surname")),
		DataColumn(Text("address")),
		DataColumn(Text("zip")),
		DataColumn(Text("city")),
	],
	rows=[]
	)

def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM clients WHERE id=?", (myid,))
		conn.commit()
		print("success delete")
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)

id_edit = Text()
name_edit = TextField(label="name")
surname_edit = TextField(label="surname")
address_edit = TextField(label="address")
zip_edit = TextField(label="zip")
city_edit = TextField(label="city")

def hidedlg(e):
	dlg.visible = False
	dlg.update()


def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE clients SET name=?, surname=?, address=?, zip=?, city=? WHERE id=?", (name_edit.value, surname_edit.value, address_edit.value, zip_edit.value, city_edit.value, myid))
		conn.commit()
		print("success Edit ")
		tb.rows.clear()	
		calldb()
		dlg.visible = False
		dlg.update()
		tb.update()
	except Exception as e:
		print(e)

dlg = Container(
	bgcolor="blue200",
	padding=10,
			content=Column([
				Row([
				Text("Edit Form",size=30,weight="bold"),
				IconButton(icon="close",on_click=hidedlg),
					],alignment="spaceBetween"),
				name_edit,
				surname_edit,
				address_edit,
				zip_edit,
				city_edit,
				ElevatedButton("Update",on_click=updateandsave)

				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	name_edit.value = data_edit['name']
	surname_edit.value = data_edit['surname']
	address_edit.value = data_edit['address']
	zip_edit.value = data_edit['zip']
	city_edit.value = data_edit['city']


	dlg.visible = True
	dlg.update()
 
def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS clients(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT,
		surname TEXT,
		address INTEGER,
		zip TEXT,
		city TEXT)
		""")
	conn.commit()


def calldb():
	create_table()
	c = conn.cursor()
	c.execute("SELECT * FROM clients")
	clients = c.fetchall()
	print(clients)
	if not clients == "":
		keys = ['id', 'name', 'surname', 'address', 'zip', 'city']
		result = [dict(zip(keys, values)) for values in clients]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Row([
                        	IconButton(icon="create",icon_color="blue",
                        		data=x,
                        		on_click=showedit

                        		),
                        	IconButton(icon="delete",icon_color="red",
                        		data=x['id'],
                        	on_click=showdelete

                        		),
                        	])),
                        DataCell(Text(x['name'])),
                        DataCell(Text(x['surname'])),
                        DataCell(Text(x['address'])),
                        DataCell(Text(x['zip'])),
                        DataCell(Text(x['city'])),
                    ],
                ),

		)


calldb()

dlg.visible = False
mytable = Column([
	dlg,
	Row([tb],scroll="always")
	])