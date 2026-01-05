#!/bin/bash

# Discord Auto Bump Bot - Ubuntu VPS Setup Script
# Run this script on your Ubuntu VPS as root or with sudo

echo "================================================"
echo "Discord Auto Bump Bot - Ubuntu Installation"
echo "================================================"

# Update system packages
echo "[1/7] Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Python and pip
echo "[2/7] Installing Python 3 and pip..."
apt-get install -y python3 python3-pip python3-venv

# Create system user for the bot
echo "[3/7] Creating system user..."
if id "autobump" &>/dev/null; then
    echo "User 'autobump' already exists"
else
    useradd -r -s /bin/bash -d /home/autobump -m autobump
    echo "Created user 'autobump'"
fi

# Create application directory
echo "[4/7] Setting up application directory..."
mkdir -p /home/autobump/auto-bump
cd /home/autobump/auto-bump

# Copy bot files (you need to upload these first)
# Copy: bot.py, config.py, requirements.txt to /home/autobump/auto-bump/

# Install Python dependencies
echo "[5/7] Installing Python dependencies..."
python3 -m pip install -r requirements.txt

# Set permissions
echo "[6/7] Setting file permissions..."
chown -R autobump:autobump /home/autobump/auto-bump
chmod 755 /home/autobump/auto-bump
chmod 644 /home/autobump/auto-bump/*.py
chmod 644 /home/autobump/auto-bump/requirements.txt

# Install and enable systemd service
echo "[7/7] Installing systemd service..."
cp autobump.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable autobump.service

echo "================================================"
echo "Installation Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit /home/autobump/auto-bump/config.py with your token and channel ID"
echo "2. Start the service: sudo systemctl start autobump"
echo "3. Check status: sudo systemctl status autobump"
echo "4. View logs: sudo journalctl -u autobump -f"
echo ""
echo "Commands:"
echo "  Start:   sudo systemctl start autobump"
echo "  Stop:    sudo systemctl stop autobump"
echo "  Restart: sudo systemctl restart autobump"
echo "  Logs:    sudo journalctl -u autobump -f"
echo ""
