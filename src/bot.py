import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from utils.init_helper import handle_extension

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Sync commands with the server
    guild_id = discord.Object(id=1285862754208448546)  # Replace with your server's ID
    try:
        await bot.tree.sync(guild=guild_id)  # Sync slash commands to a specific server
        print(f"Slash commands synced to the guild: {guild_id.id}")
    except Exception as e:
        print(f"Error syncing slash commands: {e}")
    
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def load(ctx, extension):
    await handle_extension(ctx, extension, bot.load_extension)

@bot.command()
async def unload(ctx, extension):
    await handle_extension(ctx, extension, bot.unload_extension)

@bot.command()
async def reload(ctx, extension):
    await handle_extension(ctx, extension, bot.reload_extension)

async def load_extensions():
    for filename in os.listdir('src/cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            
@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context) -> None:
    """Sync commands"""
    synced = await ctx.bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} commands globally")

# Main function to start the bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())