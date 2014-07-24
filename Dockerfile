from ubuntu:14.04
maintainer jmiller@adops.com

run sudo apt-get update
run sudo apt-get install -y python

add app /app

workdir /app
cmd python hello.py
