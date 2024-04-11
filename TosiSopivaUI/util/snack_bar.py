from flet import *

def show_snack_bar(page: Page, text):
	page.snack_bar = SnackBar(Text(text))
	page.snack_bar.open = True
	page.update()