import docker, os

class MyDockerClient(object):
    'Any class attributes goes here'

    def __init__(self, config, node):
        # Set Environment variables. I created a docer-machine with name node1
        os.environ['DOCKER_HOST'] = config.get(node, 'DOCKER_HOST')
        os.environ['DOCKER_TLS_VERIFY'] = config.get(node, 'DOCKER_TLS_VERIFY')
        os.environ['DOCKER_CERT_PATH'] = config.get(node, 'DOCKER_CERT_PATH')
        self.client = docker.from_env()

    def client(self):
        return self.client


