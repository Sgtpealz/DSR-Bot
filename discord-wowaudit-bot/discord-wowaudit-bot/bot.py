import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import requests
from collections import defaultdict
import re

from wow_data import (
    CHARACTER_MAP, CHARACTER_NAME_TO_ID, CHARACTER_ROLES, CHARACTER_CLASSES,
    CLASS_HEX_COLORS, CLASS_ICONS
)


# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WOWAUDIT_API_KEY = os.getenv('WOWAUDIT_API_KEY')
WOWAUDIT_BASE_URL = os.getenv('WOWAUDIT_BASE_URL')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

SEASON_ID = 15

IGNORED_RESPONSES = [
    "Personal Loot - Non tradeable", "Persönliche Beute – Nicht handelbar",
    "Candidate didn't respond on time", "Offspec/Greed", "Mainspec/Need", "Need", "2nd Spec",
    "Button4", "Minor Upgrade", "Autopass", "Pass", "Mog", "Disenchant"
]

RESPONSE_ORDER = ["BiS", "Major +2%", "Upgrade 1-2%", "Sidegrade 0-1%"]

@client.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    tree.copy_global_to(guild=guild)
    
    # This will REMOVE all commands in the guild and sync new ones
    await tree.sync(guild=guild)  

    print(f'✅ Slash commands synced to guild {GUILD_ID}')
    print(f'✅ Logged in as {client.user}')

def get_loot_history():
    headers = {
        "Authorization": WOWAUDIT_API_KEY,
        "Accept": "application/json"
    }
    url = f"{WOWAUDIT_BASE_URL}/v1/loot_history/{SEASON_ID}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("history_items", [])
    return []

@tree.command(name="wishlist", description="Submit a Raidbots Droptimizer link for your character.")
@app_commands.describe(character="Your character name", link="Your Droptimizer link")
async def wishlist(interaction: discord.Interaction, character: str, link: str):
    await interaction.response.send_message("🔄 Submitting wishlist to WowAudit...")
    try:
        report_id_match = re.search(r"droptimizer.*/reports/([a-zA-Z0-9]+)", link)
        if not report_id_match:
            await interaction.edit_original_response(content="❌ Invalid link. Make sure it's a valid Raidbots Droptimizer link.")
            return

        report_id = report_id_match.group(1)
        char_id = CHARACTER_NAME_TO_ID.get(character)

        if not char_id:
            await interaction.edit_original_response(content="❌ Character not recognized. Please use your full name exactly.")
            return

        payload = {
            "report_id": report_id,
            "character_id": char_id,
            "character_name": character,
            "configuration_name": "Single Target",
            "replace_manual_edits": True,
            "clear_conduits": True
        }

        headers = {
            "Authorization": WOWAUDIT_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        res = requests.post(f"{WOWAUDIT_BASE_URL}/v1/wishlists", json=payload, headers=headers)
        if res.status_code == 200:
            await interaction.edit_original_response(content="✅ Wishlist submitted successfully!")
        else:
            await interaction.edit_original_response(content=f"❌ Failed to submit wishlist. Status: {res.status_code}")

    except Exception as e:
        print(f"❌ Error during /wishlist: {e}")
        await interaction.edit_original_response(content="❌ Unexpected error occurred while submitting wishlist.")

@tree.command(name="loothistory", description="Show loot history optionally filtered by character and/or difficulty.")
@app_commands.describe(character="Character name", difficulty="Difficulty (Heroic or Mythic)")
async def loothistory(interaction: discord.Interaction, character: str = None, difficulty: str = None):
    await interaction.response.send_message("🔄 Fetching loot history...")

    try:
        items = get_loot_history()
        if not items:
            await interaction.edit_original_response(content="📭 No loot has been awarded this season yet.")
            return

        filtered = items
        if character:
            filtered = [i for i in filtered if CHARACTER_MAP.get(i.get("character_id")) == character]
        if difficulty:
            filtered = [i for i in filtered if i.get("difficulty", "").lower() == difficulty.lower()]

        if not filtered:
            await interaction.edit_original_response(content="📭 No matching loot entries found.")
            return

        summary = f"📦 **Loot History**\n"
        for item in filtered[:20]:
            date = item.get("awarded_at", "")[:10]
            char_id = item.get("character_id")
            char_name = CHARACTER_MAP.get(char_id, f"ID {char_id}")
            name = item.get("name", "Unnamed Item")
            slot = item.get("slot", "").replace("_", " ")
            difficulty_str = item.get("difficulty", "Unknown")
            summary += f"- **{name}** ({slot}) | `{date}` | 🎯 {char_name} | 🛡 {difficulty_str} \n"

        await interaction.edit_original_response(content=summary[:1900])

    except Exception as e:
        print(f"❌ Error during /loothistory: {e}")
        await interaction.edit_original_response(content="❌ Error fetching loot history.")

@tree.command(name="lootsummary", description="Show loot summary by difficulty and grouped by role.")
@app_commands.describe(difficulty="Difficulty to filter (Heroic or Mythic)")
async def lootsummary(interaction: discord.Interaction, difficulty: str):
    await interaction.response.send_message("🔄 Compiling loot summary...")

    try:
        items = get_loot_history()
        if not items:
            await interaction.edit_original_response(content="📭 No loot entries found.")
            return

        grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for item in items:
            response = item.get("response_type", {}).get("name", "Unknown")
            if response in IGNORED_RESPONSES or response not in RESPONSE_ORDER:
                continue

            difficulty_val = item.get("difficulty", "").lower()
            if difficulty_val != difficulty.lower():
                continue

            char_id = item.get("character_id")
            char_name = CHARACTER_MAP.get(char_id, f"ID {char_id}")

            for group, names in CHARACTER_ROLES.items():
                if char_name in names:
                    grouped_data[group][char_name][response] += 1

        for group in ["Tanks und Heiler", "Melees", "Ranges"]:
            if group not in grouped_data:
                continue

            message = f"📊 Loot Summary — {difficulty.title()} ({group})\n"
            message += "```\nName            " + ''.join(f"| {resp:<20}" for resp in RESPONSE_ORDER) + "\n"
            message += "-" * (len(message.splitlines()[-1])) + "\n"

            for char in sorted(grouped_data[group]):
                row = f"{char:<15}"
                for resp in RESPONSE_ORDER:
                    count = grouped_data[group][char].get(resp, 0)
                    cell = f"{count}" if count > 0 else ""
                    row += f"| {cell:<20}"
                message += row + "\n"
            message += "```"

            await interaction.followup.send(content=message[:2000])

    except Exception as e:
        print(f"❌ Error during /lootsummary: {e}")
        await interaction.edit_original_response(content="❌ Unexpected error while summarizing loot.")

# Additional commands

@tree.command(name="characterids", description="Show all character IDs currently tracked.")
async def characterids(interaction: discord.Interaction):
    message = "**📋 Character IDs:**\n"
    for char_id, name in CHARACTER_MAP.items():
        message += f"{name}: `{char_id}`\n"
    await interaction.response.send_message(message[:1900])

@tree.command(name="roster", description="Show the current roster with class and spec.")
async def roster(interaction: discord.Interaction):
    embed = discord.Embed(title="🗒️ Current Roster", color=0x2ecc71)

    for role_group, names in CHARACTER_ROLES.items():
        role_text = ""
        for name in names:
            char_class, spec = CHARACTER_CLASSES.get(name, ("Unknown", "Unknown"))
            role_text += f"**{name}** - *{char_class} - {spec}*\n"

        embed.add_field(name=role_group, value=role_text, inline=False)

    await interaction.response.send_message(embed=embed)

@tree.command(name="missingwishlist", description="Show characters who have not submitted a wishlist.")
async def missingwishlist(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Checking wishlists...")

    try:
        headers = {
            "Authorization": WOWAUDIT_API_KEY,
            "Accept": "application/json"
        }
        url = f"{WOWAUDIT_BASE_URL}/v1/wishlists"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            await interaction.edit_original_response(content="❌ Failed to fetch wishlists.")
            return

        wishlist_data = response.json().get("wishlists", [])
        characters_with_wishlist = {item.get("character_id") for item in wishlist_data}

        missing = [name for char_id, name in CHARACTER_MAP.items() if char_id not in characters_with_wishlist]

        if not missing:
            await interaction.edit_original_response(content="✅ All characters have submitted a wishlist.")
            return

        message = "**🚨 Missing Wishlists:**\n"
        for name in sorted(missing):
            message += f"- {name}\n"

        await interaction.edit_original_response(content=message[:1900])

    except Exception as e:
        print(f"❌ Error during /missingwishlist: {e}")
        await interaction.edit_original_response(content="❌ Error checking wishlists.")

@tree.command(name="help", description="Show all available bot commands.")
async def help_command(interaction: discord.Interaction):
    message = (
        "**📖 Available Commands:**\n"
        "/wishlist - Submit a Raidbots Droptimizer link.\n"
        "/loothistory - Show loot history (optional filters).\n"
        "/lootsummary - Show loot summary by role and difficulty.\n"
        "/characterids - Show tracked character IDs.\n"
        "/roster - Show the current team roster grouped by role.\n"
        "/missingwishlist - Show who is missing a wishlist.\n"
        "/help - Show this help message.\n"
    )
    await interaction.response.send_message(message)

print(f"🔐 API Key starts with: {WOWAUDIT_API_KEY[:5]}")
client.run(DISCORD_TOKEN)
