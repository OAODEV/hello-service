import os
import time
import urllib
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
build_host_addr = 'qa.iadops.com'

def ssh(build_name=None):
    """ start the container and drop the user into a shell """
    image_name = make_image_name(build_name)
    on_build_host("docker run -i -t {} /bin/bash".format(image_name))

def test(build_name=None, command=unittest_cmd):
    """ Run the unit tests in a local build """
    image_name = make_image_name(build_name)
    build(image_name)
    on_build_host("docker run {image_name} {cmd}".format(
                image_name=image_name, cmd=command))

def accept(build_name=None):
    """ Run the accpetance tests in a local build """
    test(command=accept_cmd)

def integrate(build_name=None):
    """
    Run the continuous integration workflow

    1. Pull in any new mainline changes
    2. Pull in any new current branch changese
    3. Build locally and test
    4. Push local code changes to remote hub repo (current branch)
    5. Push image to docker index

    """

    # fetch remote branch references and deletes outdated remote branch names
    local("git remote update --prune hub")

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
    on_build_host("docker push {image_name}".format(image_name=image_name))

    with settings(host_string=registry_host_addr):
        run("curl localhost:5001/{}?{}".format(image_name,
                                               urllib.quote(accept_cmd)))

    if os.path.exists("./success_art.txt"):
        with open("./success_art.txt", 'r') as art:
            print art.read()

def deploy(host, port):
    """
    deploy the service

    We deploy releases.
    A release is the code tracked in github plus config. Therefore it should
    have a name that differentiates it from a build, which for now is only used
    for testing.

    host: the url or ip of the machine to run the service on
    port: the port on the host to bind the service to

    """

    print "* Deploying to {}:{}".format(host, port)

    release_name = "release_{}".format(time.time())
    image_name = make_image_name(release_name)

    build(image_name)
    on_build_host("docker push {}".format(image_name))

    with settings(host_string=host):
        run("docker run -d -p {port}:{docker_port} {image_name}".format(
            port=port, docker_port=service_port, image_name=image_name))

    print "* {} is now available at {}:{}".format(service_name ,host, port)

def build(image_name):
    """ build the Dockerfile with the given name

        Once we have environment management built into the system we will be
        able to build services from only things that are git tracked, but for
        now we need to build them from whatever happens to be in the current
        repo to allow us to add configuration files to the containers we build

        When all configuration is read from environment varriables and is set up
        at runtime this can change and become more streamlined.

    """

    # copy current project directory to the build server

    build_path = "/build/{}/{}".format(env.user, service_name)
    on_build_host("mkdir -p {}".format(build_path))

    # ignore .git folder in rsync command

    local("rsync -rlvz --exclude .git -e ssh --delete ./ {}:{}".format(
        build_host_addr, build_path))

    on_build_host("docker build -t {} {}".format(
        image_name, build_path))

def clean():
    """ remove all docker images and containers from the vagrant env """
    on_build_host("docker rm `docker ps -aq`")
    on_build_host("docker rmi `docker images -aq`")
    print "Environment clean of stopped docker artifacts."

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

def on_build_host(cmd):
    """ send a command to the remote build machine with docker installed """
    with settings(host_string=build_host_addr):
        run(cmd)
