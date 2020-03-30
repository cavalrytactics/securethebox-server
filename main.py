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
app.app_protocol = lambda environ_path_info: 'graphql-ws'

# Api v1 - REST
api_v1 = app.register_blueprint(apiv1, url_prefix='/api/v1')

# Api v2 - GRAPHQL
api_v2 = app.register_blueprint(apiv2)

# Api v3 - WEBSOCKETS 
api_v3 = sockets.register_blueprint(apiv3)

CORS(app, resources={r"/*": {"origins": "*", "methods":["GET","POST"]}})

@app.route('/web')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    
    # Look for environment variable APPENV
    try:
        currentDirectory = os.getcwd()
        # Decrypt secrets
        with open(os.getcwd()+"/secrets/openssl","r") as f:
            envList = str(f.readline()).replace("$","").split(",")
            os.chdir(os.getcwd()+"/secrets")
            subprocess.Popen([f"openssl aes-256-cbc -K {os.environ[str(envList[0])]} -iv {os.environ[str(envList[1])]} -in secrets.tar.enc -out secrets.tar -d && tar xvf secrets.tar"],shell=True).wait()
            os.chdir(currentDirectory)
        # app.run(host='0.0.0.0', debug=True)
        server = pywsgi.WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
        server.serve_forever()
    except:
        print("ERROR")
        server = pywsgi.WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
        server.serve_forever()
        # app.run(host='0.0.0.0', debug=True)