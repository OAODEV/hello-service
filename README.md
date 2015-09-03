helloService
============

An example service project outlining our DevOps project setup

Clone this project with

    git clone -o hub -b mainline git@github.com:OAODEV/helloService.git


The Service
-----------

The hello service runs a TCP server that says hello. The greeting is readfrom
the `greeting` envar. It will also say who it is from, taking the
environment name form the environment it's deployed in.

The service is contained in `app/serve_hello.py`. This file is heavily
documented describing operations considerations.

The unit tests are in `test_hello_service.py`. This is nothing unusual
and has operations considerations documented.

The Operations Files
--------------------

The project root needs the following files in the project root to hook into the
operations platform.

### Dockerfile

This is the file that developers use to create the contained service.
For the most part, that means creating the environment, installing
depandencies, putting files in place, setting envionment veriables and
so on. The platform will use this file to build the container and
provide that container with the command to run the service. The
Dockerfile in this project has more specific documentation.

More information on [docker containers](http://docs.docker.com/).

### Manifest

This file describes to the operations platform certain specifics about
the service that the platform needs in order to work with it. Details
are documented in the Manifest file

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
      environmnet:
        herd_service_name: <service name>
        herd_unittest_cmd: <unittest cmd>

The `unittest cmd` and `service name` should be the same as in the `Manifest`
file.

### Config file

This file is not part of the repository. It is passed to the deploy command and
for this project specifies the message that this helloService should send.

    [Config]
    message="Hello World."
