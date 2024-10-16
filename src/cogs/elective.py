import discord
from discord import app_commands
from discord.ext import commands
from xml.etree import ElementTree as ET
from utils.elective_helper import create_new_category, create_new_role, toggle_role, roles_btn_view


class ElectiveGroup(commands.GroupCog, name="elective", description="Elective commands"):
    group = app_commands.Group(name="functions", description="Elective functions")
    
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Elective Cog loaded")
    
    @app_commands.command(name="initialize", description="create elective selected pattern")
    async def elective_init(self, interaction: discord.Interaction):
        # Send message and store the message ID and channel ID
        await interaction.response.send_message("Elective initialized")
        message = await interaction.channel.send("Select a role:", view=await roles_btn_view(interaction))
        
        # Store IDs in XML for later use
        self.store_message_data(interaction.channel.id, message.id)

    @app_commands.command(name="create", description="create elective category")
    async def elective(self, interaction: discord.Interaction, name: str):
        # Create new role and category
        name = name + " (take)"
        new_role = await create_new_role(interaction, name)
        await create_new_category(interaction, name, new_role)
        await toggle_role(interaction, new_role)
        
        # Update the message with new role options
        channel_id, message_id = self.retrieve_message_data()
        channel = await interaction.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.edit(content="Select a role:", view=await roles_btn_view(interaction))

    def store_message_data(self, channel_id, message_id):
        # Save message and channel data to XML
        root = ET.Element("root")
        channel_elem = ET.SubElement(root, "channel_id")
        channel_elem.text = str(channel_id)
        message_elem = ET.SubElement(root, "message_id")
        message_elem.text = str(message_id)
        
        tree = ET.ElementTree(root)
        tree.write("src/data/elective.xml")

    def retrieve_message_data(self):
        # Read message and channel IDs from XML
        tree = ET.parse("data/elective.xml")
        root = tree.getroot()
        channel_id = int(root.find("channel_id").text)
        message_id = int(root.find("message_id").text)
        
        return channel_id, message_id

# Add the cog to the bot
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ElectiveGroup(bot))
