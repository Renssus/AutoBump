# Discord Auto Bump Bot - VPS Setup Guide

## Overview
This is a Discord self-bot that automatically bumps your server on multiple platforms:
- **Disboard**: Every 2 hours
- **DiscServers**: Every 3 hours
- **D-Invites**: Every 2 hours
- **Discadia**: Every 24 hours

## System Requirements
- Ubuntu 20.04 LTS or newer
- Python 3.8+
- 256MB RAM minimum
- Internet connection

## Installation Steps

### Step 1: Upload Files to VPS
Upload all files to your VPS:
```bash
scp -r ./* user@your_vps_ip:/tmp/auto-bump/
```

### Step 2: SSH into VPS
```bash
ssh user@your_vps_ip
cd /tmp/auto-bump
```

### Step 3: Run Setup Script
```bash
sudo bash setup.sh
```

### Step 4: Configure Bot
Edit the config file with your credentials:
```bash
sudo nano /home/autobump/auto-bump/config.py
```

Update the following:
```python
USER_TOKEN = "YOUR_DISCORD_TOKEN_HERE"
CHANNEL_ID = 1453369707523739820  # Your channel ID
```

### Step 5: Start the Bot
```bash
sudo systemctl start autobump
```

### Step 6: Verify it's Running
```bash
sudo systemctl status autobump
```

To view real-time logs:
```bash
sudo journalctl -u autobump -f
```

## Common Commands

### Check Bot Status
```bash
sudo systemctl status autobump
```

### View Logs
```bash
# Recent logs
sudo journalctl -u autobump -n 50

# Follow logs in real-time
sudo journalctl -u autobump -f

# Logs from last hour
sudo journalctl -u autobump --since "1 hour ago"
```

### Restart Bot
```bash
sudo systemctl restart autobump
```

### Stop Bot
```bash
sudo systemctl stop autobump
```

### Remove from Autostart
```bash
sudo systemctl disable autobump
```

## Bump Schedule

| Platform | Interval | Last Bumped |
|----------|----------|-------------|
| Disboard | 2 hours | Auto-tracked |
| DiscServers | 3 hours | Auto-tracked |
| D-Invites | 2 hours | Auto-tracked |
| Discadia | 24 hours | Auto-tracked |

## Troubleshooting

### Bot Not Starting
1. Check logs: `sudo journalctl -u autobump -n 100`
2. Verify token is correct in config.py
3. Ensure channel ID exists and bot has access
4. Check Python version: `python3 --version`

### Permission Denied
```bash
sudo chown -R autobump:autobump /home/autobump/auto-bump
sudo chmod 755 /home/autobump/auto-bump
```

### Port Already in Use
The bot doesn't use a specific port, but ensure Discord connectivity is working:
```bash
ping discord.com
```

### Update Bot
To update the bot after making changes locally:
```bash
scp bot.py user@your_vps_ip:/tmp/bot.py
ssh user@your_vps_ip
sudo cp /tmp/bot.py /home/autobump/auto-bump/bot.py
sudo systemctl restart autobump
```

## Security Notes

⚠️ **Important**: Never share your bot token publicly!

- Keep `config.py` secured
- The setupscript creates a dedicated `autobump` user for security
- Logs are stored securely with systemd journal
- Token is only visible to the autobump user

## Support

Check bot logs for detailed error messages:
```bash
sudo journalctl -u autobump -f
```

## Uninstall

To completely remove the bot:
```bash
sudo systemctl stop autobump
sudo systemctl disable autobump
sudo rm /etc/systemd/system/autobump.service
sudo systemctl daemon-reload
sudo userdel -r autobump
```
