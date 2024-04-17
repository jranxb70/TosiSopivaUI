from flet import *
from DBEngineWrapper import DBEngineWrapper
from DllUtility import DllUtility

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
	id_edit.value = data_edit['company_id']
	name_edit.value = data_edit['company_name']
	address_edit.value = data_edit['company_address']
	zip_edit.value = data_edit['company_zip']
	city_edit.value = data_edit['company_city']
	phone_edit.value = data_edit['company_phone']
	business_id_edit.value = data_edit['company_business_id']

	dlg.visible = True
	dlg.update()
 
def calldb():
	db_engine = DBEngineWrapper()
	company = db_engine.get_company(1)

	if not len(company) == 0:
		result = dict(company)

		tb.rows.append(
			DataRow(
                cells=[
                    DataCell(Text(result['company_name'])),
                    DataCell(Text(result['company_address'])),
                    DataCell(Text(result['company_zip'])),
                    DataCell(Text(result['company_city'])),
                    DataCell(Text(result['company_phone'])),
                    DataCell(Text(result['company_business_id'])),
                    DataCell(Row([
                        IconButton(icon="EDIT",icon_color="blue",
                        	data=result,
                        	on_click=showedit
                        ),
                        IconButton(icon="delete",icon_color="red",
                        	data=result['company_id'],
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