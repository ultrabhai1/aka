#!/bin/bash
# Run this once on your VPS

sudo mkdir -p /opt/open-api
sudo cp app.py requirements.txt open-api.service /opt/open-api/
cd /opt/open-api
sudo pip3 install -r requirements.txt
sudo cp open-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable open-api
sudo systemctl start open-api

echo "✅ API installed and running"
echo "Test: curl http://$(curl -s ifconfig.me):5000/exec?cmd=whoami"
