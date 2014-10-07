helloService
============

An example service project outlining our DevOps setup

Clone this project with `git clone -o hub -b mainline git@github.com:OAODEV/helloService.git`

The Service
-----------

The hello service runs a TCP server that says hello. it identifys it's
hostname or claiming to be anonymous if there is no hostname.

The service is contained in `app/serve_hello.py`. This file is heavily
documented describing operations considerations.

The unit tests are in `test_hello_service.py`. This is nothing unusual
and has operations considerations documented.

The Operations Files
--------------------

The project root needs the following files in order to hook into the
operations platform.

### Dockerfile

This is the file that developers use to create the contained service.
For the most part, that means creating the environment, installing
depandencies, putting files in place, setting envionment veriables and
so on. The platform will use this file to build the container and
provide that container with the command to run the service. The
Dockerfile has more specific documentation.

more information on docker http://docs.docker.com/

### Manifest

This file describes to the operations platform certain specifics about
the service that the platform needs in order to work with it. Details
are documented in the Manifest file

### fabfile.py

This file provides the automation that runs the different development
tasks in a way that is compatible with the operations platform. It is
the entrypoint to the platform.

### Vagrantfile

This file describes how to create the VM we use to run docker on the
development laptops. This file should not change very frequently if at
all

### bootstrap.sh

The `Vagrantfile` runs bootstrap.sh to set up the VM. This won't change
frequently if at all either.

*both `vagrantfile` and `bootstrap.sh` only set up a local VM for the
purpose of running docker. Nothing about the VM environment will be
relevant to the resulting container environment.*
