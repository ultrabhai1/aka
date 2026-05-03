#!/bin/bash
set -e

echo "🚀 Deploying open API to VPS"

if [ -n "$VPS_IP" ] && [ -n "$VPS_USER" ]; then
    tar -czf deploy.tar.gz app.py requirements.txt
    scp -o StrictHostKeyChecking=no deploy.tar.gz $VPS_USER@$VPS_IP:/tmp/
    ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP << 'ENDSSH'
        mkdir -p /opt/open-api
        cd /opt/open-api
        tar -xzf /tmp/deploy.tar.gz
        pip3 install -r requirements.txt
        # Kill old process if running
        pkill -f "python3 app.py" || true
        # Start new one in background (or use systemd)
        nohup python3 app.py > api.log 2>&1 &
        echo "✅ API restarted"
ENDSSH
    echo "🎉 Deployment complete"
else
    echo "⚠️ VPS credentials missing – skipping deploy"
fi
