from flask import Flask, send_from_directory
from waitress import serve
import os

app = Flask(__name__, static_folder='../frontend/build')

@app.route('/api/hello')
def hello_world():
    response_body = {
        "name": "Hello!",
        "response": "Hello, world!"
    }

    return response_body

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

#@app.errorhandler(404)
#def not_found(e):
#    return app.send_static_file('../frontend/build/index.html')

if __name__ == "__main__":
    serve(app, listen='*:9090')