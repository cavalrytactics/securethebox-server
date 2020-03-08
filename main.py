from flask import Flask, request
from flask_restplus import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import os
from apiv1 import blueprint as apiv1
from apiv2 import blueprint as apiv2

"""

Service listens on port 5000 (Flask Default Port)

"""

app = Flask(__name__)
api = Api(app=app)

# Api v1 - REST
api_v1 = app.register_blueprint(apiv1, url_prefix='/api/v1')

# Api v2 - GRAPHQL
api_v2 = app.register_blueprint(apiv2)

CORS(app, resources={r"/*": {"origins": "*", "methods":["GET","POST"]}})

if __name__ == '__main__':
    # Look for environment variable APPENV
    try:
        currentDirectory = os.getcwd()
        with open(os.getcwd()+"/secrets/openssl","r") as f:
            envList = str(f.readline()).replace("$","").split(",")
            os.chdir(os.getcwd()+"/secrets")
            subprocess.Popen([f"openssl aes-256-cbc -K {os.environ[str(envList[0])]} -iv {os.environ[str(envList[1])]} -in secrets.tar.enc -out secrets.tar -d && tar xvf secrets.tar"],shell=True).wait()
            os.chdir(currentDirectory)
        app.run(host='0.0.0.0', debug=True)
    except:
        print("ERROR")
        app.run(host='0.0.0.0', debug=True)