import sys

def writeConfig(**kwargs):
    template = """
kind: ConfigMap
apiVersion: v1
metadata:
  name: traefik-config
  namespace: default
data:
  traefik.toml: |
    defaultEntryPoints = ["http"]
    [entryPoints]
      [entryPoints.http]
        address = ":80"
      [entryPoints.http.auth.forward]
        address = "http://auth"
        authResponseHeaders = ["X-Forwarded-User"]
    [kubernetes]
    [respondingTimeouts]
      idleTimeout = "620s"
              """

    with open('./app_controllers/infrastructure/kubernetes-deployments/ingress/'+str(sys.argv[2])+'/03_config-'+str(sys.argv[1])+'-'+str(sys.argv[2])+'.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]), serviceName=str(sys.argv[2]))