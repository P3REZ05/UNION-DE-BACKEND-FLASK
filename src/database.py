import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="perez",
    password="",
    database="mercaflask",
    port="3306"

)

def get_db_cursor():
    return db.cursor(dictionary=True)





