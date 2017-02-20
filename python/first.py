import docker, os
import ConfigParser

# Read Docker Daemon environment values
config = ConfigParser.RawConfigParser()
config.read('.env')

# Set Environment variables. I created a docer-machine with name node1
os.environ['DOCKER_HOST'] = config.get('docker-machine-node1','DOCKER_HOST')
os.environ['DOCKER_TLS_VERIFY'] = config.get('docker-machine-node1','DOCKER_TLS_VERIFY')
os.environ['DOCKER_CERT_PATH'] = config.get('docker-machine-node1','DOCKER_CERT_PATH')
client = docker.from_env()

# Print output of running container
print client.containers.run("alpine", ["echo", "hello", "world"])

# List all containers & remove
for container in client.containers.list(all=True):
  print container.name
  container.remove()

# List all images
for image in client.images.list():
  print image.id

# Remove all containers
