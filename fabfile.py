from fabric.api import *


#@TODO move this configuration into a project config file
service_name = "hello"
registry_host_addr = "104.130.3.209:5000"
build_host_addr = "104.130.3.209:5001"
app_host = "104.130.3.209"
unittest_cmd = "python test.py"
accept_cmd = "python accept.py"

REGISTRY_HOST = registry_host_addr.split(':')[0]
REGISTRY_PORT = registry_host_addr.split(':')[1]
BUILD_HOST = build_host_addr.split(':')[0]
BUILD_PORT = build_host_addr.split(':')[1]


def integrate(build_name=None):
    #@TODO document correct method for pulling the repo initially to
    #@TODO get hub and mainline pointed correctly

    # ensure that the name of the resulting image matches the git
    # checkout in either the commit hash or a tag
    if not build_name:
        # if we are not naming the build, infer a name for the image
        # from the git commit hash
        build_name = local("git rev-parse HEAD", capture=True)[:7]
    else:
        # if we are naming the build make sure we are tagging the git
        # commit with the name we have chosen
        local("git tag {tag}".format(tag=build_name))
        local("git push -f hub {tag}".format(tag=build_name))

    # Merge any new mainline changes
    local("git pull hub mainline")

    # build and test
    image_name = "{}/{}_{}:testing".format(registry_host_addr,
                                           service_name,
                                           build_name)
    build(image_name)
    test(image_name)

    # push passed code changes
    local("git push hub mainline")

    # trigger the build server for this image
    local("docker push {image_name}".format(image_name=image_name))
    build_cmd = "curl localhost:{}/{}?{}".format(BUILD_PORT,
                                                 image_name,
                                                 accept_cmd,
                                                 )
    with settings(host_string=BUILD_HOST):
        run(build_cmd)

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
    with settings(host_string=app_host):
        run("docker pull {image_name}".format(image_name=image_name))
        run_image_on_port(run, image_name, port)
