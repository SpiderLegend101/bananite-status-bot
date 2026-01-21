# main.py
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
ROLE_ID = 1454677608733216880
TEXT_CHANNEL_ID = 1462339053193138260

VANITY_LINK_PATTERN = r"(\/bananite|discord\.gg\/bananite)"  # Only keep /bananite check

# ====== CHECK FUNCTIONS ======
def has_bananite_status(member: discord.Member) -> bool:
    """Check if the member has /bananite in their custom status"""
    for activity in member.activities:
        if isinstance(activity, discord.CustomActivity):
            if activity.name and re.search(VANITY_LINK_PATTERN, activity.name, re.IGNORECASE):
                return True
    return False

def should_have_role(member: discord.Member) -> bool:
    return has_bananite_status(member)

# ====== EVENTS ======
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)
    channel = bot.get_channel(TEXT_CHANNEL_ID)

    # Initial scan when bot comes online
    for member in guild.members:
        if should_have_role(member) and role not in member.roles:
            await member.add_roles(role)
            await channel.send(f"🍌 {member.mention} has received **{role.name}**!")

    # Start the loop to continuously check members
    fast_scan.start()

@bot.event
async def on_presence_update(before, after):
    """Update roles when a member changes their custom status"""
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    member = guild.get_member(after.id)
    if not member:
        return

    had_role = should_have_role(before)
    has_role = should_have_role(after)

    if has_role and not had_role and role not in member.roles:
        await member.add_roles(role)
        await channel.send(f"🍌 {member.mention} has received **{role.name}**!")
    elif had_role and not has_role and role in member.roles:
        await member.remove_roles(role)
        await channel.send(f"⚠️ {member.mention} has lost **{role.name}**.")

# ====== TASK LOOP ======
@tasks.loop(seconds=30)
async def fast_scan():
    """Continuously scan members and assign/remove role based on /bananite status"""
    await bot.wait_until_ready()
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)
    channel = bot.get_channel(TEXT_CHANNEL_ID)

    for member in guild.members:
        if should_have_role(member) and role not in member.roles:
            await member.add_roles(role)
            await channel.send(f"🍌 {member.mention} has received **{role.name}**!")
        elif not should_have_role(member) and role in member.roles:
            await member.remove_roles(role)
            await channel.send(f"⚠️ {member.mention} has lost **{role.name}**.")

# ====== RUN BOT ======
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is missing!")

bot.run(TOKEN)
