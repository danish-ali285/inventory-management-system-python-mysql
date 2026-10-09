import mysql.connector as mydatabase

def get_connection():
    database = mydatabase.connect(
        host = "localhost",
        username = "root",
        password = "ALI@321as#.",
        database = "inventory_system"
    )
    return database
