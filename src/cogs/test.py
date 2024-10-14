#cogs/test.py
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    @commands.command(name="hello", description="Say hello to the bot")
    async def hello(self, ctx: commands.Context):
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(test(bot))
