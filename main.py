from flask import Flask, request, render_template
from flask_restplus import reqparse, abort, Api, Resource
from flask_sockets import Sockets
from flask_cors import CORS, cross_origin
import os
import subprocess
from apiv1 import blueprint as apiv1
from apiv2 import blueprint as apiv2
from apiv3 import blueprint as apiv3

"""

Service listens on port 5000 (Flask Default Port)

"""

app = Flask(__name__)

api = Api(app=app)
sockets = Sockets(app)

# Api v1 - REST
api_v1 = app.register_blueprint(apiv1, url_prefix='/api/v1')

# Api v2 - GRAPHQL
api_v2 = app.register_blueprint(apiv2)

# Api v3 - WEBSOCKETS 
api_v3 = sockets.register_blueprint(apiv3)
# @sockets.route('/chat')
# def chat_socket(ws):
#     while not ws.closed:
#         message = ws.receive()
#         if message is None:  # message is "None" if the client has closed.
#             continue
#         clients = ws.handler.server.clients.values()
#         for client in clients:
#             client.ws.send(message)

CORS(app, resources={r"/*": {"origins": "*", "methods":["GET","POST"]}})

@app.route('/web')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Look for environment variable APPENV
    try:
        currentDirectory = os.getcwd()
        # Decrypt secrets
        with open(os.getcwd()+"/secrets/openssl","r") as f:
            envList = str(f.readline()).replace("$","").split(",")
            os.chdir(os.getcwd()+"/secrets")
            subprocess.Popen([f"openssl aes-256-cbc -K {os.environ[str(envList[0])]} -iv {os.environ[str(envList[1])]} -in secrets.tar.enc -out secrets.tar -d && tar xvf secrets.tar"],shell=True).wait()
            os.chdir(currentDirectory)
        app.run(host='0.0.0.0', debug=True)
    except:
        print("ERROR")
        app.run(host='0.0.0.0', debug=True)