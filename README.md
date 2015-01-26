helloService
============

An example service project outlining our DevOps setup

Clone this project with

    git clone -o hub -b mainline git@github.com:OAODEV/helloService.git

Update common ops files by running this command in the project root.

    curl https://gist.githubusercontent.com/oaojesse/2320739caf2e4c735542/raw/78b97c71db858862e2dcad7b326063063f000644/update_common.sh | sh

In order to work with the operations platform developers need to install [Fabric](http://www.fabfile.org/installing.html).

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
Dockerfile has more specific documentation.

More information on [docker containers](http://docs.docker.com/).

### Manifest

This file describes to the operations platform certain specifics about
the service that the platform needs in order to work with it. Details
are documented in the Manifest file

Each `Dockerfile` must put the `Manifest` at `/Manifest` so that the
platform may access it in a known location.

### fabfile.py

This file provides the automation that runs the different development
tasks in a way that is compatible with the operations platform. It is
the entry point to the platform.

### Config file

This file is not part of the repository. It is passed to the deploy command and
specifies the message that this helloService should send.

    [Config]
    message="Hello World."