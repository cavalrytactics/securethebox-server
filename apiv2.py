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

# class GraphQLObservableUnboxingView(GraphQLView):
#     def execute_graphql_request(
#             self, request, data, query, variables, operation_name, show_graphiql=False
#     ):
#         target_result = None

#         def override_target_result(value):
#             nonlocal target_result
#             target_result = value

#         execution_result = super().execute_graphql_request(request, data, query, variables, operation_name, show_graphiql)
#         if execution_result:
#             if isinstance(execution_result, ObservableBase):
#                 target = execution_result.subscribe(on_next=lambda value: override_target_result(value))
#                 target.dispose()
#             else:
#                 return execution_result

#         return target_result

# blueprint.add_url_rule(
#     "/graphql", view_func=GraphQLObservableUnboxingView.as_view("graphql", schema=schema, graphiql=True, backend=GraphQLCustomCoreBackend())
# )

blueprint.add_url_rule('/graphql', view_func=OveridenView.as_view('graphql', schema=schema, backend=GraphQLCustomCoreBackend(), graphiql=True))


# GRAPHQL API