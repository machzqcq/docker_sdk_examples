from python.client import *
import configparser,subprocess,re

"""
Create 3 VM nodes - I used docker-machine to create 3 as below at bash prompt
# for i in 1 2 3; docker-machine create --virtualbox node$i;done
Node1, Node2 and Node3. I intend to make Node1 as manager and others workers
Read this for concepts - https://github.com/machzqcq/docker-orchestration
"""
conf = configparser.RawConfigParser()
conf.read('../config/.env')

# In case you want to assert the values. Note: If you are using virtualenv, then the below will not locate docker-machine binary
# node1_ip = subprocess.getoutput("docker-machine ip node1")
# assert str(node1_ip) in conf.get('docker-machine-node1','DOCKER_HOST')
# node2_ip = subprocess.getoutput('docker-machine ip node2')
# assert str(node2_ip) in conf.get('docker-machine-node2','DOCKER_HOST')
# node3_ip = subprocess.getoutput('docker-machine ip node3')
# assert str(node3_ip) in conf.get('docker-machine-node3','DOCKER_HOST')

node1_client = MyDockerClient(conf, 'docker-machine-node1').client
node2_client = MyDockerClient(conf, 'docker-machine-node2').client
node3_client = MyDockerClient(conf, 'docker-machine-node3').client

# Initialize a swarm and leave it. If the node is already part of swarm, then try, except to handle it properly
# try:
#     node1_client.swarm.init(
#         advertise_addr='eth1', listen_addr='0.0.0.0:2377',
#         force_new_cluster=False, snapshot_interval=5000,
#         log_entries_for_slow_followers=1200
#     )
# except Exception as err:
#     print("OS error: {0}".format(err))
#     print(type(err))
#     print(err.args)
#

# eth1 instead of eth0 , becuase the 192.x address was assigned by virtual box and that is what docker-machine has
node1_client.swarm.init(
    advertise_addr='eth1', listen_addr='0.0.0.0:2377',
    force_new_cluster=True, snapshot_interval=5000,
    log_entries_for_slow_followers=1200
)
swarm_attrs = node1_client.swarm.attrs
manager_token = swarm_attrs['JoinTokens']['Manager']
worker_token = swarm_attrs['JoinTokens']['Worker']

# Join Node2 as worker
node2_client.swarm.join(remote_addrs=["192.168.99.103:2377"],join_token=worker_token,
                        advertise_addr='eth1',listen_addr='0.0.0.0:2377')

# Join Node3 as Worker
node3_client.swarm.join(remote_addrs=["192.168.99.103:2377"], join_token=worker_token,
                        advertise_addr='eth1', listen_addr='0.0.0.0:2377')
print(node1_client.swarm.attrs)

# List nodes
for node in node1_client.nodes.list():
    print("NodeID,Attributes\n")
    print("{0},{1}".format(node.id, node.attrs))

# List only worker nodes

for node in node1_client.nodes.list(filters={'role': 'worker'}):
    print("NodeID,Attributes\n")
    print("{0},{1}".format(node.id, node.attrs))

# force=True needed for manager to leave the swarm
node2_client.swarm.leave()
node3_client.swarm.leave()
node1_client.swarm.leave(force=True)
print(node1_client.swarm.attrs)

# Note: Bad things can really happen if swarm enters a dangling state. In fact my VM's lost docker-engine state too
# The docker-machine provisioner got corrupted - hence I had to docker-machine provision node1 (to re-provision)


