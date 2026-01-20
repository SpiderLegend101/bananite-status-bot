import discord
from discord.ext import commands
import re
import os

# ====== INTENTS ======
intents = discord.Intents.default()
intents.members = True
intents.presences = True  # Needed to read custom statuses

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== CONFIGURATION ======
GUILD_ID = 1449955287682514976      # Your Discord server ID
ROLE_ID = 1454677608733216880       # Role to assign/remove
TEXT_CHANNEL_ID = 1462339053193138260  # Channel to send notifications
VANITY_LINK_PATTERN = r"(\/bananite|discord\.gg\/bananite)"  # Regex pattern

# ====== EVENTS ======
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")  # Logs bot username + discriminator

@bot.event
async def on_member_update(before, after):
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)
    member = guild.get_member(after.id)
    text_channel = guild.get_channel(TEXT_CHANNEL_ID)

    # Helper function to get /bananite custom status from activities
    def get_bananite_status(activities):
        for activity in activities:
            if isinstance(activity, discord.CustomActivity):
                status = activity.name
                if status and re.search(VANITY_LINK_PATTERN, status, re.IGNORECASE):
                    return True
        return False

    had_status = get_bananite_status(before.activities)
    has_status = get_bananite_status(after.activities)

    # ====== ROLE ASSIGNMENT ======
    if has_status and not had_status:
        # User added the /bananite status
        if role not in member.roles:
            await member.add_roles(role)
            print(f"Assigned {role.name} to {member.name}")
            await text_channel.send(
                f"🍌 {member.mention} has received the role {role.name} "
                f"for showing `/bananite` in their custom status!"
            )

    # ====== ROLE REMOVAL ======
    elif had_status and not has_status:
        # User removed /bananite from their status
        if role in member.roles:
            await member.remove_roles(role)
            print(f"Removed {role.name} from {member.name}")
            await text_channel.send(
                f"⚠️ {member.mention} has lost the role {role.name} "
                f"because `/bananite` was removed from their custom status."
            )

# ====== RUN BOT ======
TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(TOKEN)
