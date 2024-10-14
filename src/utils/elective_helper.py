#elective_helper.py
import discord
import xml.etree.ElementTree as ET

class RolesBtnView(discord.ui.View):
    def __init__(self, roles, timeout=180):
        super().__init__(timeout=timeout)
        self.roles = roles
        for role in roles:
            self.add_item(RolesBtn(role))

class RolesBtn(discord.ui.Button):
    def __init__(self, role):
        super().__init__(label=role.name, style=discord.ButtonStyle.primary, custom_id=str(role.id))
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        role = self.role

        if role is None:
            await interaction.response.send_message("Role not found", ephemeral=True)
            return
        if role in user.roles:
            # Remove the role from the user
            await remove_role(interaction, user, role)
            return
        if role:
            # Add the role to the user
            await add_role(interaction, user, role)

async def create_new_category(interaction: discord.Interaction, name: str, new_role):
    # Check if the category already exists
    for category in interaction.guild.categories:
        if category.name == name:
            await interaction.response.send_message(f"Category {name} already exists!")
            return

    # Check if the category name is valid
    if len(name) > 20:
        await interaction.response.send_message("Category name is too long!")
        return

    # Get the guild and create a new category
    guild = interaction.guild
    new_category = await guild.create_category(name)
    new_category.set_permissions(guild.default_role, read_messages=False)
    new_category.set_permissions(new_role, read_messages=True)

    # Add text and voice channels to the category
    await guild.create_text_channel("notices", category=new_category)
    await guild.create_text_channel("HW", category=new_category)
    await guild.create_text_channel("Quiz", category=new_category)
    await guild.create_voice_channel("HW", category=new_category)
    await guild.create_voice_channel("Quiz", category=new_category)

    # Create a new role with the same name as the category
    new_role = await guild.create_role(name=name)
    
    # Send confirmation message
    await interaction.response.send_message(f"Category {name} and role {new_role.name} have been created!")

# crate new role function that can be called by the slash command
async def create_new_role(interaction: discord.Interaction, name: str):
    # Check if the role already exists
    for role in interaction.guild.roles:
        if role.name == name:
            await interaction.response.send_message(f"Role {name} already exists!")
            return

    # Check if the role name is valid
    if len(name) > 20:
        await interaction.response.send_message("Role name is too long!")
        return

    # Get the guild and create a new role
    guild = interaction.guild
    new_role = await guild.create_role(name=name)
    return new_role

    # Send confirmation message
    await interaction.response.send_message(f"Role {new_role.name} has been created!")

async def add_role(interaction: discord.Interaction, role):
    if not role:
        await interaction.response.send_message("Role not found!")
        return
    # Add the role to the user
    await interaction.user.add_roles(role)
    await interaction.response.send_message(f"Added {role.name} to {interaction.user.name}", ephemeral=True)

async def remove_role(interaction: discord.Interaction, user, role):
    if not role:
        await interaction.response.send_message("Role not found!")
        return
    # Remove the role from the user
    await interaction.user.remove_roles(role)
    await interaction.response.send_message(f"Removed {role.name} from {user.name}", ephemeral=True)
    

async def edit_message(interaction: discord.Interaction, message_id: int, new_content: str):
    # Get the channel and message
    channel = interaction.channel
    message = await channel.fetch_message(message_id)

    # Edit the message
    await message.edit(content=new_content)
    await interaction.response.send_message(f"Message {message_id} has been edited!")

async def roles_btn_view(ctx):
    roles = [role for role in ctx.guild.roles if role.name.endswith("(take)")]
    view = RolesBtnView(roles=roles, timeout=None)  # Explicitly pass roles by name
    return view
       




