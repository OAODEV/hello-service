helloService
============

An example service project outlining our DevOps project setup

Clone this project with

    git clone git@github.com:OAODEV/helloService.git


The Service
-----------

The hello service runs a TCP server that says hello. The greeting is read from
the `greeting` envar. It will also say who it is from, taking the
environment name from the environment it's deployed in.

The service is contained in `app/serve_hello.py`. This file is heavily
documented, describing operations considerations.

The unit tests are in `test_hello_service.py`. This is nothing unusual
and has operations considerations documented.

The Operations Files
--------------------

The following files are required in the project root to hook into the
operations platform.

### Dockerfile

This is the file that developers use to create the contained service.
For the most part, that means creating the environment, installing
dependencies, putting files in place, setting envionment variables, and
so on. The platform will use this file to build the container and
provide that container with the command to run the service. The
Dockerfile in this project has more specific documentation.

More information on [docker containers](http://docs.docker.com/).

### Manifest

This file describes the services to herd, offering certain specifics
about the service, information the platform requires to work with it.
Details are documented in the Manifest file

Each `Dockerfile` must put the `Manifest` at `/Manifest` so that the
platform may access it in a known location.

    ADD Manifest /Manifest

### Version

This file simply holds the semantic version of the application at the commit. Fully optional.

### circle.yml

The configuration file for our CI Service. Just copy the file here into your
project root, then update the `herd_service_name` and `herd_unittest_cmd` lines
under `machine -> environment`

    machine:
      services:
        - docker
      environment:
        herd_service_name: <service name>
        herd_unittest_cmd: <unittest cmd>

The `unittest cmd` and `service name` should be the same as in the `Manifest`
file.

### Config file

This file is not part of the repository. It is passed to the configure command.
It should be a file with one `<key>=<value>` statement per line.

    message="Hello World."

# Iterating and Deploying with herd

## Clone the repo

    git clone git@github.com:OAODEV/hello-service.git
    cd hello-service

## Update tests and code

    echo "# `whoami` ran the tutorial on `date`\n" >> app/serve_hello.py
    git commit --am "adds importand comment"

## Integrate

For details on the herd command `integrate` see https://github.com/OAODEV/herd#integrate

    herd integrate

## Note the build name in CircleCI

This is currently a manual process. If the build passes, we go over to
[CircleCI](https://circleci.com/gh/OAODEV/hello-service), click into our build
then look for where it says

    echo "The build name is in here!!!" r.iadops.com/$herd_service_name:$herd_build_tag
    
It's in there and should look like this.

    r.iadops.com/hello:<semver>_build.<hash>

## Configure the Build

First create or locate a config file

    echo "greeting=<your personal greeting>" > hello.conf

Then use that to configure the build using the build name you noted earlier.
This will result in a Release.

    herd configure r.iadops.com/hello:<semver>_build.<hash> ./hello.conf

If this succeeds, it will print out the details of the Release that was created.
Note the release number.

## Deploy the release

    herd deploy <Release Number> <host[:port]>
