# Configuration file for Auto Bump Bot
# Update these values with your own token and channel ID

USER_TOKEN = "MTQ1MzEyMDA2NDM0OTAxMTk2OA.GXoC-t._xPEut5GsHTStBv9f_19eIv0UsW8WB-oPtU-1w"
CHANNEL_ID = 1453369707523739820

# Server IDs for bumping
BUMP_SERVERS = {
    "Disboard": {
        "server_id": 302050872383242240,
        "interval_hours": 2,
        "command": "/bump"
    },
    "DiscServers": {
        "server_id": 1376241207428255784,
        "interval_hours": 3,
        "command": "/bump"
    },
    "D-Invites": {
        "server_id": 678211574183362571,
        "interval_hours": 2,
        "command": "/bump"
    },
    "Discadia": {
        "server_id": 1222548162741538938,
        "interval_hours": 24,
        "command": "/bump"
    }
}

# Logging configuration
LOG_FILE = "auto_bump.log"
LOG_LEVEL = "INFO"
