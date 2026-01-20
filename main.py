import discord
from discord.ext import commands
import re
import os

# Intents needed to detect member updates
intents = discord.Intents.default()
intents.members = True
intents.presences = True  # needed to read status

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace these with your actual IDs
GUILD_ID = 1449955287682514976      # your server ID
ROLE_ID = 1454677608733216880       # role to assign
TEXT_CHANNEL_ID = 1462339053193138260  # text channel for notifications

# Regex pattern to detect the vanity link
VANITY_LINK_PATTERN = r"/bananite"

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.event
async def on_member_update(before, after):
    # Check if the user updated their status
    if after.activity and hasattr(after.activity, "name"):
        status = after.activity.name
        if re.search(VANITY_LINK_PATTERN, status, re.IGNORECASE):
            guild = bot.get_guild(GUILD_ID)
            role = guild.get_role(ROLE_ID)
            member = guild.get_member(after.id)

            # Assign role if not already assigned
            if role not in member.roles:
                await member.add_roles(role)
                print(f"Assigned {role.name} to {member.name}")

                # Send a message in your specific text channel
                text_channel = guild.get_channel(TEXT_CHANNEL_ID)
                await text_channel.send(
                    f"🍌 {member.mention} has received the role {role.name} for showing `/bananite` in their status!"
                )

import os

TOKEN = os.environ.get("DISCORD_TOKEN")  # <-- this reads the token from your environment
bot.run(TOKEN)
