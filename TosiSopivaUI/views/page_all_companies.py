import flet as ft
from flet import *
from flet_route import Params, Basket
from views.app_bar import AppBar
# IMPORT YOU CREATE TABLE 
from db_companies import mytable, tb, calldb
import sqlite3
conn = sqlite3.connect("invoice.db",check_same_thread=False)

def page_all_companies(page: ft.Page, params: Params, basket: Basket):

	page.scroll = "auto"

	def showInput(e):
		inputcon.offset = transform.Offset(0,0)
		page.update()

	def hidecon(e):
		inputcon.offset = transform.Offset(2,0)
		page.update()

	def savedata(e):
		try:
			# INPUT TO DATABASE
			c = conn.cursor()
			c.execute("INSERT INTO company(name, address, zip, city, phone, business_id) VALUES(?,?,?,?,?,?)",(name.value, address.value, zip.value, city.value, phone.value, business_id.value))
			conn.commit()

			# AND SLIDE RIGHT AGAIN IF FINAL INPUT SUUCESS
			inputcon.offset = transform.Offset(2,0)

			# ADD SNACKBAR IF SUCCESS INPUT TO DATABASE
			page.snack_bar = SnackBar(
				Text("Saved"),)
			page.snack_bar.open = True

			name.value =''
			address.value =''
			zip.value =''
			city.value =''
			phone.value =''
			business_id.value =''
   
			# REFRESH TABLE
			tb.rows.clear()
			calldb()
			tb.update()
			page.update()

		except Exception as e:
			print(e)

	# CREATE FIELD FOR INPUT
	name = TextField(label="name")
	address = TextField(label="address")
	zip = TextField(label="zip", input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"[0-9]",
            replacement_string="",
    ))
	city = TextField(label="city")
	phone = TextField(label="phone", input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"[0-9+]",
            replacement_string="",
    ))
	business_id = TextField(label="business_id", input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"[0-9]",
            replacement_string="",
    ))

	# CREATE MODAL INPUT FOR ADD NEW DATA 
	inputcon = Card(
		# ADD SLIDE LEFT EFFECT
		offset = transform.Offset(2,0),
		animate_offset = animation.Animation(600,curve="easeIn"),
		elevation=30,
		content=Container(
			content=Column([
				Row([
				Text("Add new company",size=20,weight="bold"),
				IconButton(icon="close",icon_size=30,
				on_click=hidecon
					),
					]),
				name,
				address,
				zip,
                city,
				phone,
				business_id,
				FilledButton("Save",
				on_click=savedata)
			])
		)
	)

	return ft.View(
    	"/page_all_companies",
     	scroll = "always",
        
       	controls=[
            AppBar().build(),
            Text("COMPANIES",size=30,weight="bold"),
			ElevatedButton("add new company", on_click=showInput),
   			ElevatedButton(text='Go to Back', on_click=lambda _:page.go('/page_cabinet')),
		mytable,
		# AND DIALOG FOR ADD DATA
		inputcon 
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )