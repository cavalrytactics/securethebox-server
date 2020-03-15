from flask import Blueprint
from flask_graphql import GraphQLView
from app_schema.schema import schema
from mongoengine import connect
import os 

connect(os.environ["MONGODB_NAMESPACE"], host="mongodb+srv://"+os.environ["MONGODB_USER"]+":"+os.environ["MONGODB_PASSWORD"]+"@"+os.environ["MONGODB_CLUSTER"], alias="default")

blueprint = Blueprint('apiv2', __name__)

blueprint.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)
# GRAPHQL API