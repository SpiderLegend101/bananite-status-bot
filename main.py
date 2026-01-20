import discord
from discord.ext import commands, tasks
import re
import os
from flask import Flask
from threading import Thread

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

# ====== HELPER FUNCTION ======
def has_bananite_custom_status(member):
    for activity in member.activities:
        if isinstance(activity, discord.CustomActivity) and activity.type == discord.ActivityType.custom:
            if activity.name and re.search(VANITY_LINK_PATTERN, activity.name, re.IGNORECASE):
                return True
    return False

# ====== SCAN MEMBERS ON STARTUP ======
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)
    text_channel = guild.get_channel(TEXT_CHANNEL_ID)

    for member in guild.members:
        if has_bananite_custom_status(member):
            if role not in member.roles:
                await member.add_roles(role)
                await text_channel.send(
                    f"🍌 {member.mention} has received the role {role.name} "
                    f"for showing `/bananite` in their custom status!"
                )

# ====== ON MEMBER UPDATE ======
@bot.event
async def on_member_update(before, after):
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)
    member = guild.get_member(after.id)
    text_channel = guild.get_channel(TEXT_CHANNEL_ID)

    had_status = has_bananite_custom_status(before)
    has_status = has_bananite_custom_status(after)

    # Assign role
    if has_status and not had_status:
        if role not in member.roles:
            await member.add_roles(role)
            await text_channel.send(
                f"🍌 {member.mention} has received the role {role.name} "
                f"for showing `/bananite` in their custom status!"
            )

    # Remove role
    elif had_status and not has_status:
        if role in member.roles:
            await member.remove_roles(role)
            await text_channel.send(
                f"⚠️ {member.mention} has lost the role {role.name} "
                f"because `/bananite` was removed from their custom status."
            )

# ====== KEEP BOT ONLINE ======
app = Flask('')

@app.route('/')
def home():
    return "Bananite Vanity is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

keep_alive()

# ====== RUN BOT ======
TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(TOKEN)
