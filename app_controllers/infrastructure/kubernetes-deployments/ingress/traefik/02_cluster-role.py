import sys

def writeConfig(**kwargs):
    template = """
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: {serviceName}-{clusterName}-ingress-controller
rules:
  - apiGroups:
      - ""
    resources:
      - services
      - endpoints
      - secrets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - extensions
    resources:
      - ingresses
    verbs:
      - get
      - list
      - watch
---
# create Traefik service account
kind: ServiceAccount
apiVersion: v1
metadata:
  name: {serviceName}-{clusterName}-ingress-controller
  namespace: default
---
# bind role with service account
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: {serviceName}-{clusterName}-ingress-controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: {serviceName}-{clusterName}-ingress-controller
subjects:
- kind: ServiceAccount
  name: {serviceName}-{clusterName}-ingress-controller
  namespace: default
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/ingress/'+str(sys.argv[2])+'/02_cluster-role-'+str(sys.argv[1])+'-'+str(sys.argv[2])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]), serviceName=str(sys.argv[2]))