import discord

# Helper Functions
def category_exists(guild, category_name: str):
    return any(category.name == category_name for category in guild.categories)

def role_exists(guild, role_name: str):
    return any(role.name == role_name for role in guild.roles)

async def configure_category_permissions(category, default_role, new_role):
    await category.set_permissions(default_role, read_messages=False)
    await category.set_permissions(new_role, read_messages=True)

async def create_default_channels(guild, category):
    channels = ["notices", "HW", "Quiz"]
    for channel in channels:
        await guild.create_text_channel(channel, category=category)
        await guild.create_voice_channel(channel, category=category)

# Role Management
async def toggle_role(interaction: discord.Interaction, role):
    if not role:
        return
    user = interaction.user
    if role in user.roles:
        await user.remove_roles(role)
    if role not in user.roles:
        await user.add_roles(role)

async def create_new_role(interaction: discord.Interaction, role_name: str):
    guild = interaction.guild
    
    if len(role_name) > 20:
        await interaction.response.send_message("Role name is too long!")
        return

    if role_exists(guild, role_name):
        await interaction.response.send_message(f"Role {role_name} already exists!")
        return

    new_role = await guild.create_role(name=role_name)
    return new_role

# Category Management
async def create_new_category(interaction: discord.Interaction, category_name: str, new_role):
    guild = interaction.guild
    
    if len(category_name) > 20:
        await interaction.response.send_message("Category name is too long!")
        return

    if category_exists(guild, category_name):
        await interaction.response.send_message(f"Category {category_name} already exists!")
        return

    new_category = await guild.create_category(category_name)
    await configure_category_permissions(new_category, guild.default_role, new_role)
    await create_default_channels(guild, new_category)
    
    await interaction.response.send_message(f"Category {category_name} created with role {new_role.name}!")

# Message Editing
async def edit_message(interaction: discord.Interaction, message_id: int, new_content: str):
    channel = interaction.channel
    message = await channel.fetch_message(message_id)
    
    await message.edit(content=new_content)
    await interaction.response.send_message(f"Message {message_id} has been edited!")

# UI Handling - Button for Roles
class RolesBtn(discord.ui.Button):
    def __init__(self, role):
        super().__init__(label=role.name, style=discord.ButtonStyle.primary, custom_id=str(role.id))
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        await toggle_role(interaction, self.role)
        

# UI Handling - Button View
class RolesBtnView(discord.ui.View):
    def __init__(self, roles, timeout=180):
        super().__init__(timeout=timeout)
        self.roles = roles
        self._add_role_buttons()

    def _add_role_buttons(self):
        for role in self.roles:
            self.add_item(RolesBtn(role))

# View for Role Buttons
async def roles_btn_view(interaction: discord.Interaction):
    roles = [role for role in interaction.guild.roles if role.name.endswith("(take)")]
    return RolesBtnView(roles=roles, timeout=None)
