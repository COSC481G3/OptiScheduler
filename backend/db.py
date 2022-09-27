import mysql.connector
import os
import time

# Loop to wait for mysql server, there's probably a better way of doing this
def init_db():
    try:
        mysqldb = mysql.connector.connect(
            host="opti_db",
            user="user",
            # env declared in docker-compose
            password=os.getenv('MYSQL_PASSWORD'),
            database="db"
        )
    except (mysql.connector.errors.InterfaceError, mysql.connector.errors.DatabaseError):
        time.sleep(5)
        mysqldb = init_db()
    
    return mysqldb

# Init db
db = init_db()

# Insert name, place into db
def db_insert(name, place):
    cursor = db.cursor()
    cursor.execute("CREATE TABLE if not exists customers (name VARCHAR(255), address VARCHAR(255))")
    cursor.execute("INSERT INTO customers (name, address) VALUES (%s, %s)", (name, place))
    db.commit()
    cursor.close()

# Retrieve all db items
def db_retrieve():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers")
    result = cursor.fetchall()
    cursor.close()

    return result