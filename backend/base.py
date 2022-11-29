from flask import Flask, send_from_directory, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from waitress import serve
from datetime import datetime
from backend import db
import os
import json

app = Flask("OptiServe", static_folder='../frontend/build')
limiter = Limiter(
    app,
    key_func=get_remote_address,
    storage_uri="memory://"
)

# /api/hello
@app.route('/api/hello')
@limiter.exempt
def hello_world():

    return {
        "name": "Hello!",
        "response": "Hello, world! :)"
    }

# /api/addUser?username=X&password=X
@app.route('/api/addUser', methods=['GET', 'POST'])
@limiter.limit("1/second")
def addUser():

    #Get params
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
    elif request.method == 'POST':
        jsonres = request.get_json()
        username = jsonres.get('username')
        password = jsonres.get('password')
    if(username is None or password is None):
        return {
            "error": "Value cannot be null!"
        }

    #Add user
    user = db.User()
    err = user.add(username, password)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully added user."
        }

# /api/getToken?username=X&password=X
@app.route('/api/getToken', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getToken():

    #Get params
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
    elif request.method == 'POST':
        jsonres = request.get_json()
        username = jsonres.get("username")
        password = jsonres.get('password')
    if(username is None or password is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.getUserPass(username, password)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "token": user.token
        }

# /api/getUser?token=X
@app.route('/api/getUser', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getUser():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
    if(token is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    else:
        return json.dumps(user.to_dict())

# /api/getStore?token=X
@app.route('/api/getStore', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getStore():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
    if(token is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    else:
        return json.dumps(user.store.to_dict())

# /api/setStore?token=X&store_name=X&store_address=X
@app.route('/api/setStore', methods=['GET', 'POST'])
@limiter.limit("1/second")
def setStoreName():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        name = request.args.get('store_name')
        address = request.args.get('store_address')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        name = jsonres.get('store_name')
        address = jsonres.get('store_address')
    if(token is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Set name
    err = user.store.set(name, address)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully updated store."
        }

# /api/addEmployee?token=X&firstname=X&lastname=X
@app.route('/api/addEmployee', methods=['GET', 'POST'])
@limiter.limit("1/second")
def addEmployee():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')
        pto = request.args.get('PTO_Days_Rem')
        dob = request.args.get('DOB')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        firstname = jsonres.get('first_name')
        lastname = jsonres.get('last_name')
        pto = jsonres.get('PTO_Days_Rem')
        dob = jsonres.get('DOB')
    if(token is None or firstname is None or lastname is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Format date
    try:
        if(dob):
            dob = datetime.fromisoformat(dob)
    except ValueError:
        return {
            "error": "dob must be in ISO8601!"
        }
    
    #Convert to int
    try:
        pto = int(pto)
    except TypeError:
        return {
            "error": "PTO must be a number!"
        }
    
    #Add employee
    employee = db.Employee()
    err = employee.add(user.store.id, firstname, lastname, pto, dob)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully added employee."
        }

# /api/getEmployee?token=X&emp_id=X
@app.route('/api/getEmployee', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getEmployee():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('emp_id')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        id = jsonres.get('emp_id')
    if(token is None or id is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get employee
    emp = db.Employee()
    err = emp.get(id)
    if(err):
        return {
            "error": err
        }
    else:
        return json.dumps(emp.to_dict(), default=str)

# /api/getEmployees?token=X
@app.route('/api/getEmployees', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getEmployees():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
    if(token is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get employees
    employees = [emp.to_dict() for emp in user.store.getEmployees()]
    return json.dumps({"employees": employees}, default=str)

# /api/setEmployee?token=X&emp_id=X&first_name=X
@app.route('/api/setEmployee', methods=['GET', 'POST'])
@limiter.limit("1/second")
def setEmployee():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('emp_id')
        firstname = request.args.get('first_name')
        lastname = request.args.get('last_name')
        pto = request.args.get('PTO_Days_Rem')
        dob = request.args.get('DOB')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        id = jsonres.get('emp_id')
        firstname = jsonres.get('first_name')
        lastname = jsonres.get('last_name')
        pto = jsonres.get('PTO_Days_Rem')
        dob = jsonres.get('DOB')
    if(token is None or id is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get employee
    emp = db.Employee()
    err = emp.get(id)
    if(err):
        return {
            "error": err
        }
    
    #Set employee
    err = emp.set(firstname, lastname, pto, dob)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully added employee."
        }

# /api/deleteEmployee?token=X
@app.route('/api/deleteEmployee', methods=['GET', 'POST'])
@limiter.limit("1/second")
def deleteEmployee():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('emp_id')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        id = jsonres.get('emp_id')
    if(token is None or id is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get employee
    emp = db.Employee()
    err = emp.get(id)
    if(err):
        return {
            "error": err
        }
    
    #Delete employee
    err = emp.delete()
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully deleted employee."
        }

# /api/addTimeOff?token=X&name=X&start=X&end=X
# start and end should be in ISO8601 date format
@app.route('/api/addTimeOff', methods=['GET', 'POST'])
@limiter.limit("1/second")
def addTimeOff():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        emp_id = request.args.get('emp_id')
        start = request.args.get('start')
        end = request.args.get('end')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        emp_id = request.args.get('emp_id')
        start = jsonres.get('start')
        end = jsonres.get('end')
    if(token is None or emp_id is None or start is None or end is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get employee
    emp = db.Employee()
    err = emp.get(emp_id)
    if(err):
        return {
            "error": err
        }
    
    #Format date
    try:
        startdate = datetime.fromisoformat(start)
        enddate = datetime.fromisoformat(end)
    except ValueError:
        return {
            "error": "start & end must be in ISO8601!"
        }
    
    #Add timeoff
    timeoff = db.TimeOff()
    err = timeoff.add(emp.id, startdate, enddate)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully added timeoff."
        }

# /api/getTimeOff?token=X&timeoff_id=X
@app.route('/api/getTimeOff', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getTimeOff():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('timeoff_id')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        id = jsonres.get('timeoff_id')
    if(token is None or id is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get TimeOff
    timeoff = db.TimeOff()
    err = timeoff.get(id)
    if(err):
        return {
            "error": err
        }
    else:
        return json.dumps(timeoff.to_dict(), default=str)

# /api/getTimeOffs?token=X&emp_id=X
@app.route('/api/getTimeOffs', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getTimeOffs():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        emp_id = request.args.get('emp_id')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        emp_id = jsonres.get('emp_id')
    if(token is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get employee
    emp = db.Employee()
    err = emp.get(emp_id)
    if(err):
        return {
            "error": err
        }
    
    #Get time off
    timeoffs = [timeoff.to_dict() for timeoff in emp.getTimeOff()]
    return json.dumps({"timeoffs": timeoffs}, default=str)

# /api/deleteTimeOff?token=X&timeoff_id=X
@app.route('/api/deleteTimeOff', methods=['GET', 'POST'])
@limiter.limit("1/second")
def deleteTimeOff():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('timeoff_id')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        id = jsonres.get('timeoff_id')
    if(token is None or id is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get timeoff
    timeoff = db.TimeOff()
    err = timeoff.get(id)
    if(err):
        return {
            "error": err
        }
    
    #Delete employee
    err = timeoff.delete()
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully deleted holiday."
        }

# /api/addHoliday?token=X&name=X&start=X&end=X
# start and end should be in ISO8601 date format
@app.route('/api/addHoliday', methods=['GET', 'POST'])
@limiter.limit("1/second")
def addHoliday():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        name = request.args.get('name')
        start = request.args.get('start')
        end = request.args.get('end')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        name = jsonres.get('name')
        start = jsonres.get('start')
        end = jsonres.get('end')
    if(token is None or name is None or start is None or end is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Format date
    try:
        startdate = datetime.fromisoformat(start)
        enddate = datetime.fromisoformat(end)
    except ValueError:
        return {
            "error": "start & end must be in ISO8601!"
        }
    
    #Add holiday
    holiday = db.Holiday()
    err = holiday.add(user.store.id, name, startdate, enddate)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully added holiday."
        }

# /api/getHoliday?token=X&hol_id=X
@app.route('/api/getHoliday', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getHoliday():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('hol_id')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        id = jsonres.get('hol_id')
    if(token is None or id is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get holiday
    hol = db.Holiday()
    err = hol.get(id)
    if(err):
        return {
            "error": err
        }
    else:
        return json.dumps(hol.to_dict(), default=str)

# /api/getHolidays?token=X
@app.route('/api/getHolidays', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getHolidays():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
    if(token is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get holidays
    holidays = [hol.to_dict() for hol in user.store.getHolidays()]
    return json.dumps({"holidays": holidays}, default=str)

# /api/deleteHoliday?token=X&hol_id=X
@app.route('/api/deleteHoliday', methods=['GET', 'POST'])
@limiter.limit("1/second")
def deleteHoliday():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('hol_id')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        id = jsonres.get('hol_id')
    if(token is None or id is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get holiday
    hol = db.Holiday()
    err = hol.get(id)
    if(err):
        return {
            "error": err
        }
    
    #Delete employee
    err = hol.delete()
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully deleted holiday."
        }

# /api/addHours?token=X&day=X&open_time=X&close_time=X
@app.route('/api/addHours', methods=['GET', 'POST'])
def addHours():
    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        day = request.args.get('day')
        open_time = request.args.get('open_time')
        close_time = request.args.get('close_time')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        day = jsonres.get('day')
        open_time = jsonres.get('open_time')
        close_time = jsonres.get('close_time')
    if(token is None or day is None or open_time is None or close_time is None):
        return {
            "error": "Value cannot be null!"
        }

    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get hours
    hours = db.Hours()
    err = hours.get(user.store.id, day)
    if(not err):
        err = hours.set(open_time, close_time)
        if(err):
            return {
                "error": err
            }
        else:
            return {
                "success": "Successfully updated hours."
            }
    
    #Add hours
    err = hours.add(user.store.id, day, open_time, close_time)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully added hours."
        }

# /api/getHours?token=X
@app.route('/api/getHours', methods=['GET', 'POST'])
def getHours():
    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
    if(token is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get hours
    hours = [hour.to_dict() for hour in user.store.getHours()]
    return json.dumps({"hours": hours}, default=str)

# /api/setHours?token=X&day=X&open_time=X&close_time=X
@app.route('/api/setHours', methods=['GET', 'POST'])
def setHours():
    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        day = request.args.get('day')
        open_time = request.args.get('open_time')
        close_time = request.args.get('close_time')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        day = jsonres.get('day')
        open_time = jsonres.get('open_time')
        close_time = jsonres.get('close_time')
    if(token is None or day is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Format date
    try:
        if(open_time):
            open_time = datetime.fromisoformat(open_time)
        if(close_time):
            close_time = datetime.fromisoformat(close_time)
    except ValueError:
        return {
            "error": "start & end must be in ISO8601!"
        }
    
    #Get hours
    hours = db.Hours()
    err = hours.get(user.store.id, day)
    if(err):
        return {
            "error": "Hours not yet added!"
        }
    
    #Set hours
    err = hours.set(open_time, close_time)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully updated hours."
        }

# /api/deleteHours?token=X&day=X
@app.route('/api/deleteHours', methods=['GET, POST'])
def deleteHours():
    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        day = request.args.get('day')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        day = jsonres.get('day')
    if(token is None or day is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get hours
    hour = db.Hours()
    err = hour.get(user.store.id, day)
    if(err):
        return {
            "error": err
        }
    
    #Delete hours
    err = hour.delete()
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully deleted hours."
        }

# /api/addAvailability?token=X&emp_id=X&day=X&start_time=X&end_time=X
@app.route('/api/addAvailability', methods=['GET', 'POST'])
def addAvailability():
    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        emp_id = request.args.get('emp_id')
        day = request.args.get('day')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        emp_id = jsonres.get('emp_id')
        day = jsonres.get('day')
        start_time = jsonres.get('start_time')
        end_time = jsonres.get('end_time')
    if(token is None or emp_id is None or day is None or start_time is None or end_time is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get availability
    avail = db.Availability()
    err = avail.get(emp_id, day)
    if(not err):
        err = avail.set(start_time, end_time)
        if(err):
            return err
        else:
            return {
                "success": "Successfully updated availability"
            }
    
    #Add availability
    err = avail.add(emp_id, day, start_time, end_time)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully added availability."
        }

# /api/getAvailability?token=X&emp_id=X
@app.route('/api/getAvailability', methods=['GET', 'POST'])
def getAvailability():
    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        emp_id = request.args.get('emp_id')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        emp_id = jsonres.get('emp_id')
    if(token is None or emp_id is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get employee
    employee = db.Employee()
    err = employee.get(emp_id)
    if(err):
        return {
            "error": err
        }
    
    #Get availability
    availabilities = [ava.to_dict() for ava in employee.getAvailability()]
    return json.dumps({"availability": availabilities}, default=str)

# /api/setAvailability?token=X&emp_id=X&day=X&start_time=X&end_time=X
@app.route('/api/setAvailability', methods=['GET', 'POST'])
def setAvailability():
    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        emp_id = request.args.get('emp_id')
        day = request.args.get('day')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        emp_id = jsonres.get('emp_id')
        day = jsonres.get('day')
        start_time = jsonres.get('start_time')
        end_time = jsonres.get('end_time')
    if(token is None or day is None or emp_id is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Format date
    try:
        if(start_time):
            start_time = datetime.fromisoformat(start_time)
        if(end_time):
            end_time = datetime.fromisoformat(end_time)
    except ValueError:
        return {
            "error": "start & end must be in ISO8601!"
        }

    #Get availability
    avail = db.Availability()
    err = avail.get(emp_id, day)
    if(err):
        return {
            "error": "Availability not yet added!"
        }
    
    #Set availability
    err = avail.set(start_time, end_time)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully set availability."
        }

# /api/deleteAvailability?token=X&emp_id=X&day=X
@app.route('/api/deleteAvailability', methods=['GET, POST'])
def deleteAvailability():
    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        emp_id = request.args.get('emp_id')
        day = request.args.get('day')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        emp_id = jsonres.get('emp_id')
        day = jsonres.get('day')
    if(token is None or emp_id is None or day is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get availability
    avail = db.Availability()
    err = avail.get(emp_id, day)
    if(err):
        return {
            "error": err
        }
    
    #Delete hours
    err = avail.delete()
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully deleted availability."
        }

@app.route('/api/getSchedule', methods=['GET', 'POST'])
def getSchedule():
    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        day = request.args.get('day')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        day = jsonres.get('day')
    if(token is None or day is None):
        return {
            "error": "Value cannot be null!"
        }
    
    #Convert day (int) to day (string)
    if(day == 0):
        day = "Sunday"
    elif(day == 1):
        day = "Monday"
    elif(day == 2):
        day = "Tuesday"
    elif(day == 3):
        day = "Wednesday"
    elif(day == 4):
        day = "Thursday"
    elif(day == 5):
        day = "Friday"
    elif(day == 6):
        day = "Saturday"

    #Get user
    user = db.User()
    err = user.get(token)
    if(err):
        return {
            "error": err
        }
    
    #Get hours
    hours = user.store.getHours(day)
    if(not hours):
        return {
            "error": "Hours not yet set!"
        }

    #Get employees
    employees = user.store.getEmployees()

    #Get availability
    avail_list = []
    for emp in employees:
        avail = emp.getAvailability(day)
        if(avail):
            avail.first_name = emp.first_name
            avail.last_name = emp.last_name

            if(avail.start_time < hours.open_time):
                avail.start_time = hours.open_time
            if(avail.end_time > hours.close_time):
                avail.end_time = hours.close_time

            avail_list.append(avail)
    
    avail_list.sort(key=lambda x: x.start_time)
    
    availabilities = [ava.to_dict() for ava in avail_list]
    return json.dumps({"availability": availabilities}, default=str)

# Returns the static content for production deployment
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Serves the app with waitress for production deployment
if __name__ == "__main__":
    serve(app, listen='*:5000')