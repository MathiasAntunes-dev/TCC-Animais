import sqlite3

DATABASE = "data/pet.sqlite3"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn