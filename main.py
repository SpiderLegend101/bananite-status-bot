import discord
from discord.ext import commands, tasks
import re
import os

# ====== INTENTS ======
intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== CONFIGURATION ======
GUILD_ID = 1449955287682514976
STATUS_ROLE_ID = 1454677608733216880
TEXT_CHANNEL_ID = 1462339053193138260

VANITY_LINK_PATTERN = r"(\/bananite|discord\.gg\/bananite)"

def has_bananite_status(member: discord.Member) -> bool:
    for activity in member.activities:
        if isinstance(activity, discord.CustomActivity):
            if activity.name and re.search(VANITY_LINK_PATTERN, activity.name, re.IGNORECASE):
                return True
    return False

def should_have_status_role(member: discord.Member) -> bool:
    return has_bananite_status(member)

@bot.event
async def on_ready():
    activity = discord.Streaming(
        name="discord.gg/bananite",
        url="https://twitch.tv/doesnotexist123456"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print(f"{bot.user} is online!")

    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(STATUS_ROLE_ID)
    channel = bot.get_channel(TEXT_CHANNEL_ID)

    for member in guild.members:
        if should_have_status_role(member) and role not in member.roles:
            await member.add_roles(role)
            await channel.send(f"🍌 {member.mention} has received **{role.name}**!")

    fast_scan.start()

@bot.event
async def on_presence_update(before, after):
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(STATUS_ROLE_ID)
    member = guild.get_member(after.id)
    channel = bot.get_channel(TEXT_CHANNEL_ID)

    if not member:
        return

    if should_have_status_role(after) and role not in member.roles:
        await member.add_roles(role)
        await channel.send(f"🍌 {member.mention} has received **{role.name}**!")

    elif not should_have_status_role(after) and role in member.roles:
        await member.remove_roles(role)

@tasks.loop(seconds=30)
async def fast_scan():
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(STATUS_ROLE_ID)
    channel = bot.get_channel(TEXT_CHANNEL_ID)

    for member in guild.members:
        if should_have_status_role(member) and role not in member.roles:
            await member.add_roles(role)
            await channel.send(f"🍌 {member.mention} has received **{role.name}**!")
        elif not should_have_status_role(member) and role in member.roles:
            await member.remove_roles(role)

TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing!")

bot.run(TOKEN)
