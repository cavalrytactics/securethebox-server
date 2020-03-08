from flask_restplus import Namespace, Resource, fields, reqparse
from app_managers.kubernetes_manager import KubernetesManager
import os

kubernetes_parser = reqparse.RequestParser()
kubernetes_parser.add_argument('challenge', help='{error_msg}', type=dict, location='json')

km = KubernetesManager()
api = Namespace('kubernetes', description='Kubernetes related operations')

@api.route('/challenges/<string:challenge_id>')
class KubernetesDeploy(Resource):
    @api.doc('deploy_challenge')
    def post(self, challenge_id):
        args = kubernetes_parser.parse_args()
        try:
            if args['challenge']['action'] == "apply":
                km.setVariables(args['challenge']['clusterName'],args['challenge']['userName'],args['challenge']['action'],args['challenge']['emailAddress'])
                km.manageKubernetesCluster()
                km.manageKubernetesDns()
                km.manageKubernetesIngress()
                km.manageKubernetesStorage()
                km.manageKubernetesAuthentication()
                km.manageKubernetesServices()
            elif args['challenge']['action'] == "delete":
                km.setVariables(args['challenge']['clusterName'],args['challenge']['userName'],args['challenge']['action'],args['challenge']['emailAddress'])
                km.manageKubernetesServices()
                km.manageKubernetesAuthentication()
                km.manageKubernetesStorage()
                km.manageKubernetesIngress()
                km.manageKubernetesDns()
                km.manageKubernetesCluster()
            return "success", 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return "error", 404
