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

# BiS removed
RESPONSE_ORDER = ["Major +2%", "Upgrade 1-2%", "Sidegrade 0-1%"]

# map common label variants to our buckets
RESPONSE_VARIANTS = {
    "major +2%": "Major +2%",
    "major upgrade +2%": "Major +2%",
    "großes upgrade +2%": "Major +2%",
    "grosses upgrade +2%": "Major +2%",

    "upgrade 1-2%": "Upgrade 1-2%",
    "upgrade 1–2%": "Upgrade 1-2%",
    "verbesserung 1-2%": "Upgrade 1-2%",
    "verbesserung 1–2%": "Upgrade 1-2%",

    "sidegrade 0-1%": "Sidegrade 0-1%",
    "sidegrade 0–1%": "Sidegrade 0-1%",
    "seitengrade 0-1%": "Sidegrade 0-1%",
    "seitengrade 0–1%": "Sidegrade 0-1%",
}

def normalize_response(name: str) -> str | None:
    if not name:
        return None
    key = name.strip().lower()
    return RESPONSE_VARIANTS.get(key)

def group_for_character(char_name: str) -> str:
    """Derive Tanks und Heiler / Melees / Ranges from CHARACTER_CLASSES."""
    cls_spec = CHARACTER_CLASSES.get(char_name)
    if not cls_spec:
        return "Ungrouped"
    _, spec = cls_spec
    if spec in ("Tank", "Heal"):
        return "Tanks und Heiler"
    if spec == "Melee":
        return "Melees"
    if spec == "Ranged":
        return "Ranges"
    return "Ungrouped"

@client.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    tree.copy_global_to(guild=guild)
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

# ---------- Loot summary builder & Refresh button ----------

def build_group_summary_text(items, difficulty: str, target_group: str) -> str | None:
    """
    Build one group's summary text using current items, difficulty and auto-grouping.
    Returns None if this group has no matching rows.
    """
    # group -> char -> bucket -> count
    grouped_data = defaultdict(lambda: defaultdict(int))

    for item in items:
        raw_resp = (item.get("response_type") or {}).get("name", "")
        resp = normalize_response(raw_resp)
        if not resp or resp not in RESPONSE_ORDER:
            continue

        if (item.get("difficulty", "") or "").lower() != difficulty.lower():
            continue

        char_id = item.get("character_id")
        char_name = CHARACTER_MAP.get(char_id, f"ID {char_id}")

        group = group_for_character(char_name)
        if group != target_group:
            continue

        grouped_data[char_name][resp] += 1

    if not grouped_data:
        return None

    # dynamic width for Name column (no huge gap)
    max_name_len = max(len(n) for n in grouped_data.keys())
    header = "Name".ljust(max_name_len) + "".join(f" | {resp:<16}" for resp in RESPONSE_ORDER)
    sep_len = max_name_len + len(RESPONSE_ORDER) * (3 + 16)

    message = f"📊 Loot Summary — {difficulty.title()} ({target_group})\n"
    message += "```\n" + header + "\n" + "-" * sep_len + "\n"

    for char in sorted(grouped_data.keys()):
        row = char.ljust(max_name_len)
        for resp in RESPONSE_ORDER:
            count = grouped_data[char].get(resp, 0)
            row += f" | {(str(count) if count else ''):<16}"
        message += row + "\n"
    message += "```"
    return message

class LootSummaryView(discord.ui.View):
    def __init__(self, difficulty: str, group: str, *, timeout: float | None = 300):
        super().__init__(timeout=timeout)
        self.difficulty = difficulty
        self.group = group

    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.primary, emoji="🔄")
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        items = get_loot_history()
        new_text = build_group_summary_text(items, self.difficulty, self.group)
        if not new_text:
            new_text = f"📭 No matching loot entries for **{self.group}**."
        # Re-attach a new view so the button keeps working after edits
        await interaction.response.edit_message(content=new_text, view=LootSummaryView(self.difficulty, self.group))

# ----------------------------------------------------------

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
            filtered = [i for i in filtered if (i.get("difficulty", "") or "").lower() == difficulty.lower()]

        if not filtered:
            await interaction.edit_original_response(content="📭 No matching loot entries found.")
            return

        summary = f"📦 **Loot History**\n"
        for item in filtered[:20]:
            date = (item.get("awarded_at", "") or "")[:10]
            char_id = item.get("character_id")
            char_name = CHARACTER_MAP.get(char_id, f"ID {char_id}")
            name = item.get("name", "Unnamed Item")
            slot = (item.get("slot", "") or "").replace("_", " ")
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

        sent_any = False
        ordered_groups = ["Tanks und Heiler", "Melees", "Ranges"]

        # include Ungrouped at the end if any rows fall there
        # quick probe:
        has_ungrouped = any(group_for_character(CHARACTER_MAP.get(i.get("character_id"), ""))
                            == "Ungrouped"
                            for i in items)
        if has_ungrouped:
            ordered_groups.append("Ungrouped")

        for group in ordered_groups:
            text = build_group_summary_text(items, difficulty, group)
            if not text:
                continue
            view = LootSummaryView(difficulty, group)
            await interaction.followup.send(content=text, view=view)
            sent_any = True

        if not sent_any:
            await interaction.edit_original_response(content="📭 No matching loot entries found.")
        else:
            await interaction.edit_original_response(content="✅ Posted loot summaries with a Refresh button.")

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
        "/lootsummary - Show loot summary by role and difficulty (with Refresh button).\n"
        "/characterids - Show tracked character IDs.\n"
        "/roster - Show the current team roster grouped by role.\n"
        "/missingwishlist - Show who is missing a wishlist.\n"
        "/help - Show this help message.\n"
    )
    await interaction.response.send_message(message)

print(f"🔐 API Key starts with: {WOWAUDIT_API_KEY[:5]}")
client.run(DISCORD_TOKEN)
