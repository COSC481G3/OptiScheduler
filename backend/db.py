from datetime import datetime
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
    cursor.execute("CREATE TABLE Holiday(holiday_id INT NOT NULL AUTO_INCREMENT, store_id INT, name VARCHAR(40), start DATETIME, end DATETIME, PRIMARY KEY(holiday_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE Employee(Employee_id INT NOT NULL AUTO_INCREMENT, store_id INT, first_name varchar(40) NOT NULL, last_name varchar(40) NOT NULL, PTO_Days_Rem INT, DOB DATE, PRIMARY KEY(Employee_id), FOREIGN KEY(store_id) REFERENCES Store(store_id))")
    cursor.execute("CREATE TABLE TimeOff(timeoff_id INT NOT NULL AUTO_INCREMENT, Employee_id INT, start DATETIME, end DATETIME, hours INT, PRIMARY KEY(timeoff_id), FOREIGN KEY(Employee_id) REFERENCES Employee(Employee_id))")
   
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

class TimeOff:
    #Add timeoff to db
    def add(self, emp_id: str, start: datetime, end: datetime):
        self.emp_id = emp_id
        self.start = start
        self.end = end
        #Get hours off
        duration = end - start
        self.hours = divmod(duration.total_seconds(), 3600)[0]

        #Insert into db
        ex = execute("INSERT INTO TimeOff (Employee_id, start, end, hours) VALUES (%s, %s, %s, %s)", (emp_id, start, end, self.hours), True)
        if(ex == "Database error."):
            return ex
        
        self.id = ex
        log.warning("TimeOff \"" + str(self.id) + "\" has been added!")
    
    #Get timeoff w/ id
    def get(self, id: str):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM TimeOff WHERE timeoff_id = %s", (id, ))
        result = cursor.fetchone()
        cursor.close()

        if(result):
            self.id = result[0]
            self.emp_id = result[1]
            self.start = result[2]
            self.end = result[3]
            self.hours = result[4]
        else:
            return "Could not find TimeOff."
    
    #Set timeoff with optional values
    def set(self, start: datetime = None, end: datetime = None):
        if(not self.id):
            return("Cannot set before init!")
        
        if(start):
            self.start = start
        if(end):
            self.end = end
        if(start or end):
            duration = end - start
            self.hours = divmod(duration.total_seconds(), 3600)[0]
        
        log.warning("TimeOff \"" + str(self.id) + "\" has been updated!")
        return execute("UPDATE TimeOff SET start = %s, end = %s, hours = %s WHERE timeoff_id = %s", (self.start, self.end, self.hours, self.id))
    
    #Delete timeoff from db
    def delete(self):
        log.warning("TimeOff \"" + str(self.id) + "\" has been deleted!")
        return execute("DELETE FROM TimeOff WHERE timeoff_id = %s", (self.id, ))
    
    def to_dict(self):
        return {
            "id": self.id,
            "emp_id": self.emp_id,
            "start": self.start,
            "end": self.end,
            "hours": self.hours
        }

class Holiday:
    #Add holiday to db
    def add(self, store_id: str, name: str, start: datetime, end: datetime):
        self.store_id = store_id
        self.name = name
        self.start = start
        self.end = end

        #Insert into db
        ex = execute("INSERT INTO Holiday (store_id, name, start, end) VALUES (%s, %s, %s, %s)", (store_id, name, start, end), True)
        if(ex == "Database error."):
            return ex
        
        self.id = ex
        log.warning("Holiday \"" + name + "\" has been added!")
    
    #Get holiday w/ id
    def get(self, id: str):
        db.ping(True)
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM Holiday WHERE holiday_id = %s", (id, ))
        result = cursor.fetchone()
        cursor.close()

        if(result):
            self.id = result[0]
            self.store_id = result[1]
            self.name = result[2]
            self.start = result[3]
            self.end = result[4]
        else:
            return "Could not find Holiday."
    
    #Set holiday with optional values
    def set(self, name: str = None, start: datetime = None, end: datetime = None):
        if(not self.id):
            return("Cannot set before init!")
        
        if(name):
            self.name = name
        if(start):
            self.start = start
        if(end):
            self.end = end
        
        log.warning("Holiday \"" + self.name + "\" has been updated!")
        return execute("UPDATE Holiday SET name = %s, start = %s, end = %s WHERE holiday_id = %s", (self.name, self.start, self.end, self.id))
    
    #Delete holiday from db
    def delete(self):
        log.warning("Employee \"" + self.name + "\" has been deleted!")
        return execute("DELETE FROM Holiday WHERE holiday_id = %s", (self.id, ))
    
    def to_dict(self):
        return {
            "id": self.id,
            "store_id": self.store_id,
            "name": self.name,
            "start": self.start,
            "end": self.end
        }

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
        if(not self.id):
            return "Cannot set before init!"

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
    
    #Get all timeoff for employee
    def getTimeOff(self):
        db.ping(True)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM TimeOff WHERE Employee_id = %s", (self.id, ))
        result = cursor.fetchall()
        cursor.close()
        timeoffs = []

        #Cycles through all matching holidays in db, appends them to list
        for timeoff in result:
            t = TimeOff()
            t.get(timeoff[0])
            timeoffs.append(t)

        return timeoffs
        
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
        if(not self.id):
            return "Cannot set name before init!"
        
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
    
    #Get all holidays for store
    def getHolidays(self):
        db.ping(True)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Holiday WHERE store_id = %s", (self.id, ))
        result = cursor.fetchall()
        cursor.close()
        holidays = []

        #Cycles through all matching holidays in db, appends them to list
        for holiday in result:
            h = Holiday()
            h.get(holiday[0])
            holidays.append(h)

        return holidays

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
            return "Cannot set store before init!"
        
        self.store = store

        log.warning("User \"" + self.username + "\" has been updated!")
        return execute("UPDATE User SET store_id = %s WHERE user_id = %s", (self.store.id, self.id))

        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "store_id": self.store.id
        }