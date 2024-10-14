from discord.ext import commands
from utils.elective_helper import create_new_category, create_new_role, add_role, roles_btn_view
from xml.etree import ElementTree as ET

class Elective(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Elective Cog loaded")
    
    @commands.command(name="init_elective", description="create elective selected pattern")
    async def elective_init(self, ctx: commands.Context):
        channel_id = ctx.channel.id
        view = await roles_btn_view(ctx)
        message = await ctx.send("Select a role:", view=view)
        
        message_id = message.id
        root = ET.Element("root")
        channel = ET.SubElement(root, "channel_id")
        channel.text = str(channel_id)
        message = ET.SubElement(root, "message_id")
        message.text = str(message_id)
        tree = ET.ElementTree(root)
        tree.write("data/elective.xml")

    @commands.command(name="create_elective", description="create elective category")
    async def elective(self, ctx: commands.Context, name: str):
        new_role = await create_new_role(ctx, name)
        await create_new_category(ctx, name, new_role=new_role)
        await add_role(ctx, new_role)
        # get the message id from data/elective.xml
        tree = ET.parse("data/elective.xml")
        root = tree.getroot()
        channel_id = int(root.find("channel_id").text)
        message_id = int(root.find("message_id").text)
        # Fetch the channel and message
        channel = await ctx.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)
        # add new role to the message
        view = await roles_btn_view(ctx)
        await message.edit(content="Select a role:", view=view)

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Elective(bot))
