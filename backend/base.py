from flask import Flask, send_from_directory, request
import logging
from waitress import serve
import os
import db

app = Flask("OptiServe", static_folder='../frontend/build')

# localhost:5000/api/hello
@app.route('/api/hello')
def hello_world():
    response_body = {
        "name": "Hello!",
        "response": "Hello, world! :)"
    }

    return response_body

# localhost:5000/api/dbtestinsert?name=Walter White&place=308 Negra Arroyo Lane, Albuquerque, New Mexico
@app.route('/api/dbtestinsert', methods=['GET'])
def dbtestinsert():
    if request.method == 'GET':
        db.db_insert(request.args.get('name'), request.args.get('place'))

    response_body = {
        "response": "Successfully inserted data."
    }

    return response_body

# localhost:5000/api/dbtestretrieve
@app.route('/api/dbtestretrieve')
def dbtestretrieve():
    retrieve = db.db_retrieve()

    return retrieve

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