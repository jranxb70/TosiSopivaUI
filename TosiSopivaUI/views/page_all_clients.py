import flet as ft
from flet import *
from flet_route import Params, Basket

# IMPORT YOU CREATE TABLE 
from db_clients import mytable, tb, calldb
from db_create_all_tables import create_table_clients
import sqlite3
conn = sqlite3.connect("invoice.db",check_same_thread=False)

def page_all_clients(page: ft.Page, params: Params, basket: Basket):
    
    # AND RUN SCRIPT FOR CREATE TABLE WHEN FLET FIRST RUN
	create_table_clients()

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
			c.execute("INSERT INTO clients (name,surname,address,zip,city) VALUES(?,?,?,?,?)",(name.value,surname.value,address.value,zip.value,city.value))
			conn.commit()
			print("success")

			# AND SLIDE RIGHT AGAIN IF FINAL INPUT SUUCESS
			inputcon.offset = transform.Offset(2,0)

			# ADD SNACKBAR IF SUCCESS INPUT TO DATABASE

			page.snack_bar = SnackBar(
				Text("success INPUT"),
				bgcolor="green"
				)

			page.snack_bar.open = True

			# REFRESH TABLE
			tb.rows.clear()
			calldb()
			tb.update()
			page.update()


		except Exception as e:
			print(e)

	# CREATE FIELD FOR INPUT

	name = TextField(label="name")
	surname = TextField(label="surname")
	address = TextField(label="address")
	zip = TextField(label="zip")
	city = TextField(label="city")

	# CREATE MODAL INPUT FOR ADD NEW DATA 
	inputcon = Card(
		# ADD SLIDE LEFT EFFECT
		offset = transform.Offset(2,0),
		animate_offset = animation.Animation(600,curve="easeIn"),
		elevation=30,
		content=Container(
			content=Column([
				Row([
				Text("Add new data",size=20,weight="bold"),
				IconButton(icon="close",icon_size=30,
				on_click=hidecon
					),
					]),
				name,
				surname,
				address,
				zip,
				city,
				FilledButton("save data",
				on_click=savedata
					)
			])
		)
	)

	return ft.View(
    	"/page_all_clients",
        
       	controls=[
            Text("CLIENTS",size=30,weight="bold"),
			ElevatedButton("add new data", on_click=showInput),
   			ElevatedButton(text='Go to Back', on_click=lambda _:page.go('/temp_nav')),
		mytable,
		# AND DIALOG FOR ADD DATA
		inputcon 
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )