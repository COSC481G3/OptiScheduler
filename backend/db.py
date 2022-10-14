import mysql.connector
import os
import time
import logging

log = logging.getLogger("OptiServe.db")

# Loop to wait for mysql server, there's probably a better way of doing this
def init_db():
    log.warning("Connecting to db...")
    try:
        mysqldb = mysql.connector.connect(
            host="opti_db",
            user="user",
            # env declared in docker-compose
            password=os.getenv('MYSQL_PASSWORD'),
            database="db"
        )
        log.warning("Connected!")
    except (mysql.connector.errors.InterfaceError, mysql.connector.errors.DatabaseError):
        time.sleep(5)
        mysqldb = init_db()
    
    return mysqldb

# Init db
db = init_db()

def create_db():
    cursor = db.cursor(buffered=True)
    cursor.execute("USE db")

    #Don't create if tables already exists
    cursor.execute("SHOW TABLES")
    for x in cursor:
        if str(x) == '(\'Store\',)':
            log.warning("DB Found, skipping creation")
            cursor.close()
            return

    log.warning("DB not found, creating...")
    #Create tables
    cursor.execute("CREATE TABLE Store(store_id INT NOT NULL, store_name varchar(99) NOT NULL, store_address varchar(99) NOT NULL, PRIMARY KEY(store_id))")
    cursor.execute("CREATE TABLE Holiday(store_id INT, start_date DATE, end_date DATE, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE Employee(Employee_id INT NOT NULL, store_id INT, first_name varchar(40) NOT NULL, last_name varchar(40) NOT NULL, PTO_Days_Rem INT, DOB DATE, PRIMARY KEY(Employee_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    #DOB References Date of Birth for employees. DATE type in mysql is written 'YYYY-MM-DD'
    cursor.execute("CREATE TABLE TimeOff(Employee_id INT, PTO BOOLEAN, start_date DATE, end_date DATE, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    #Time off table for workers. Careful with BOOLEAN type its actually Binary or the TinyInt type in MYSQL speak
    cursor.execute("CREATE TABLE MondayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursor.execute("CREATE TABLE TuesdayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursor.execute("CREATE TABLE WednesdayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursor.execute("CREATE TABLE ThursdayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursor.execute("CREATE TABLE FridayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursor.execute("CREATE TABLE SaturdayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursor.execute("CREATE TABLE SundayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    #Monday-Sunday Worker Availability, TIME in mysql is written 'HH:MM:SS'
    cursor.execute("CREATE TABLE MondayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE TuesdayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE WednesdayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE ThursdayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE FridayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE SaturdayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE SundayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    #Store Hours Mon-Friday
    cursor.execute("CREATE TABLE Schedule(auto_id INT NOT NULL, Employee_id INT, Date DATE, start_time TIME, end_time TIME, PRIMARY KEY(auto_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    #Schedule data for employees.

    cursor.close()

#Autofill db tables
create_db()