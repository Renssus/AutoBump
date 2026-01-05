#!/bin/bash

# Discord Auto Bump Bot - One-Command VPS Deployment
# Run: bash deploy.sh

set -e

echo "================================================"
echo "Discord Auto Bump Bot - VPS Deployment"
echo "================================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "ERROR: This script must be run as root (use sudo)"
    exit 1
fi

# Update system
echo "[1/8] Updating system packages..."
apt-get update
apt-get upgrade -y

# Install dependencies
echo "[2/8] Installing Python 3 and Git..."
apt-get install -y python3 python3-pip git

# Create user
echo "[3/8] Creating autobump system user..."
if id "autobump" &>/dev/null; then
    echo "    → User 'autobump' already exists"
else
    useradd -r -s /bin/bash -d /home/autobump -m autobump
    echo "    → Created user 'autobump'"
fi

# Clone repository
echo "[4/8] Cloning AutoBump repository..."
if [ -d "/home/autobump/auto-bump" ]; then
    echo "    → Directory exists, pulling latest..."
    cd /home/autobump/auto-bump
    sudo -u autobump git pull origin main
else
    echo "    → Cloning repository..."
    sudo -u autobump git clone https://github.com/Renssus/AutoBump.git /home/autobump/auto-bump
fi

# Create virtual environment
echo "[5/8] Creating Python virtual environment..."
sudo -u autobump python3 -m venv /home/autobump/auto-bump/venv

# Install Python dependencies in venv
echo "[5.5/8] Installing Python dependencies..."
/home/autobump/auto-bump/venv/bin/pip install --upgrade pip setuptools wheel
/home/autobump/auto-bump/venv/bin/pip install -r /home/autobump/auto-bump/requirements.txt

# Verify discord.py is installed
echo "[5.7/8] Verifying installation..."
/home/autobump/auto-bump/venv/bin/pip list | grep discord

# Set permissions
echo "[6/8] Setting file permissions..."
chown -R autobump:autobump /home/autobump/auto-bump
chmod 755 /home/autobump/auto-bump
chmod 644 /home/autobump/auto-bump/*.py
chmod 644 /home/autobump/auto-bump/requirements.txt

# Install systemd service
echo "[7/8] Installing systemd service..."
cp /home/autobump/auto-bump/autobump.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable autobump

# Create log directory
echo "[8/8] Setting up logging..."
mkdir -p /var/log/autobump
chown autobump:autobump /var/log/autobump
chmod 755 /var/log/autobump

# Update config path in service file
sed -i 's|WorkingDirectory=/home/autobump/auto-bump|WorkingDirectory=/home/autobump/auto-bump|g' /etc/systemd/system/autobump.service
systemctl daemon-reload

echo ""
echo "================================================"
echo "✓ Installation Complete!"
echo "================================================"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Edit your Discord token and channel ID:"
echo "   nano /home/autobump/auto-bump/config.py"
echo ""
echo "   Set these values:"
echo "   USER_TOKEN = 'YOUR_DISCORD_TOKEN'"
echo "   CHANNEL_ID = 1453369707523739820"
echo ""
echo "2. Start the bot:"
echo "   systemctl start autobump"
echo ""
echo "3. Check if it's running:"
echo "   systemctl status autobump"
echo ""
echo "4. View live logs:"
echo "   journalctl -u autobump -f"
echo ""
echo "================================================"
echo "Useful Commands:"
echo "================================================"
echo "Start:       systemctl start autobump"
echo "Stop:        systemctl stop autobump"
echo "Restart:     systemctl restart autobump"
echo "Status:      systemctl status autobump"
echo "Logs:        journalctl -u autobump -f"
echo "Recent logs: journalctl -u autobump -n 50"
echo "Update:      cd /home/autobump/auto-bump && git pull && systemctl restart autobump"
echo ""
