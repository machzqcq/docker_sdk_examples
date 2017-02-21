from python.client import *
import configparser

"""
Read config from client
"""
conf = configparser.RawConfigParser()
conf.read('../config/.env')

"""
Initialize MyDockerClient
"""
myclient = MyDockerClient(conf).client

"""
Initialize MyDockerImage
"""

myimages = MyDockerImage(myclient).images()

for image in myimages.list():
    print(image.id)
