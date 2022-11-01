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

# localhost:5000/api/hello
@app.route('/api/hello')
@limiter.exempt
def hello_world():

    return {
        "name": "Hello!",
        "response": "Hello, world! :)"
    }

# localhost:5000/api/addUser?username=X&password=X
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

# localhost:5000/api/getToken?username=X&password=X
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

# localhost:5000/api/getUser?token=X
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

# localhost:5000/api/getStore?token=X
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

# localhost:5000/api/setStore?token=X&store_name=X&store_address=X
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

# localhost:5000/api/addEmployee?token=X&firstname=X&lastname=X
@app.route('/api/addEmployee', methods=['GET', 'POST'])
@limiter.limit("1/second")
def addEmployee():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        firstname = jsonres.get('first_name')
        lastname = jsonres.get('last_name')
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
    
    #Add employee
    employee = db.Employee()
    err = employee.add(user.store.id, firstname, lastname)
    if(err):
        return {
            "error": err
        }
    else:
        return {
            "success": "Successfully added employee."
        }

# localhost:5000/api/getEmployee?token=X&emp_id=X
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

# localhost:5000/api/getEmployees?token=X
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

# localhost:5000/api/setEmployee?token=X&emp_id=X&first_name=X
@app.route('/api/setEmployee', methods=['GET', 'POST'])
@limiter.limit("1/second")
def setEmployee():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('emp_id')
        firstname = request.args.get('first_name')
        lastname = request.args.get('last_name')
        pto = request.args.get('pto')
        dob = request.args.get('dob')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        id = jsonres.get('emp_id')
        firstname = jsonres.get('first_name')
        lastname = jsonres.get('last_name')
        pto = jsonres.get('pto')
        dob = jsonres.get('dob')
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

# localhost:5000/api/deleteEmployee?token=X
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

# localhost:5000/api/addTimeOff?token=X&name=X&start=X&end=X
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

# localhost:5000/api/getTimeOff?token=X&timeoff_id=X
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

# localhost:5000/api/getTimeOffs?token=X&emp_id=X
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

# localhost:5000/api/deleteTimeOff?token=X&timeoff_id=X
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

# localhost:5000/api/addHoliday?token=X&name=X&start=X&end=X
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

# localhost:5000/api/getHoliday?token=X&hol_id=X
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

# localhost:5000/api/getHolidays?token=X
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

# localhost:5000/api/deleteHoliday?token=X&hol_id=X
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