#!/usr/bin/env bash

apt-get update

# install key components
apt-get install -y python-pip python-dev

# install python modules
pip install virtualenv
#pip install flask requests uwsgi

#### For development, start the development server with debug
cd /vagrant
source venv/bin/activate
pip install -r requirements.txt
nohup python /vagrant/oracl.py &

#### Allow anyone to write to the data directory for the application
#### Better security would be nice, but this works
#### chmod -R 777 /vagrant/data


