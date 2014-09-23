FROM ubuntu:14.04
MAINTAINER jmiller@adops.com

RUN sudo apt-get update
RUN sudo apt-get install -y python python-pip git

# eventually install this from an internal server that is exposed
# by deploying the library.
RUN pip install git+https://github.com/OAODEV/hellolib.git

ADD . /app

WORKDIR /app/app
CMD python serve_hello.py
