from datetime import datetime
from tracemalloc import start
import mysql.connector
import os
import time
import logging
import secrets
import string
import re
import bcrypt

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
    db.ping(True)
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

    cursor.execute("CREATE TABLE Store(store_id INT NOT NULL AUTO_INCREMENT, store_name varchar(99), store_address varchar(99), PRIMARY KEY(store_id))")
    cursor.execute("CREATE TABLE Holiday(store_id INT, name VARCHAR(40), start_date DATE, end_date DATE, start_time TIME, end_time TIME, PRIMARY KEY(store_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE Employee(Employee_id INT NOT NULL AUTO_INCREMENT, store_id INT, first_name varchar(40) NOT NULL, last_name varchar(40) NOT NULL, PTO_Days_Rem INT, DOB DATE, PRIMARY KEY(Employee_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    
    #DOB References Date of Birth for employees. DATE type in mysql is written 'YYYY-MM-DD'
    cursor.execute("CREATE TABLE TimeOff(Employee_id INT, start_date DATE, end_date DATE, start_time TIME, end_time TIME, total_hours INT, PRIMARY KEY(Employee_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
   
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
    cursor.execute("CREATE TABLE Schedule(auto_id INT NOT NULL AUTO_INCREMENT, Employee_id INT, Date DATE, start_time TIME, end_time TIME, PRIMARY KEY(auto_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
    
    #Users for login info
    cursor.execute("CREATE TABLE User(user_id INT NOT NULL AUTO_INCREMENT, store_id INT, username varchar(99) NOT NULL, password varchar(99) NOT NULL, token varchar(99) NOT NULL, PRIMARY KEY(user_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")

    cursor.close()

#Autofill db tables
create_db()

#Shorthand execute w/ error catching. Returns if db error.
def execute(query: str, params: tuple, returnID: bool = False):
    db.ping(True)
    cursor = db.cursor()
    try:
        cursor.execute(query, params)
    except Exception as e:
        cursor.close()
        log.warning(e)
        return "Database error."
    
    id = cursor.lastrowid
    db.commit()
    cursor.close()

    if(returnID):
        return id

class Employee:
    #Add employee
    def add(self, store_id: str, first_name: str, last_name: str, PTO_Days_Rem: int = 0, DOB: str = '2000-01-01'):
        self.store_id = store_id
        self.first_name = first_name
        self.last_name = last_name
        self.PTO_Days_Rem = PTO_Days_Rem
        self.DOB = DOB

        #Insert into DB
        ex = execute("INSERT INTO Employee (store_id, first_name, last_name, PTO_Days_Rem, DOB) VALUES (%s, %s, %s, %s, %s)", (store_id, first_name, last_name, PTO_Days_Rem, DOB), True)
        if(ex == "Database error."):
            return ex
        
        self.id = ex
        log.warning("Employee \"" + self.first_name + "\" has been added!")
    
    #Get employee w/ id
    def get(self, id: str):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM Employee WHERE Employee_id = %s", (id, ))
        result = cursor.fetchone()
        cursor.close()

        if(result):
            self.id = result[0]
            self.store_id = result[1]
            self.first_name = result[2]
            self.last_name = result[3]
            self.PTO_Days_Rem = result[4]
            self.DOB = result[5]
        else:
            return "Could not find Employee."
        
    #Set optional employee data
    def set(self, first_name: str = None, last_name: str = None, PTO_Days_Rem: int = None, DOB: str = None):
        if(not self.first_name):
            return "Cannot set before initialization!"

        if(first_name):
            self.first_name = first_name
        if(last_name):
            self.last_name = last_name
        if(PTO_Days_Rem):
            self.PTO_Days_Rem = PTO_Days_Rem
        if(DOB):
            self.DOB = DOB
        
        log.warning("Employee \"" + self.first_name + "\" has been updated!")
        return execute("UPDATE Employee SET first_name = %s, last_name = %s, PTO_Days_Rem = %s, DOB = %s WHERE Employee_id = %s", (self.first_name, self.last_name, self.PTO_Days_Rem, self.DOB, self.id))
    
    #Delete employee from db
    def delete(self):
        log.warning("Employee \"" + self.first_name + "\" has been deleted!")
        return execute("DELETE FROM Employee WHERE Employee_id = %s", (self.id, ))
        
    def to_dict(self):
        return {
            "id": self.id,
            "store_id": self.store_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "PTO_Days_Rem": self.PTO_Days_Rem,
            "DOB": self.DOB
        }

class Store:
    #Add Store with default values for name & address
    def add(self, name: str = " ", address: str = " "):
        self.name = name
        self.address = address

        #Insert into DB
        ex = execute("INSERT INTO Store (store_name, store_address) VALUES (%s, %s)", (self.name, self.address), True)
        if(ex == "Database error."):
            return ex
        
        #Set ID
        self.id = ex
        log.warning("Store \"" + str(self.id) + "\" has been added!")
    
    #Get Store using ID, returning if successful
    def get(self, id: str):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM Store WHERE store_id = %s", (id, ))
        result = cursor.fetchone()
        cursor.close()

        if(result):
            self.id = result[0]
            self.name = result[1]
            self.address = result[2]
        else:
            return "Could not find store."
    
    #Set store with optional values name, address
    def set(self, name: str = None, address: str = None):
        if(not self.name):
            return "Cannot set name before initialization!"
        
        if(name):
            self.name = name
        if(address):
            self.address = address
        
        log.warning("Store \"" + self.name + "\" has been updated!")
        return execute("UPDATE Store SET store_name = %s, store_address = %s WHERE store_id = %s", (self.name, self.address, self.id))
    
    #Get all employees for store
    def getEmployees(self):
        db.ping(True)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Employee WHERE store_id = %s", (self.id, ))
        result = cursor.fetchall()
        cursor.close()
        employees = []

        #Cycles through all matching employees in db, appends them to list
        for employee in result:
            e = Employee()
            e.get(employee[0])
            employees.append(e)

        return employees

    #Set employee time off
    def set_time_off(self, start_date, end_date, start_time, end_time, employee_id):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM Employee WHERE Employee_id = %s", (employee_id))
        result = cursor.fetchone()

        if not result:
            log.warning("Invalid Employee id.")
            #checks if employee exists
        else:
            cursor.execute("Insert INTO TimeOff (Employee_id, start_date, end_date, start_time, end_time) VALUES (%s, %s, %s, %s, %s)", (employee_id, start_date, end_date, start_time, end_time))
            cursor.close()
            log.warning("Time off successfully added.")
        return

    #update employee time off
    def update_time_off(old_start_date, old_end_date, employee_id, new_start_date, new_end_date, start_time, end_time):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM TimeOff WHERE Employee_id = %s AND start_date = %s AND end_date = %s", (employee_id, old_start_date, old_end_date))
        result = cursor.fetchone()

        if not result:
            log.warning("Invalid input. Either incorrect employee id or time off dates.")
            #checks if employee exists
        else:
            cursor.execute("UPDATE TimeOff SET start_date = %s end_date = %s start_time = %s end_time = %s WHERE Employee_id = %s AND start_date = %s AND end_date = %s", (new_start_date, new_end_date, start_time, end_time, employee_id, old_start_date, old_end_date))
            cursor.close()
            log.warning("Time off successfully updated.")
            
        return

    def set_holiday(self, name, start_date, end_date, start_time, end_time ):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("INSERT INTO Holiday (store_id, name, start_date, end_date, start_time, end_time) VALUES (%s, %s, %s, %s, %s, %s)", (self.id, name, start_date, end_date, start_time, end_time))
        #simple execution alterations to this table should be open to MANAGERS ONLY
        cursor.close()
        return

    def update_holiday(self, old_name, old_start_date, old_end_date, new_name, new_start_date, new_end_date, start_time, end_time):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM Holiday WHERE store_id = %s AND old_start_date = %s AND old_end_date = %s AND old_name = %s", (self.id, old_start_date, old_end_date, old_name))
        result = cursor.fetchone()

        if not result:
            log.warning("Invalid input. Either incorrect dates or holiday name")
            #checks if employee exists
        else:
            cursor.execute("UPDATE TimeOff SET name = %s start_date = %s end_date = %s start_time = %s end_time = %s WHERE Employee_id = %s AND start_date = %s AND end_date = %s AND old_name = %s", (new_name, new_start_date, new_end_date, start_time, end_time, self.id, old_start_date, old_end_date, old_name))
            cursor.close()
            log.warning("Holiday successfully updated.")
        return


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }

class User:
    #Adds user and generates id & token
    def add(self, username: str, password: str):
        #Validate username
        if(re.search("^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$", username)):
            self.username = username
        else:
            return "Username must be 8 to 20 characters long, and contain no special characters."
        
        #Validate password
        if(re.search("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password)):
            #hash password
            salt = bcrypt.gensalt()
            hashedpw = bcrypt.hashpw(password.encode('utf-8'), salt)
            self.password = hashedpw
        else:
            return "Password must be at least 8 characters, contain one letter and one number."
        
        #Generate token
        self.token = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(20))


        #Generate store
        self.store = Store()
        self.store.add()
        
        #Insert into DB
        ex = execute("INSERT INTO User (store_id, username, password, token) VALUES (%s, %s, %s, %s)", (self.store.id, self.username, self.password, self.token), True)
        if(ex == "Database error."):
            return ex
        
        #Set ID
        self.id = ex
        log.warning("User \"" + username + "\" has been added!")

    
    #Gets user with username & password
    def getUserPass(self, username: str, password: str):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM User WHERE username = %s", (username, ))
        result = cursor.fetchone()
        cursor.close()

        if(result):
            self.id = result[0]
            self.store = Store()
            self.store.get(result[1])
            self.username = result[2]

            #check hashed pw
            if(bcrypt.checkpw(password.encode('utf-8'), result[3].encode('utf-8'))):
                self.password = result[3]
            else:
                return "Wrong password!"
            
            self.token = result[4]
        else:
            log.warning("Could not find user.")

            return "Could not find user."
    
    #Gets user with token
    def get(self, token: str):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM User WHERE token = %s", (token, ))
        result = cursor.fetchone()
        cursor.close()

        if(result):
            self.id = result[0]
            self.store = Store()
            self.store.get(result[1])
            self.username = result[2]
            self.password = result[3]
            self.token = result[4]
        else:
            log.warning("Could not find user.")

            return "Could not find user."
    
    #Changes store associated with user
    def setStore(self, store: Store):
        if(not self.store):
            return "Cannot set store before initialization!"
        
        self.store = store

        log.warning("User \"" + self.username + "\" has been updated!")
        return execute("UPDATE User SET store_id = %s WHERE user_id = %s", (self.store.id, self.id))

        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "store_id": self.store.id
        }