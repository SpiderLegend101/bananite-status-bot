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

VANITY_LINK_PATTERN = r"(\/bananite|discord\.gg\/bananite)"

# ====== CHECK FUNCTIONS ======
def has_bananite_status(member: discord.Member) -> bool:
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

    for member in guild.members:
        if should_have_role(member) and role not in member.roles:
            await member.add_roles(role)
            await channel.send(f"🍌 {member.mention} has received **{role.name}**!")

    fast_scan.start()

@bot.event
async def on_presence_update(before, after):
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    member = guild.get_member(after.id)

    if not member:
        return

    had = should_have_role(before)
    has = should_have_role(after)

    if has and not had and role not in member.roles:
        await member.add_roles(role)
        await channel.send(f"🍌 {member.mention} has received **{role.name}**!")
    elif had and not has and role in member.roles:
        await member.remove_roles(role)
        await channel.send(f"⚠️ {member.mention} has lost **{role.name}**.")

@tasks.loop(seconds=30)
async def fast_scan():
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
bot.run(TOKEN)
