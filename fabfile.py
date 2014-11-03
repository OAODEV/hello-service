import os
from ConfigParser import ConfigParser
from fabric.api import *

env.use_ssh_config = True

manifest = ConfigParser()
manifest.read('Manifest')

service_name = manifest.get('Service', 'name')
unittest_cmd = manifest.get('Service', 'unittest_cmd')
service_port = manifest.get('Service', 'service_port')

registry_host_addr = 'r.iadops.com'

registry_cert = """
-----BEGIN CERTIFICATE-----
MIID7TCCAtWgAwIBAgIJAO/As4eaf7Q6MA0GCSqGSIb3DQEBCwUAMIGMMQswCQYD
VQQGEwJVUzERMA8GA1UECAwITmV3IFlvcmsxETAPBgNVBAcMCE5ldyBZb3JrMQww
CgYDVQQKDANPQU8xDzANBgNVBAsMBkJUU0RFVjEVMBMGA1UEAwwMci5pYWRvcHMu
Y29tMSEwHwYJKoZIhvcNAQkBFhJqbWlsbGVyQGlhZG9wcy5jb20wHhcNMTQxMTAz
MTc0MzIyWhcNMTUxMTAzMTc0MzIyWjCBjDELMAkGA1UEBhMCVVMxETAPBgNVBAgM
CE5ldyBZb3JrMREwDwYDVQQHDAhOZXcgWW9yazEMMAoGA1UECgwDT0FPMQ8wDQYD
VQQLDAZCVFNERVYxFTATBgNVBAMMDHIuaWFkb3BzLmNvbTEhMB8GCSqGSIb3DQEJ
ARYSam1pbGxlckBpYWRvcHMuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEArfCOIOdG7UodiPGQdOsfyILnvTKjH3+YEmwOLIENbI50kDcs9tav/AC5
GwPT+IblrhcmmJX0DeVPXzBf7FNweCl1r5bkabc9gnUPIHDSObC/ej3r7/+gF6bF
qbJDqM/3QX/ePx8hhsnmb8n7NGF9lfSlMvxp2F9RFuxL29sXvt4tLrZZj1B/VBzg
yHcZt5UGhK+1CNQsvPbY1S852RBacSMP3X34v74w9G6GEepI5dpQQ4PHQiAqBPeE
27wqYBKBcsbzAWcSRLXFhf/w4AFMsOJUaPNLkfRsO93/P2OsDX95O+oAnDEDsZMV
PQJs52Ky3/yAp5aJZZ/FtHvg9aYr4wIDAQABo1AwTjAdBgNVHQ4EFgQUCi3oa93J
xGSTxImMIQWFBhPjkA0wHwYDVR0jBBgwFoAUCi3oa93JxGSTxImMIQWFBhPjkA0w
DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAZzJ9vlTQJRtjpTrMMQ9f
0vnTIbPHg4/Nk1Em7XO3GdDZ89mSv1sPS9X/meWpCzm2+2yBR2+rSoQbQfI7NgjX
rjFsvb6mcaNpja+kC6xlMCTu5mP5hLxAWCZNtBHYJ/btObq1A/4kofhlUSRN6hqH
WFWAA5xKyll1rZSP5ZvyIokQbZWuJLe5v53K4hv5MCnAIOi1PQbpUwMNebU+fP9v
H3gz4vWuBn8XFWPjlDUmF6UzquI+Qjyqz4FUq3XRdb0pc2V4JCvpzJhjPkVb2ZiS
6Dxh5QX1XKXPuz3g4roeBIzSb1Cd8nGleVnE4I2zXaQVJH3qXJKueBqUj24ER0GI
ZA==
-----END CERTIFICATE-----
"""

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

def test(build_name=None):
    """ Run the unit tests in a local build """
    image_name = make_image_name(build_name)
    build(image_name)
    vagrant("docker run {image_name} {cmd}".format(
                image_name=image_name, cmd=unittest_cmd))

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

    # install registry cert
    cert_folder = "/etc/docker/certs.d/r.iadops.com"
    vagrant("mkdir -p {}".format(cert_folder))
    vagrant("echo '{}' > {}/ca.crt".format(registry_cert, cert_folder))

    # push passed image to the docker index
    image_name = make_image_name(build_name)
    vagrant("docker push {image_name}".format(image_name=image_name))

    if os.path.exists("./success_art.txt"):
        with open("./success_art.txt", 'r') as art:
            print art.read()

    #TODO trigger acceptance testing in the Build server

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
