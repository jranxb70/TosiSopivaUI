import flet as ft
from flet import *
from flet_route import Params, Basket

# IMPORT YOU CREATE TABLE 
from db_products import mytable, tb, calldb
from db_create_all_tables import create_table_products
import sqlite3
conn = sqlite3.connect("invoice.db",check_same_thread=False)

def page_all_products(page: ft.Page, params: Params, basket: Basket):
    
    # AND RUN SCRIPT FOR CREATE TABLE WHEN FLET FIRST RUN
	create_table_products()

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
			c.execute("INSERT INTO products (name,quantity,price) VALUES(?,?,?)",(name.value,quantity.value,price.value))
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
	quantity = TextField(label="quantity")
	price = TextField(label="price")

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
				quantity,
				price,
				FilledButton("save data",
				on_click=savedata
					)
			])
		)
	)

	return ft.View(
    	"/page_all_products",
        
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