import flet as ft
from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

from DBEngineWrapper import DBEngineWrapper
engine = DBEngineWrapper()

tb = DataTable(
	columns=[Column(scroll="always"),
		DataColumn(Text("ID")),
		DataColumn(Text("First name")),
		DataColumn(Text("Last name")),
		DataColumn(Text("Address")),
		DataColumn(Text("Postal code")),
		DataColumn(Text("City")),
		DataColumn(Text("Phone")),
		DataColumn(Text("Email")),
    	DataColumn(Text("Actions")),
	],
	rows=[]
	)

def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM customer WHERE id=?", (myid,))
		conn.commit()
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)

id_edit = Text()
firstname_edit = TextField(label="firstname")
lastname_edit = TextField(label="lastname")
address_edit = TextField(label="address")
zip_edit = TextField(label="zip",input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"[0-9]",
            replacement_string="",
        ))
city_edit = TextField(label="city")
phone_edit = TextField(label="phone", input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"[0-9+]",
            replacement_string="",
        ))
email_edit = TextField(label="email")

def hidedlg(e):
	dlg.visible = False
	dlg.update()
 
def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE customer SET firstname=?, lastname=?, address=?, zip=?, city=?, phone=?, email=? WHERE id=?", (firstname_edit.value, lastname_edit.value, address_edit.value, zip_edit.value, city_edit.value,  phone_edit.value, email_edit.value, myid))
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
	top = 10,
			content=Column([
				Row([
				Text("Edit Form",size=30,weight="bold"),
				IconButton(icon="close",on_click=hidedlg),
					],alignment="spaceBetween"),
				firstname_edit,
				lastname_edit,
				address_edit,
				zip_edit,
				city_edit,
				phone_edit,
				email_edit,
				ElevatedButton("Update",on_click=updateandsave)
				])
)

def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['customer_id']
	firstname_edit.value = data_edit['firstname']
	lastname_edit.value = data_edit['lastname']
	address_edit.value = data_edit['address']
	zip_edit.value = data_edit['zip']
	city_edit.value = data_edit['city']
	phone_edit.value = data_edit['phone']
	email_edit.value = data_edit['email']

	dlg.visible = True
	dlg.update()
 
# def create_table():
# 	c = conn.cursor()
# 	c.execute("""CREATE TABLE IF NOT EXISTS customer(
# 		id INTEGER PRIMARY KEY AUTOINCREMENT,
# 		firstname  TEXT,
# 		lastname	TEXT,
# 		address	TEXT,
# 		zip        INTEGER,
# 		city       TEXT,
#   		phone      TEXT,
#     	email     TEXT)
# 		""")
# 	conn.commit()

def calldb():
	# create_table()
	# c = conn.cursor()
	# c.execute("SELECT * FROM customer")
	# clients = c.fetchall()
	# clients = engine.getCustomer(1)
	clients = engine.queryCustomers()
	# print(clients)
	# print(clients['customers'][1]['first_name'])
	# print(clients['customer_id'])
	if not clients == "":
		# for customer in clients['customers']:
		# 	print("Customer ID:", customer['customer_id'])
		# 	print("Name:", customer['first_name'], customer['last_name'])
		# 	print("Address:", customer['address'])
		# 	print("City:", customer['city'])
		# 	print("Zip Code:", customer['zip'])
		# 	print("Phone:", customer['phone'])
		# 	print("Email:", customer['email'])
		# 	print()
		# keys = ['id', 'firstname', 'lastname', 'address', 'zip', 'city', 'phone', 'email']
		# result = [dict(zip(keys, values)) for values in clients]
		for customer in clients['customers']:
			tb.rows.append(
				DataRow(cells=[        
                  DataCell(Text(customer['customer_id'])),
                  DataCell(Text(customer['first_name'])),
                  DataCell(Text(customer['last_name'])),
                  DataCell(Text(customer['address'])),
                  DataCell(Text(customer['city'])),
                  DataCell(Text(customer['zip'])),
                  DataCell(Text(customer['phone'])),
                  DataCell(Text(customer['email'])),
                  DataCell(Row([
                    IconButton(icon="EDIT",icon_color="blue",
                         		data=customer['customer_id'],
                        		on_click=showedit
                 		),
                   	IconButton(icon="delete",icon_color="red",
                       		data=customer['customer_id'],
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