from flask import Flask, send_from_directory, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from waitress import serve
import os
import json
import db

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

# localhost:5000/api/setStoreName?name=X&token=X
@app.route('/api/setStoreName', methods=['GET', 'POST'])
@limiter.limit("1/second")
def setStoreName():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        name = request.args.get('name')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        name = jsonres.get('token')
    if(token is None or name is None):
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
    err = user.store.setName(name)
    if(err):
        return {
            "error": err
        }
    else:
        return json.dumps(user.store.to_dict())

# localhost:5000/api/setStoreName?name=X&token=X
@app.route('/api/setStoreAddress', methods=['GET', 'POST'])
@limiter.limit("1/second")
def setStoreAddress():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        address = request.args.get('address')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        address = jsonres.get('address')
    if(token is None or address is None):
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
    
    #Set address
    err = user.store.setAddress(address)
    if(err):
        return {
            "error": err
        }
    else:
        return json.dumps(user.store.to_dict())

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

@app.route('/api/setEmployee', methods=['GET', 'POST'])
@limiter.limit("1/second")
def setEmployee():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('id')
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')
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

@app.route('/api/deleteEmployee', methods=['GET', 'POST'])
@limiter.limit("1/second")
def deleteEmployee():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('id')
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

# localhost:5000/api/getEmployee?token=X&id=X
@app.route('/api/getEmployee', methods=['GET', 'POST'])
@limiter.limit("1/second")
def getEmployee():

    #Get params
    if request.method == 'GET':
        token = request.args.get('token')
        id = request.args.get('id')
    elif request.method == 'POST':
        jsonres = request.get_json()
        token = jsonres.get('token')
        id = jsonres.get('id')
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