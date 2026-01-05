import asyncio
from discord.ext import commands
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

bot = commands.Bot(command_prefix="!", self_bot=True)

# Track last bump times
last_bump_time = {}
for server_name in BUMP_SERVERS:
    last_bump_time[server_name] = datetime.now() - timedelta(hours=24)

@bot.event
async def on_ready():
    logger.info("=" * 60)
    logger.info(f"✓ Bot logged in as {bot.user.name}#{bot.user.discriminator}")
    logger.info(f"✓ User ID: {bot.user.id}")
    logger.info(f"✓ Target Channel ID: {CHANNEL_ID}")
    logger.info(f"✓ Monitoring {len(BUMP_SERVERS)} servers")
    logger.info("=" * 60)
    bot.loop.create_task(auto_bump())

async def send_bump_command(server_name, app_id):
    """Send bump command using slash command interaction"""
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            logger.error(f"✗ Channel {CHANNEL_ID} not found")
            return False
        
        logger.info(f"→ Sending /bump command to {server_name}...")
        
        # Get available application commands in the channel
        try:
            application_commands = await channel.application_commands()
            
            # Find the bump command for this specific bot
            for command in application_commands:
                if command.name == "bump" and str(command.application_id) == str(app_id):
                    await command(channel)
                    logger.info(f"✓ Bump sent for {server_name} ✓")
                    return True
            
            logger.warning(f"⚠ Bump command not found for {server_name}, trying fallback")
            await channel.send("/bump")
            return True
            
        except Exception as e:
            logger.error(f"✗ Error getting application commands: {str(e)}")
            await channel.send("/bump")
            return True
            
    except Exception as e:
        logger.error(f"✗ Error sending bump for {server_name}: {str(e)}")
        return False

async def auto_bump():
    """Auto bump task that runs continuously"""
    await bot.wait_until_ready()
    
    while not bot.is_closed():
        try:
            current_time = datetime.now()
            
            for server_name, config in BUMP_SERVERS.items():
                interval = timedelta(hours=config["interval_hours"])
                last_bump = last_bump_time.get(server_name, datetime.now() - timedelta(hours=24))
                
                # Check if enough time has passed
                if current_time - last_bump >= interval:
                    app_id = config["server_id"]
                    success = await send_bump_command(server_name, app_id)
                    
                    if success:
                        last_bump_time[server_name] = datetime.now()
                    
                    await asyncio.sleep(2)  # Small delay between bumps
                else:
                    # Calculate time until next bump
                    next_bump_time = last_bump + interval
                    time_remaining = next_bump_time - current_time
                    hours = int(time_remaining.total_seconds() // 3600)
                    minutes = int((time_remaining.total_seconds() % 3600) // 60)
                    
                    logger.debug(f"⏱ {server_name}: Next bump in {hours}h {minutes}m")
            
            # Wait 60 seconds before checking again
            await asyncio.sleep(60)
            
        except Exception as e:
            logger.error(f"✗ Error in auto bump: {str(e)}")
            await asyncio.sleep(60)

def main():
    logger.info("=" * 60)
    logger.info("Discord Auto Bump Bot - Starting")
    logger.info("=" * 60)
    
    try:
        bot.run(USER_TOKEN)
    except Exception as e:
        logger.error(f"✗ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
