import flet as ft
from flet import *
from flet_route import Params, Basket
from views.app_bar import AppBar
# IMPORT YOU CREATE TABLE 
from db_invoices import create_table, mytable, tb, calldb
import sqlite3
conn = sqlite3.connect("invoice.db",check_same_thread=False)

def page_all_invoices(page: ft.Page, params: Params, basket: Basket):
    
    # AND RUN SCRIPT FOR CREATE TABLE WHEN FLET FIRST RUN
	create_table()

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
			c.execute("INSERT INTO invoices (client_id,invoice_date, invoice_subtotal, invoice_total, invoice_tax, bank_reference, invoice_lines) VALUES(?,?,?,?,?,?,?)",
             (client_id.value,invoice_date.value,invoice_subtotal.value, invoice_total.value, invoice_tax.value, bank_reference.value, invoice_lines.value))
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

	client_id = TextField(label="client_id")
	invoice_date = TextField(label="invoice_date")
	invoice_subtotal = TextField(label="invoice_subtotal")
	invoice_total = TextField(label="invoice_total")
	invoice_tax = TextField(label="invoice_tax")
	bank_reference = TextField(label="bank_reference")
	invoice_lines = TextField(label="invoice_lines")

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
				client_id,
				invoice_date,
				invoice_subtotal,
                invoice_total,
                invoice_tax,
                bank_reference,
                invoice_lines,
				FilledButton("save data",
				on_click=savedata
					)
			])
		)
	)

	return ft.View(
    	"/page_all_invoices",
        
       	controls=[
             AppBar().build(),
            Text("INVOICES",size=30,weight="bold"),
			ElevatedButton("add new invoice", on_click=showInput),
   			ElevatedButton(text='Go to Back', on_click=lambda _:page.go('/temp_nav')),
		mytable,
		# AND DIALOG FOR ADD DATA
		inputcon 
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )