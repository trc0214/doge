import discord
from discord import app_commands
from discord.ext import commands

class TestGroup(commands.GroupCog, name="test", description="Test commands"):
    group = app_commands.Group(name="functions", description="Test functions")
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    # Event listener for when the bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("test Cog loaded")

    # Event listener for messages
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if 'ping' in message.content.lower():
            await message.channel.send('PONG!')

    # Slash command: /hello
    @app_commands.command(name="hello", description="Say hello to the bot")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TestGroup(bot))
