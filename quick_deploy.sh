#!/bin/bash

# Quick Start Deployment Script
# Run on your VPS to deploy the bot quickly

#!/bin/bash
set -e

REPO_URL="$1"
BOT_DIR="/home/autobump/auto-bump"

if [ -z "$REPO_URL" ]; then
    echo "Usage: ./quick_deploy.sh <git_repo_url>"
    echo "Example: ./quick_deploy.sh https://github.com/user/auto-bump.git"
    exit 1
fi

echo "Stopping existing service..."
sudo systemctl stop autobump 2>/dev/null || true

echo "Pulling latest code..."
cd $BOT_DIR
sudo -u autobump git pull origin main

echo "Installing dependencies..."
sudo python3 -m pip install -r requirements.txt

echo "Restarting service..."
sudo systemctl restart autobump

echo "Checking status..."
sudo systemctl status autobump

echo "Done! Check logs with: sudo journalctl -u autobump -f"
