import discord
from discord.ext import tasks
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

class AutoBumpBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.channel_id = CHANNEL_ID
        self.bump_tasks = {}
        self.last_bump_time = {}
        
        # Initialize last bump times
        for server_name in BUMP_SERVERS:
            self.last_bump_time[server_name] = datetime.now() - timedelta(hours=24)
    
    async def on_ready(self):
        logger.info(f"✓ Bot logged in as {self.user}")
        logger.info(f"✓ Connected to Discord")
        logger.info(f"✓ Target Channel ID: {self.channel_id}")
        logger.info(f"✓ Monitoring {len(BUMP_SERVERS)} servers")
        
        # Start the bump monitor if not already running
        if not self.bump_monitor.is_running():
            self.bump_monitor.start()
            logger.info("✓ Bump monitor started")
    
    async def send_bump_command(self, server_name):
        """Send a bump command to the configured channel"""
        try:
            channel = self.get_channel(self.channel_id)
            if channel is None:
                logger.error(f"✗ Channel {self.channel_id} not found")
                return False
            
            logger.info(f"→ Sending /bump command to {server_name}...")
            
            # Send the slash command - Discord will trigger the bot's slash command handler
            message = await channel.send("/bump")
            
            self.last_bump_time[server_name] = datetime.now()
            logger.info(f"✓ /bump slash command sent for {server_name} ✓")
            return True
            
        except Exception as e:
            logger.error(f"✗ Error sending bump for {server_name}: {str(e)}")
            return False
    
    @tasks.loop(minutes=1)
    async def bump_monitor(self):
        """Monitor and execute bump commands on schedule"""
        try:
            current_time = datetime.now()
            
            for server_name, config in BUMP_SERVERS.items():
                interval = timedelta(hours=config["interval_hours"])
                last_bump = self.last_bump_time.get(server_name, datetime.now() - timedelta(hours=24))
                
                # Check if enough time has passed
                if current_time - last_bump >= interval:
                    await self.send_bump_command(server_name)
                else:
                    # Calculate time until next bump
                    next_bump_time = last_bump + interval
                    time_remaining = next_bump_time - current_time
                    hours = int(time_remaining.total_seconds() // 3600)
                    minutes = int((time_remaining.total_seconds() % 3600) // 60)
                    
                    # Log every hour or at startup
                    if minutes == 0 or minutes == 1:
                        logger.debug(f"⏱ {server_name}: Next bump in {hours}h {minutes}m")
        
        except Exception as e:
            logger.error(f"✗ Error in bump monitor: {str(e)}")
    
    @bump_monitor.before_loop
    async def before_bump_monitor(self):
        """Wait until bot is ready before starting the monitor"""
        await self.wait_until_ready()

def main():
    logger.info("=" * 60)
    logger.info("Discord Auto Bump Bot - Starting")
    logger.info("=" * 60)
    
    try:
        bot = AutoBumpBot()
        bot.run(USER_TOKEN)
    except Exception as e:
        logger.error(f"✗ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
