import mysql.connector
import os
import time
import config
#Using a local config file for MySQLDB info for security practice but if you don't want to bother
#on local machine just remove config file and fill in host, user, password manually(typically host="localhost", user="root" and whatever password you use.)

# Loop to wait for mysql server, there's probably a better way of doing this
def init_db():
    try:
        mysqldb = mysql.connector.connect(
            host=config.getHost(),
            user=config.getUser(),
            # env declared in docker-compose
            password=config.getPass(),
            #Pull data from config file.
            
        )
    except (mysql.connector.errors.InterfaceError, mysql.connector.errors.DatabaseError):
        print(mysql.connector.errors.InterfaceError, mysql.connector.errors.DatabaseError)
        time.sleep(5)
        mysqldb = init_db()
    
    return mysqldb, mysqldb.cursor()

def create_db(cursorObj):
    cursorObj.execute("CREATE DATABASE OptiDB;")
    cursorObj.execute("USE OptiDB;")
    cursorObj.execute("CREATE TABLE Store(store_id INT NOT NULL, store_name varchar(99) NOT NULL, store_address varchar(99) NOT NULL, PRIMARY KEY(store_id));")
    cursorObj.execute("CREATE TABLE Holiday(store_id INT, start_date DATE, end_date DATE, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id));")
    cursorObj.execute("CREATE TABLE Employee(Employee_id INT NOT NULL, store_id INT, first_name varchar(40) NOT NULL, last_name varchar(40) NOT NULL, PTO_Days_Rem INT, DOB DATE, PRIMARY KEY(Employee_id), FOREIGN KEY(store_id) REFERENCES Store(store_id));")
    #DOB References Date of Birth for employees. DATE type in mysql is written 'YYYY-MM-DD'
    cursorObj.execute("CREATE TABLE TimeOff(Employee_id INT, PTO BOOLEAN, start_date DATE, end_date DATE, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id));")
    #Time off table for workers. Careful with BOOLEAN type its actually Binary or the TinyInt type in MYSQL speak
    cursorObj.execute("CREATE TABLE MondayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursorObj.execute("CREATE TABLE TuesdayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursorObj.execute("CREATE TABLE WednesdayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursorObj.execute("CREATE TABLE ThursdayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursorObj.execute("CREATE TABLE FridayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursorObj.execute("CREATE TABLE SaturdayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    cursorObj.execute("CREATE TABLE SundayAvail(Employee_id INT, start_time TIME, end_time TIME, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    #Monday-Sunday Worker Availability, TIME in mysql is written 'HH:MM:SS'
    cursorObj.execute("CREATE TABLE MondayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursorObj.execute("CREATE TABLE TuesdayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursorObj.execute("CREATE TABLE WednesdayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursorObj.execute("CREATE TABLE ThursdayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursorObj.execute("CREATE TABLE FridayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursorObj.execute("CREATE TABLE SaturdayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursorObj.execute("CREATE TABLE SundayHours(store_id INT, open_time TIME, close_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    #Store Hours Mon-Friday
    cursorObj.execute("CREATE TABLE Schedule(auto_id INT NOT NULL, Employee_id INT, Date DATE, start_time TIME, end_time TIME, PRIMARY KEY(auto_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    #Schedule data for employees. 
    


    #cursorObj.execute("CREATE TABLE Employee();")
    return


# Init db
dbOBj, cursorObj = init_db()

cursorObj.execute("SHOW DATABASES;")
DB_Exists = False
for x in cursorObj:
    if str(x) == '(\'OptiDB\',)':
        DB_Exists = True

if(not DB_Exists):
    create_db(cursorObj)

#Checks if the database is currently on system if not it manually creates the database and tables
