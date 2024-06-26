import flet as ft
from flet import *
from util.snack_bar import show_snack_bar

from DBEngineWrapper import DBEngineWrapper
from DllUtility import DllUtility
engine = DBEngineWrapper()

tb = DataTable(
	columns=[
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
		engine.deleteCustomer(myid)
		tb.rows.clear()	
		calldb()
		tb.update()
		show_snack_bar(e.page, 'Deleted!')
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
            regex_string=r"[0-9+\-]",
            replacement_string="",
        ))
email_edit = TextField(label="email")

def hidedlg(e):
	dlg.visible = False
	dlg.update()
 
def updateandsave(e):
	try:
		myid = id_edit.value	
		engine.updateCustomer(myid, firstname_edit.value, lastname_edit.value, address_edit.value, zip_edit.value, city_edit.value, phone_edit.value, email_edit.value)
		tb.rows.clear()	
		calldb()
		dlg.visible = False
		dlg.update()
		tb.update()
		show_snack_bar(e.page, 'Updated!')
	except Exception as e:
		print(e)

dlg = Container(
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
	firstname_edit.value = data_edit['first_name']
	lastname_edit.value = data_edit['last_name']
	address_edit.value = data_edit['address']
	zip_edit.value = data_edit['zip']
	city_edit.value = data_edit['city']
	phone_edit.value = data_edit['phone']
	email_edit.value = data_edit['email']

	dlg.visible = True
	dlg.update()

def calldb():
	clients = engine.queryCustomers()
	if not clients == "":	
		tb.rows.clear()
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
                         		data=customer,
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

def start():
	utility = None
	db_connection_failed = False
	try:
		utility = DllUtility()
	except FileNotFoundError as e:
		print(e)
		db_connection_failed = True

	if not db_connection_failed:
		srv = utility.get_server_name()
		db = utility.get_database_name()
		user = utility.get_user_name()
		calldb()

dlg.visible = False
mytable = Column([
	dlg,
	Row([tb],scroll="always")
	])