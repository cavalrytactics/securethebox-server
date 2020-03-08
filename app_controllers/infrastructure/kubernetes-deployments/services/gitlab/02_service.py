import sys

def writeConfig(**kwargs):
    template = """
apiVersion: v1
kind: Service
metadata:
  name: {serviceName}-{userName}
  annotations:
    external-dns.alpha.kubernetes.io/hostname: {serviceName}-{userName}.{clusterName}.securethebox.us
spec:
  selector:
    app: {serviceName}-{userName}
  ports:
    - name: http
      targetPort: 80
      port: 80
    - name: https
      targetPort: 443
      port: 443
    - name: ssh
      targetPort: 22
      port: 2222
  type: LoadBalancer
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/services/'+str(sys.argv[2])+'/02_service-'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))