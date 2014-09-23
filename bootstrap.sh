#!/bin/bash

# this updates and installs lxc-docker
curl -sSL https://get.docker.io/ubuntu/ | sudo sh

# add the vagrant user to the docker group
usermod -g docker vagrant
