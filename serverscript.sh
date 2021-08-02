#! /bin/bash

apt update
apt install python3 python3-pip -y
pip3 install --upgrade pip
pip3 install flwr

echo "import flwr as fl
fl.server.start_server(config={\"num_rounds\": 3})" >> server.py

python3 server.py
