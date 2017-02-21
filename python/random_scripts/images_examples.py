import docker, os
import configparser

# Read Docker Daemon environment values
config = configparser.RawConfigParser()
config.read('../config/.env')

# Set Environment variables. I created a docer-machine with name node1
os.environ['DOCKER_HOST'] = config.get('docker-machine-node1', 'DOCKER_HOST')
os.environ['DOCKER_TLS_VERIFY'] = config.get('docker-machine-node1', 'DOCKER_TLS_VERIFY')
os.environ['DOCKER_CERT_PATH'] = config.get('docker-machine-node1', 'DOCKER_CERT_PATH')
client = docker.from_env()

# List all images
print("Initial image list")
for image in client.images.list():
    print(image.id)


# Pull an image
image = client.images.pull('alpine:latest')
print("Image:", image.id, " successfully pulled")
print("Image tags:")
print(image.tags)
