#!/bin/bash
set -e
if [ -n "$VPS_IP" ] && [ -n "$VPS_USER" ]; then
    gcc -O3 -pthread -o bgmi bgmi.c
    tar -czf deploy.tar.gz app.py bgmi requirements.txt
    scp deploy.tar.gz $VPS_USER@$VPS_IP:/tmp/
    ssh $VPS_USER@$VPS_IP 'cd /opt/bgmi && tar -xzf /tmp/deploy.tar.gz && pip3 install flask && pkill -f "python3 app.py" || true && nohup python3 app.py &'
fi
