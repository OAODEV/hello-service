FROM ubuntu:14.04
MAINTAINER jmiller@adops.com

RUN sudo apt-get update
RUN sudo apt-get install -y python python-pip git
RUN pip install mock

# eventually install this from an internal server that is exposed
# by deploying the library.
RUN pip install git+git://104.130.3.209:9000/

ADD . /app

WORKDIR /app/app
CMD python serve_hello.py
