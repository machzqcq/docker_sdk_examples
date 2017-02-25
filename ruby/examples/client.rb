#https://github.com/swipely/docker-api
require 'docker'

Docker.url = 'tcp://192.168.99.103:2376'
CERT_PATH = "/Users/pmacharl/.docker/machine/machines/node1"
Docker.options = {
    client_cert: File.join(CERT_PATH, 'cert.pem'),
    client_key: File.join(CERT_PATH, 'key.pem'),
    ssl_ca_file: File.join(CERT_PATH, 'ca.pem'),
    scheme: 'https'
}

puts Docker.version
puts Docker.info

