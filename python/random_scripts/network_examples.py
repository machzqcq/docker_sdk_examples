import docker, os
import configparser,time
from flatten_json import flatten


# Read Docker Daemon environment values
config = configparser.RawConfigParser()
config.read('../config/.env')

# Set Environment variables. I created a docer-machine with name node1
os.environ['DOCKER_HOST'] = config.get('docker-machine-node1', 'DOCKER_HOST')
os.environ['DOCKER_TLS_VERIFY'] = config.get('docker-machine-node1', 'DOCKER_TLS_VERIFY')
os.environ['DOCKER_CERT_PATH'] = config.get('docker-machine-node1', 'DOCKER_CERT_PATH')
client = docker.from_env()

# List networks
for network in client.networks.list():
    print("ID:",network.id," name:",network.name," attrs:",network.attrs)

# Create a bridge network
mynetwork = client.networks.create("network1", driver="bridge")

# Create a container and join this container to mynetwork
mycontainer = client.containers.run("alpine", ["ping","8.8.8.8"], detach=True)
mynetwork.connect(mycontainer)
# Bug in api - unless reload() is called - the ip address is not showing up - https://github.com/docker/docker-py/issues/1375
mycontainer.reload()
print(mycontainer.attrs)
flattened_json = flatten(mycontainer.attrs)
print("Network1 assigned IP:",flattened_json['NetworkSettings_Networks_network1_IPAddress'])



#Disconnect container from network
mynetwork.disconnect(mycontainer)

# Remove all containers
for container in client.containers.list(all=True):
  if container.status == 'running':
      container.kill() #container.stop() is resulting in urllib3 socket timeout
  container.remove()

# Remove the network
mynetwork.remove()

# List networks
for network in client.networks.list():
    print("ID:",network.id," name:",network.name," attrs:",network.attrs)



