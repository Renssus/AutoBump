import requests
import time
import logging
import sys
from datetime import datetime, timedelta
from config import USER_TOKEN, CHANNEL_ID, BUMP_SERVERS, LOG_FILE, LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AutoBumpBot:
    def __init__(self):
        self.channel_id = CHANNEL_ID
        self.token = USER_TOKEN
        self.last_bump_time = {}
        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        self.api_url = "https://discord.com/api/v10"
        
        # Initialize last bump times
        for server_name in BUMP_SERVERS:
            self.last_bump_time[server_name] = datetime.now() - timedelta(hours=24)
    
    def verify_connection(self):
        """Verify bot can connect to Discord"""
        try:
            response = requests.get(f"{self.api_url}/users/@me", headers=self.headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"✓ Bot logged in as {user_data.get('username')}#{user_data.get('discriminator')}")
                logger.info(f"✓ Connected to Discord API")
                logger.info(f"✓ Target Channel ID: {self.channel_id}")
                logger.info(f"✓ Monitoring {len(BUMP_SERVERS)} servers")
                return True
            else:
                logger.error(f"✗ Authentication failed: {response.status_code}")
                logger.error(f"✗ Response: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Connection error: {str(e)}")
            return False
    
    def get_application_id(self, bot_name):
        """Get the application ID for bump bots"""
        bot_ids = {
            "Disboard": "302050872383242240",
            "DiscServers": "1376241207428255784",
            "D-Invites": "678211574183362571",
            "Discadia": "1222548162741538938"
        }
        return bot_ids.get(bot_name)
    
    def send_slash_command(self, application_id, command_name="bump"):
        """Send a slash command interaction to Discord"""
        try:
            url = f"{self.api_url}/interactions"
            
            # Interaction payload for slash command
            payload = {
                "type": 2,  # Application Command
                "application_id": application_id,
                "guild_id": None,  # DM or will be filled by Discord
                "channel_id": str(self.channel_id),
                "session_id": "placeholder",
                "data": {
                    "version": "1166735583352238130",
                    "id": application_id,
                    "name": command_name,
                    "type": 1,
                    "options": [],
                    "application_command": {
                        "id": application_id,
                        "application_id": application_id,
                        "version": "1166735583352238130",
                        "type": 1,
                        "name": command_name,
                        "description": "Bump this server",
                        "dm_permission": True,
                        "contexts": [0, 1, 2],
                        "integration_types": [0, 1],
                        "options": []
                    },
                    "attachments": []
                },
                "nonce": str(int(time.time() * 1000))
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            
            if response.status_code in [200, 201, 204]:
                logger.info(f"✓ Slash command sent successfully")
                return True
            else:
                # Fallback: Try sending as message (will trigger autocomplete)
                logger.warning(f"Interaction API returned {response.status_code}, trying text fallback")
                return self.send_message(f"/{command_name}")
                
        except Exception as e:
            logger.error(f"✗ Error sending slash command: {str(e)}")
            # Fallback to text
            return self.send_message(f"/{command_name}")
    
    def send_message(self, content):
        """Send a message to the channel"""
        try:
            url = f"{self.api_url}/channels/{self.channel_id}/messages"
            payload = {"content": content}
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            
            if response.status_code in [200, 201]:
                logger.info(f"✓ Message sent: {content}")
                return True
            else:
                logger.error(f"✗ Failed to send message: {response.status_code}")
                logger.error(f"✗ Response: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Error sending message: {str(e)}")
            return False
    
    def send_bump_command(self, server_name):
        """Send a bump command to the configured channel"""
        try:
            logger.info(f"→ Sending /bump command to {server_name}...")
            
            # Get the application ID for this bump service
            app_id = self.get_application_id(server_name)
            
            if app_id:
                # Try to send as proper slash command interaction
                success = self.send_slash_command(app_id, "bump")
            else:
                # Fallback to text message
                success = self.send_message("/bump")
            
            if success:
                self.last_bump_time[server_name] = datetime.now()
                logger.info(f"✓ Bump sent for {server_name} ✓")
            
            return success
            
        except Exception as e:
            logger.error(f"✗ Error sending bump for {server_name}: {str(e)}")
            return False
    
    def check_and_bump(self):
        """Check if any bumps are due and send them"""
        try:
            current_time = datetime.now()
            
            for server_name, config in BUMP_SERVERS.items():
                interval = timedelta(hours=config["interval_hours"])
                last_bump = self.last_bump_time.get(server_name, datetime.now() - timedelta(hours=24))
                
                # Check if enough time has passed
                if current_time - last_bump >= interval:
                    self.send_bump_command(server_name)
                    # Small delay between bumps
                    time.sleep(2)
                else:
                    # Calculate time until next bump
                    next_bump_time = last_bump + interval
                    time_remaining = next_bump_time - current_time
                    hours = int(time_remaining.total_seconds() // 3600)
                    minutes = int((time_remaining.total_seconds() % 3600) // 60)
                    
                    logger.debug(f"⏱ {server_name}: Next bump in {hours}h {minutes}m")
        
        except Exception as e:
            logger.error(f"✗ Error in bump check: {str(e)}")
    
    def run(self):
        """Main bot loop"""
        logger.info("=" * 60)
        logger.info("Discord Auto Bump Bot - Starting")
        logger.info("=" * 60)
        
        # Verify connection
        if not self.verify_connection():
            logger.error("✗ Failed to connect to Discord")
            sys.exit(1)
        
        logger.info("✓ Bot ready and monitoring")
        logger.info("=" * 60)
        
        # Main loop - check every minute
        try:
            while True:
                self.check_and_bump()
                time.sleep(60)  # Check every 60 seconds
        except KeyboardInterrupt:
            logger.info("✓ Bot stopped by user")
        except Exception as e:
            logger.error(f"✗ Fatal error: {str(e)}")
            sys.exit(1)

def main():
    try:
        bot = AutoBumpBot()
        bot.run()
    except Exception as e:
        logger.error(f"✗ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
