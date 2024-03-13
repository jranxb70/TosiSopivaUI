from flet import *
import sqlite3
conn = sqlite3.connect('invoice.db',check_same_thread=False)

def create_table_clients():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS clients(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT,
		surname TEXT,
		address INTEGER,
		zip TEXT,
		city TEXT)
		""")
	conn.commit()

def create_table_products():
	c = conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS products(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT,
		quantity INTEGER,
		price INTEGER)
		""")
	conn.commit()