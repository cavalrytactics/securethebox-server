from flask import Blueprint
from flask_graphql import GraphQLView
from graphql.backend import GraphQLCoreBackend
from app_schema.schema import schema
from mongoengine import connect
import os 
from over import OveridenView

connect(os.environ["MONGODB_NAMESPACE"], host="mongodb+srv://"+os.environ["MONGODB_USER"]+":"+os.environ["MONGODB_PASSWORD"]+"@"+os.environ["MONGODB_CLUSTER"], alias="default")

blueprint = Blueprint('apiv2', __name__)

class GraphQLCustomCoreBackend(GraphQLCoreBackend):
    def __init__(self, executor=None):
        # type: (Optional[Any]) -> None
        super().__init__(executor)
        self.execute_params['allow_subscriptions'] = True

blueprint.add_url_rule('/graphql', view_func=OveridenView.as_view('graphql', schema=schema, backend=GraphQLCustomCoreBackend(), graphiql=True))


# GRAPHQL API