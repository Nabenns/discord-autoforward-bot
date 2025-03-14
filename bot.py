import os
import logging
import colorlog
from typing import Optional
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
))

logger = logging.getLogger('discord_bot')
logger.addHandler(handler)
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID', 0))
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', 0))

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Event handler when bot is ready."""
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')
    logger.info(f'Forwarding messages from channel {SOURCE_CHANNEL_ID} to {TARGET_CHANNEL_ID}')

async def forward_attachments(message: discord.Message, target_channel: discord.TextChannel) -> None:
    """Forward attachments from source message to target channel."""
    for attachment in message.attachments:
        try:
            await target_channel.send(file=await attachment.to_file())
            logger.debug(f'Forwarded attachment: {attachment.filename}')
        except Exception as e:
            logger.error(f'Failed to forward attachment {attachment.filename}: {str(e)}')

async def forward_embeds(message: discord.Message, target_channel: discord.TextChannel) -> None:
    """Forward embeds from source message to target channel."""
    if message.embeds:
        try:
            await target_channel.send(embeds=message.embeds)
            logger.debug('Forwarded embeds')
        except Exception as e:
            logger.error(f'Failed to forward embeds: {str(e)}')

@bot.event
async def on_message(message: discord.Message):
    """Event handler for new messages."""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if message is from source channel
    if message.channel.id != SOURCE_CHANNEL_ID:
        return

    # Get target channel
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if not target_channel:
        logger.error(f'Could not find target channel with ID {TARGET_CHANNEL_ID}')
        return

    try:
        # Forward message content if exists
        if message.content:
            author_name = message.author.name
            content = f'**{author_name}**: {message.content}'
            await target_channel.send(content)
            logger.debug(f'Forwarded message from {author_name}')

        # Forward attachments
        await forward_attachments(message, target_channel)

        # Forward embeds
        await forward_embeds(message, target_channel)

    except Exception as e:
        logger.error(f'Error forwarding message: {str(e)}')

def main():
    """Main function to run the bot."""
    if not TOKEN:
        logger.error('No Discord token found in environment variables')
        return
    
    if SOURCE_CHANNEL_ID == 0:
        logger.error('No source channel ID found in environment variables')
        return
    
    if TARGET_CHANNEL_ID == 0:
        logger.error('No target channel ID found in environment variables')
        return

    try:
        logger.info('Starting bot...')
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f'Failed to start bot: {str(e)}')

if __name__ == '__main__':
    main()