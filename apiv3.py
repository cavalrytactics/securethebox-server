from flask import Blueprint
from app_schema.schema import schema
import os 
from flask import render_template

blueprint = Blueprint('apiv3', __name__)

@blueprint.route('/chat')
def chat_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if message is None:  # message is "None" if the client has closed.
            continue
        clients = ws.handler.server.clients.values()
        for client in clients:
            client.ws.send(message)


# WEBSOCKETS