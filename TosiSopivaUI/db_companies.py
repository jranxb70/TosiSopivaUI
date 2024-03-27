from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

tb = DataTable(
	columns=[
		DataColumn(Text("Name")),
		DataColumn(Text("Address")),
		DataColumn(Text("Postal code")),
    	DataColumn(Text("City")),
    	DataColumn(Text("Phone")),
    	DataColumn(Text("Business_id")),
    	DataColumn(Text("Actions")),
	],
	rows=[]
	)

def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM company WHERE id=?", (myid,))
		conn.commit()
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)

id_edit = Text()
name_edit = TextField(label="name")
address_edit = TextField(label="address")
zip_edit = TextField(label="postal code", input_filter=InputFilter(
            allow=True,
            regex_string=r"[0-9]",
            replacement_string="",
        ))
city_edit = TextField(label="city")
phone_edit = TextField(label="phone", input_filter=InputFilter(
            allow=True,
            regex_string=r"[0-9+]",
            replacement_string="",
        ))
business_id_edit = TextField(label="business id", input_filter=InputFilter(
            allow=True,
            regex_string=r"[0-9]",
            replacement_string="",
        ))

def hidedlg(e):
	dlg.visible = False
	dlg.update()

def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE company SET name=?, address=?, zip=?, city=?, phone=?, business_id=? WHERE id=?", (name_edit.value, address_edit.value, zip_edit.value, city_edit.value, phone_edit.value, business_id_edit.value,  myid))
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
				address_edit,
				zip_edit,
                city_edit,
                phone_edit,
                business_id_edit,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	name_edit.value = data_edit['name']
	address_edit.value = data_edit['address']
	zip_edit.value = data_edit['zip']
	city_edit.value = data_edit['city']
	phone_edit.value = data_edit['phone']
	business_id_edit.value = data_edit['business_id']

	dlg.visible = True
	dlg.update()
 
def create_table():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS company(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT,
		address TEXT,
		zip INTEGER,
		city TEXT,
		phone TEXT,
        business_id INTEGER)
		""")
	conn.commit()

def calldb():
	create_table()
	c = conn.cursor()
	c.execute("SELECT * FROM company")
	companies = c.fetchall()
	if not companies == "":
		keys = ['id', 'name', 'address', 'zip', 'city', 'phone', 'business_id']
		result = [dict(zip(keys, values)) for values in companies]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Text(x['name'])),
                        DataCell(Text(x['address'])),
                        DataCell(Text(x['zip'])),
                        DataCell(Text(x['city'])),
                        DataCell(Text(x['phone'])),
                        DataCell(Text(x['business_id'])),
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