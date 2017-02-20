import docker, os


tls_config = docker.tls.TLSConfig(ca_cert='/Users/pmacharl/.docker/machine/machines/node1/ca.pem',
                                  client_cert=('/Users/pmacharl/.docker/machine/machines/node1/cert.pem',
                                               '/Users/pmacharl/.docker/machine/machines/node1/key.pem'))
client = docker.DockerClient(base_url='https://192.168.99.100:2376', tls=tls_config)

# If InsecureRequestWarning is thrown, fix it using - https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
# It is not an error, just a warning - that needs to be fixed in production

# Print output of running container
print client.containers.run("alpine", ["echo", "hello", "world"])

# List all containers & remove
for container in client.containers.list(all=True):
  print container.name
  container.remove()

# List all images
for image in client.images.list():
  print image.id

