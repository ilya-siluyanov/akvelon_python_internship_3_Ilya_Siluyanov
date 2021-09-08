#!/bin/bash

# A script only for Heroku server

cd src
python3 manage.py makemigrations && python3 manage.py migrate
apt update && apt -y upgrade
apt install -y python3-dev docker docker-compose
#execute command launching services
docker-compose up
