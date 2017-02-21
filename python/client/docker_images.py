from .docker_client import MyDockerClient


class MyDockerImage(MyDockerClient):
    """
    This class is not required at all. I created this for organization of thoughts and some hierarchy of docker client
    resources i.e. start with client, then get images, containers, volumes, networks etc. We could as well directly
    use the handle to docker client and not have this abstraction in between. Its a choice
    """
    def __init__(self,client):
        assert (client is not None)
        self.client = client

    def images(self):
        return self.client.images
