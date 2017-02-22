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

# Run a container

print(client.containers.run("alpine", ["echo", "hello", "world"]))

mycontainer = client.containers.run("alpine", ["echo", "hello", "world"], detach=True)
print(mycontainer.logs())

# Prune containers - Bug https://github.com/docker/docker-py/issues/1475 (fixed), client = docker.from_env(version='1.25')
# pruned_container_ids = client.containers.prune()
# print(pruned_container_ids)

client.containers.run("alpine", ["ping","8.8.8.8"], detach=True)


#List all containers & remove
for container in client.containers.list(all=True):
  print("Name:",container.name," Short_ID:",container.short_id," status:",container.status)
  print("Attrs:", container.attrs)
  if container.status == 'running':
      container.kill() #container.stop() is resulting in urllib3 socket timeout
  container.remove()

# Stream stats. stats() returns a generator and we can call next(generator) until it raises StopIteration exception
# The below code doesn't exit by itself , you have to SIGTERM or SIGKILL
# mycontainer = client.containers.run("alpine", ["ping","8.8.8.8"], detach=True)
# stats_stream = mycontainer.stats(decode=True)
# for item in stats_stream:
#     print(item)

# Top command
mycontainer = client.containers.run("alpine", ["ping","8.8.8.8"], detach=True)
print(mycontainer.top(ps_args='aux'))


