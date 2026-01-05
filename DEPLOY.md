# Quick VPS Deployment Guide

## Prerequisites
- Ubuntu 20.04+ VPS with root/sudo access
- Git installed
- SSH access to your VPS

## One-Command Deployment

```bash
ssh root@your_vps_ip
curl -fsSL https://raw.githubusercontent.com/Renssus/AutoBump/main/deploy.sh | bash
```

Or manually:

## Step-by-Step Deployment

### 1. SSH into your VPS
```bash
ssh root@your_vps_ip
```

### 2. Clone the Repository
```bash
git clone https://github.com/Renssus/AutoBump.git /home/autobump/auto-bump
cd /home/autobump/auto-bump
```

### 3. Run the Setup Script
```bash
bash setup.sh
```

This will:
- Update system packages
- Install Python 3 & pip
- Create `autobump` system user
- Install dependencies from `requirements.txt`
- Set up systemd service for auto-startup
- Enable auto-start on reboot

### 4. Configure Your Bot
```bash
nano /home/autobump/auto-bump/config.py
```

Edit these lines:
```python
USER_TOKEN = "YOUR_DISCORD_TOKEN_HERE"
CHANNEL_ID = 1453369707523739820  # Your channel ID
```

Save: `Ctrl+X` → `Y` → `Enter`

### 5. Start the Bot
```bash
systemctl start autobump
```

### 6. Check if it's Running
```bash
systemctl status autobump
```

### 7. View Live Logs
```bash
journalctl -u autobump -f
```

## Common Commands After Deployment

### View Status
```bash
systemctl status autobump
```

### Restart Bot
```bash
systemctl restart autobump
```

### Stop Bot
```bash
systemctl stop autobump
```

### View Recent Logs
```bash
journalctl -u autobump -n 50
```

### View Last Hour of Logs
```bash
journalctl -u autobump --since "1 hour ago"
```

### Update Bot from GitHub
```bash
cd /home/autobump/auto-bump
git pull origin main
systemctl restart autobump
```

## What Each File Does

| File | Purpose |
|------|---------|
| `bot.py` | Main bot script - runs the auto-bump logic |
| `config.py` | Configuration (token, channel ID, bump schedules) |
| `requirements.txt` | Python dependencies (discord.py) |
| `autobump.service` | Systemd service file for auto-startup |
| `setup.sh` | Automated setup script |
| `deploy.sh` | One-command deployment script |

## Troubleshooting

### Bot Won't Start
```bash
# Check logs for errors
journalctl -u autobump -n 100

# Check if Python is installed
python3 --version

# Check if dependencies are installed
python3 -c "import discord; print(discord.__version__)"
```

### Permission Errors
```bash
sudo chown -R autobump:autobump /home/autobump/auto-bump
sudo chmod 755 /home/autobump/auto-bump
```

### Discord Token Error
- Verify token is correct in `config.py`
- Make sure there are no extra spaces/quotes
- Check token hasn't expired

### Bot Doesn't Send Bumps
- Check channel ID is correct: `journalctl -u autobump -f`
- Verify bot has permissions in that channel
- Make sure account isn't locked/banned

## Bump Schedule

The bot automatically bumps on this schedule:
- **Disboard**: Every 2 hours
- **DiscServers**: Every 3 hours
- **D-Invites**: Every 2 hours
- **Discadia**: Every 24 hours

Schedules are tracked automatically and won't double-bump.

## Security

- Never share your bot token
- Token is only readable by `autobump` user
- Logs don't contain sensitive token info
- Service runs as dedicated non-root user

## Getting Help

View all logs:
```bash
journalctl -u autobump -n 1000
```

Check if service is enabled:
```bash
systemctl is-enabled autobump
```

Disable auto-start:
```bash
systemctl disable autobump
```

Completely remove:
```bash
systemctl stop autobump
systemctl disable autobump
rm /etc/systemd/system/autobump.service
systemctl daemon-reload
userdel -r autobump
```
