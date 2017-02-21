from python.client import *
import configparser

conf = configparser.RawConfigParser()
conf.read('../config/.env')

myclient = MyDockerClient(conf).client
print(myclient.containers.run("alpine", ["echo", "hello", "world"]))

# List all containers & remove
for container in myclient.containers.list(all=True):
  print(container.name)
  container.remove()

# List all images
for image in myclient.images.list():
  print(image.id)

# List networks
for network in myclient.networks.list():
    print("Network ID --> Name")
    print(network.id, "-->", network.name)

# List volumes

for volume in myclient.volumes.list():
    print("Volume ID --> Name")
    print(volume.id,"-->", volume.name)