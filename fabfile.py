import urllib
from ConfigParser import ConfigParser

from fabric.api import *

manifest = ConfigParser()
manifest.read('Manifest')

service_name = manifest.get('Service', 'name')
unittest_cmd = manifest.get('Service', 'unittest_cmd')
accept_cmd = manifest.get('Service', 'accept_cmd')
sanity_cmd = manifest.get('Service', 'sanity_cmd')

service_port = manifest.get('Service', 'service_port')
docs_port = manifest.get('Service', 'docs_port')
coverage_port = manifest.get('Service', 'coverage_port')

registry_host_addr = '104.130.3.209:5000'
accept_host_addr = '104.130.3.209:5001'

REGISTRY_HOST = registry_host_addr.split(':')[0]
REGISTRY_PORT = registry_host_addr.split(':')[1]
ACCEPT_HOST = accept_host_addr.split(':')[0]
ACCEPT_PORT = accept_host_addr.split(':')[1]

def up():
    local('vagrant up')

def down():
    local('vagrant destroy')

def test(build_name=None):
    image_name = make_image_name(build_name)
    build(image_name)
    vagrant("docker run {image_name} {cmd}".format(
                image_name=image_name, cmd=unittest_cmd))

def accept(build_name=None):
    image_name = make_image_name(build_name)
    build(image_name)
    vagrant("docker run -d -p 127.0.0.1:{}:{} {}".format(
        service_port, service_port, image_name))
    try:
        vagrant(accept_cmd)
    except Exception, e:
        raise e
    finally:
        vagrant("docker stop `docker ps -q`")
        vagrant("docker rm `docker ps -aq`")

def integrate(build_name=None):

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

    # trigger the build server for this image
    image_name = make_image_name(build_name)
    vagrant("docker push {image_name}".format(image_name=image_name))
    accept_trigger = "curl localhost:{}/{}?{}".format(ACCEPT_PORT,
                                                      urllib.quote(image_name),
                                                      urllib.quote(accept_cmd),
                                                      )
    with settings(host_string=ACCEPT_HOST):
        run(accept_trigger)

def deploy_local(image_name, port):
    build(image_name)
    run_image_on_port(vagrant, image_name, port)

def deploy(image_name, port):
    with settings(host_string=app_host):
        run("docker pull {image_name}".format(image_name=image_name))
        run_image_on_port(run, image_name, port)

def build(image_name):
    vagrant("docker build -t {image_name} .".format(image_name=image_name))

def run_image_on_port(runner, image_name, port):
    test(image_name)
    runner("docker run -p {port}:{docker_port} -i -t -d {image_name}".format(
            port=port, docker_port=exposed_port, image_name=image_name))

def make_image_name(build_name):
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
    local("vagrant ssh -c 'cd /vagrant && {}'".format(cmd))
