from fabric.api import *

env.hosts = ['104.130.3.209']

#@TODO move this configuration into project config files
service_name = "hello"
registry_host = "104.130.3.209:5000"
unittest_cmd = "python test.py"
acceptance_cmd = "python accept.py"

def integrate(build_name=None):
    #@TODO document correct method for pulling the repo initially to
    #@TODO get hub and mainline pointed correctly
    if not build_name:
        build_name = local("git rev-parse HEAD", capture=True)[:7]
    else:
        local("git tag {tag}".format(tag=build_name))
        local("git push -f hub {tag}".format(tag=build_name)
    image_name = "{}/{}_{}".format(registry_host, service_name, build_name)
    local("git pull hub mainline")
    build(image_name)
    test(image_name)
    local("git push hub mainline")
    local("docker push {image_name}".format(image_name=image_name))
    #@TODO trigger CI build and acceptance test

def build(image_name):
    local("docker build -t {image_name} .".format(image_name=image_name))

def test(image_name):
    local("docker run {image_name} {cmd}".format(
                image_name=image_name, cmd=unittest_cmd))

def run_image_on_port(runner, image_name, port):
    test(image_name)
    runner("docker run -p {port}:8000 -i -t -d {image_name}".format(
            port=port, image_name=image_name))

def deploy_local(image_name, port):
    build(image_name)
    run_image_on_port(local, image_name, port)

def deploy(image_name, port):
    run("docker pull {image_name}".format(image_name=image_name))
    run_image_on_port(run, image_name, port)
