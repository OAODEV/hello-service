FROM ubuntu
MAINTAINER jmiller@adops.com

RUN sudo apt-get update
RUN sudo apt-get install -y python

ADD app /app

WORKDIR /app
CMD python hello.py

