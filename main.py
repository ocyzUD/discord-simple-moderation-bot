import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user.name}")

@bot.tree.command(name="ban", description="ban a useless member")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if member == interaction.user:
        await interaction.response.send_message("you cant ban yourself goober", ephemeral=True)
        return
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member} has been banned for {reason}")
    except Exception as e:
        await interaction.response.send_message(f"An error occured: {e}", ephemeral=True)

@bot.tree.command(name="kick", description="kick a nig from your server")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if member == interaction.user:
        await interaction.response.send_message("You cant kick yourself", ephemeral=True)
        return
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member} has been kicked for {reason}")
    except Exception as e:
        await interaction.response.send_message(f"An error occured: {e}", ephemeral=True)
                  
@bot.tree.command(name="mute", description="Mute a member")
async def mute(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    muted_role = discord.utils.get(interaction.guild.roles, name="muted")
    if not muted_role:
        muted_role = await interaction.guild.create_role(name="muted")
        for channel in interaction.guild.text_channels:
            await channel.set_permissions(muted_role, speak=False, send_message=False)


    try:
        await member.add_roles(muted_role, reason=reason)
        await interaction.response.send_message(f"{member} has been muted for {reason}")
    except Exception as e:
        await interaction.response.send_message(f"an error occured: {e}, ephermal=True")


@bot.tree.command(name="unmute", description="unmute a member")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    muted_role = discord.utils.get(interaction.guild.roles, name ="Muted")
    if not muted_role:
        await Interaction.response.send_message("no muted role found", ephemeral=True)
        return
    
    try:
        await member.remove_roles(muted_role)
        await interaction.response.send_message(f"{member} has been unmuted.")
    except Exception as e:
        await interaction.response.send_message(f"an error occured: {e}", ephemeral=True)

@ban.error
@kick.error
@mute.error
@unmute.error
async def on_command_error(interaction: discord.Integration, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("You dont have permissions to run these commands")

bot.run('YOUR_TOKEN_HERE')


