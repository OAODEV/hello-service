from fabric.api import *

env.hosts = ['104.130.3.209']

def build(image):
    local("docker build -t {image} .".format(image=image))

def test(image):
    local("docker run {image} python test.py".format(image=image))

def run_image_on_port(runner, image, port):
    test(image)
    runner("docker run -p {port}:8000 -i -t -d {image}".format(port=port,
                                                               image=image
                                                               ))

def deploy_local(image, port):
    run_image_on_port(local, image, port)

def deploy(image, port):
    build(image)
    test(image)
    local("docker push {image}".format(image=image))
    run("docker pull {image}".format(image=image))
    run_image_on_port(run, image, port)
