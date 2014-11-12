import os
import urllib2
from ConfigParser import ConfigParser
from fabric.api import *

env.use_ssh_config = True

manifest = ConfigParser()
manifest.read('Manifest')

service_name = manifest.get('Service', 'name')
unittest_cmd = manifest.get('Service', 'unittest_cmd')
accept_cmd = manifest.get('Service', 'accept_cmd')
service_port = manifest.get('Service', 'service_port')

registry_host_addr = 'r.iadops.com'

def up():
    """ Bring up the local dev environment """
    local('vagrant up')

def down():
    """ Destroy the local dev environment """
    local('vagrant destroy')

def ssh(build_name=None):
    """ start the container and drop the user into a shell """
    image_name = make_image_name(build_name)
    vagrant("docker run -i -t {} /bin/bash".format(image_name))

def test(command=unittest_cmd, build_name=None):
    """ Run the unit tests in a local build """
    image_name = make_image_name(build_name)
    build(image_name)
    vagrant("docker run {image_name} {cmd}".format(
                image_name=image_name, cmd=command))

def accept(build_name=None):
    """ Run the accpetance tests in a local build """
    test(accept_cmd)

def integrate(build_name=None):
    """
    Run the continuous integration workflow

    1. Pull in any new mainline changes
    2. Pull in any new current branch changese
    3. Build locally and test
    4. Push local code changes to remote hub repo (current branch)
    5. Push image to docker index

    """

    # Merge any new mainline changes
    local("git pull hub mainline")

    # Merge any new current branch changes
    branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
    if branch != 'mainline':
        # if the remote exists, pull it
        with settings(warn_only=True):
            local("git pull hub {}".format(branch))

    # build and test
    test(build_name)

    # push passed code changes to current branch
    local("git push -u hub {}".format(branch))

    # push passed image to the docker index
    image_name = make_image_name(build_name)
    vagrant("docker push {image_name}".format(image_name=image_name))

    with settings(host_string='r.iadops.com'):
        run("curl localhost:5001/{}?{}".format(image_name, accept_command))

    if os.path.exists("./success_art.txt"):
        with open("./success_art.txt", 'r') as art:
            print art.read()


def deploy(host, port):
    """
    deploy the service

    host: the url or ip of the machine to run the service on
    port: the port on the host to bind the service to

    """

    print "* Deploying to {}:{}".format(host, port)

    image_name = make_image_name(None)

    build(image_name)
    vagrant("docker push {image_name}".format(image_name=image_name))

    with settings(host_string=host):
        run("docker run -d -p {port}:{docker_port} {image_name}".format(
            port=port, docker_port=service_port, image_name=image_name))

    print "* {} is now available at {}:{}".format(service_name ,host, port)

def build(image_name):
    """ build the Dockerfile with the given name """
    local("vagrant ssh -c 'docker build -t {image_name} /vagrant'".format(
        image_name=image_name))

def clean():
    """ remove all docker images and containers from the vagrant env """
    vagrant("docker stop `docker ps -aq`")
    vagrant("docker rm `docker ps -aq`")
    vagrant("docker rmi `docker images -aq`")
    print "Environment clean of old docker artifacts."

def make_image_name(build_name=''):
    """
    make an image name based on the given build name and current git state

    """

    # ensure that the name of the resulting image matches the git
    # checkout in either the commit hash or a tag
    if not build_name:
        # if we are not naming the build, infer a name for the image
        # from the git commit hash
        build_name = local("git rev-parse HEAD", capture=True)[:7]
    else:
        # if we are naming the build make sure we are tagging the git
        # commit with the name we have chosen
        local("git tag -f {tag}".format(tag=build_name))
        local("git push -f hub {tag}".format(tag=build_name))

    image_name = "{}/{}_{}:testing".format(registry_host_addr,
                                           service_name,
                                           build_name)

    return image_name

def vagrant(cmd):
    """ send a command to the vagrant box """
    local("vagrant ssh -c '{}'".format(cmd))
