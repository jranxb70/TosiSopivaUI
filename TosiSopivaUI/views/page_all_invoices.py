import flet as ft
from flet import *
from flet_route import Params, Basket
from views.app_bar import AppBar
# IMPORT YOU CREATE TABLE 
from db_invoices import mytable, tb, calldb, start, add_invoice
from views.page_invoice_line import page_invoice_line
#import sqlite3
#conn = sqlite3.connect("invoice.db",check_same_thread=False)


def page_all_invoices(page: ft.Page, params: Params, basket: Basket):
    
    # AND RUN SCRIPT FOR CREATE TABLE WHEN FLET FIRST RUN
	#create_table()
	start()	

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
			# c = conn.cursor()
			# c.execute("INSERT INTO invoice (customer_id, invoice_date, invoice_bankreference, invoice_subtotal, invoice_tax, invoice_total, invoice_due_date) VALUES(?,?,?,?,?,?,?)",
   #           (customer_id.value, date.value, bank_reference.value, subtotal.value, tax.value, total.value, due_date.value))
			# conn.commit()
			invoice_lines = [{"product_item_id": 1, "quantity":10, "price":8, "product_description": "turha tuote"}]
			try:			
				add_invoice(int(customer_id.value), date.value, float(subtotal.value), float(total.value), float(tax.value), bank_reference.value, due_date.value, invoice_lines)
			except ValueError as e:
				print(e)							

			# AND SLIDE RIGHT AGAIN IF FINAL INPUT SUUCESS
			inputcon.offset = transform.Offset(2,0)

			# ADD SNACKBAR IF SUCCESS INPUT TO DATABASE
			page.snack_bar = SnackBar(
				Text("Saved"),
				)
			page.snack_bar.open = True
   
			customer_id.value = ''
			date.value = ''
			bank_reference.value = ''
			subtotal.value = ''
			tax.value = ''
			total.value = ''
			due_date.value = ''

			# REFRESH TABLE
			tb.rows.clear()
			calldb()
			tb.update()
			page.update()


		except Exception as e:
			print(e)

    # keeps track of the number of tiles already added
	page.count = 0			

	# CREATE FIELD FOR INPUT
	customer_id = TextField(label="customer id")
	date = TextField(label="invoice date")
	bank_reference = TextField(label="bank reference")
	subtotal = TextField(label="invoice subtotal")
	tax = TextField(label="invoice tax")
	total = TextField(label="invoice total")
	due_date = TextField(label="due date")

	ff = ft.ListTile(title=ft.Text(f"Tile {page.count}"))

	tolppa = 0

	
	lines = ft.Container(
				content=ft.Column(
					[
						ft.ListTile(
							leading=ft.Icon(ft.icons.ALBUM),
							title=ft.Text("The Enchanted Nightingale"),
							subtitle=ft.Text(
								f"Music by Julie Gayboy {page.count}. Lyrics by Sidney Stein."
							),
						),
						ft.Row(
							[ft.TextButton("Buy tickets"), ft.TextButton("Listen")],
							alignment=ft.MainAxisAlignment.END,
						),
					]
				),
				width=400,
				padding=10,
			)

	def fab_pressed(e):
		content = lines.content
		controls = content.controls
		controls.append(ft.Text(f"Tile was added unsuccessfully! {e.page.count}"))		
		lines.update()				
		for fuch in controls:
			pass#fuch.off()		
		#lines.content(ft.Text(f"Tile was added successfully! {e.page.count}"))#ft.ListTile(title=ft.Text(f"Tile {page.count}")))
		#invoice_line = page_invoice_line(page, params, basket)#page: ft.Page, params: Params, basket: Basket)
		#page.add(invoice_line)	
		e.page.show_snack_bar(
            ft.SnackBar(ft.Text(f"Tile was added successfully! {e.page.count}"), open=True)
        )
		e.page.count += 1
		#tolppa += 1


	page.add(ft.Text("Press the FAB to add a tile!"))

	floating_action_button = ft.FloatingActionButton(
		icon=ft.icons.ADD, on_click=fab_pressed, bgcolor=ft.colors.LIME_300
)


	# CREATE MODAL INPUT FOR ADD NEW DATA 
	# new invoice	
	inputcon = Card(
		# ADD SLIDE LEFT EFFECT
		offset = transform.Offset(2,0),
		animate_offset = animation.Animation(600,curve="easeIn"),
		elevation=30,
		content=Container(
			content=Column([
				Row([
				Text("Add new invoice",size=20,weight="bold"),
				IconButton(icon="close",icon_size=30,
				on_click=hidecon
					),
					]),
				customer_id,
				date,
				bank_reference,
				subtotal,
                tax,
                total,
                due_date,
				floating_action_button,
				lines,							
				FilledButton("Save",
				on_click=savedata
					)
			])
		)
	)


	card = ft.Card(
			content=ft.Container(
				content=ft.Column(
					[
						ft.ListTile(
							leading=ft.Icon(ft.icons.ALBUM),
							title=ft.Text("The Enchanted Nightingale"),
							subtitle=ft.Text(
								"Music by Julie Gable. Lyrics by Sidney Stein."
							),
						),
						ft.Row(
							[ft.TextButton("Buy tickets"), ft.TextButton("Listen")],
							alignment=ft.MainAxisAlignment.END,
						),
					]
				),
				width=400,
				padding=10,
			)
		)
	#page.add(card)




	return ft.View(
    	"/page_all_invoices",
     	scroll = "always",
        
       	controls=[
        	AppBar().build(),
            Text("INVOICES",size=30,weight="bold"),
			ElevatedButton("add new invoice", on_click=showInput),
   			ElevatedButton(text='Go to Back', on_click=lambda _:page.go('/page_cabinet')),
		mytable,
		# AND DIALOG FOR ADD DATA
		inputcon, card
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )