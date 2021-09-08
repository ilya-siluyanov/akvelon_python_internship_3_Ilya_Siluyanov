#!/bin/bash

# A script only for Heroku server

cd src
sudo apt update && sudo apt -y upgrade
sudo apt install -y python3-dev docker docker-compose
#execute command launching services
docker-compose up
