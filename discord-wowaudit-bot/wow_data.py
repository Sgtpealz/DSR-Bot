# wow_data.py

# Character data from provided list
CHARACTER_MAP = {
    4343606: "Hannox",
    4440556: "Insebtion",
    4459420: "Iyásu",
    3938881: "Dengø",
    4342796: "Pudu",
    4414716: "Barrageobamá",
    4411771: "Greenmelt",
    4389535: "Hugeheals",
    4460945: "Thalvir",
    4225318: "Akaï",
    4339466: "Balest",
    4330503: "Valeeh",
    4397102: "Lattenseppi",
    4157476: "Böllercolada",
    4440555: "Farnis",
    3938886: "Stormi",
    4343631: "Bloody",
    4388727: "Ayutra",
    4154328: "Balî",
    4411772: "Mîlanîa",
    3799853: "Naish",
    4414793: "Narune",
    4463918: "Nedbigbi",
    3799860: "Noirrion",
    4414724: "Thylin",
    3875920: "Vanitas",
    3938887: "Zidina",
    3969334: "Senkai",
    4285787: "Taypsi",
    4446765: "Lavalexi",
    3938880: "Huntjinn",
    4417993: "Inancabi",
    4011638: "Justíce",
    3799864: "Æoreth",
    4413813: "Sneakerz"
}

CHARACTER_NAME_TO_ID = {v: k for k, v in CHARACTER_MAP.items()}

CHARACTER_CLASSES = {
    "Hannox": ("Hunter", "Ranged"),
    "Insebtion": ("Death Knight", "Melee"),
    "Iyásu": ("Shaman", "Heal"),
    "Dengø": ("Paladin", "Melee"),
    "Pudu": ("Paladin", "Heal"),
    "Barrageobamá": ("Demon Hunter", "Melee"),
    "Greenmelt": ("Evoker", "Ranged"),
    "Hugeheals": ("Paladin", "Melee"),
    "Thalvir": ("Death Knight", "Melee"),
    "Akaï": ("Monk", "Melee"),
    "Balest": ("Shaman", "Heal"),
    "Valeeh": ("Priest", "Heal"),
    "Lattenseppi": ("Warrior", "Melee"),
    "Böllercolada": ("Warlock", "Ranged"),
    "Farnis": ("Druid", "Ranged"),
    "Stormi": ("Death Knight", "Tank"),
    "Bloody": ("Warrior", "Melee"),
    "Ayutra": ("Evoker", "Ranged"),
    "Balî": ("Shaman", "Heal"),
    "Mîlanîa": ("Death Knight", "Melee"),
    "Naish": ("Priest", "Ranged"),
    "Narune": ("Druid", "Ranged"),
    "Nedbigbi": ("Death Knight", "Melee"),
    "Noirrion": ("Hunter", "Ranged"),
    "Thylin": ("Monk", "Tank"),
    "Vanitas": ("Mage", "Ranged"),
    "Zidina": ("Shaman", "Ranged"),
    "Senkai": ("Warlock", "Ranged"),
    "Taypsi": ("Priest", "Heal"),
    "Lavalexi": ("Druid", "Heal"),
    "Huntjinn": ("Hunter", "Ranged"),
    "Inancabi": ("Mage", "Ranged"),
    "Justíce": ("Paladin", "Melee"),
    "Æoreth": ("Warrior", "Tank"),
    "Sneakerz": ("Rogue", "Melee")
}

# Group by raid role (based on "role" in data)
CHARACTER_ROLES = {
    "Tanks und Heiler": [
        "Pudu", "Iyásu", "Balest", "Valeeh", "Balî", "Thylin", "Æoreth", "Stormi", "Taypsi", "Lavalexi"
    ],
    "Melees": [
        "Insebtion", "Dengø", "Barrageobamá", "Hugeheals", "Thalvir", "Akaï", "Lattenseppi",
        "Bloody", "Mîlanîa", "Nedbigbi", "Justíce", "Sneakerz"
    ],
    "Ranges": [
        "Hannox", "Greenmelt", "Böllercolada", "Farnis", "Ayutra", "Naish", "Narune", "Noirrion",
        "Vanitas", "Zidina", "Senkai", "Huntjinn", "Inancabi"
    ]
}


# Class colors (hex)
CLASS_HEX_COLORS = {
    "Death Knight": 0xC41F3B,
    "Demon Hunter": 0xA330C9,
    "Druid": 0xFF7D0A,
    "Evoker": 0x33937F,
    "Hunter": 0xABD473,
    "Mage": 0x69CCF0,
    "Monk": 0x00FF96,
    "Paladin": 0xF58CBA,
    "Priest": 0xFFFFFF,
    "Rogue": 0xFFF569,
    "Shaman": 0x0070DE,
    "Warlock": 0x9482C9,
    "Warrior": 0xC79C6E
}

# Class icons
CLASS_ICONS = {
    "Death Knight": "🩸",
    "Demon Hunter": "👿",
    "Druid": "🐻",
    "Evoker": "🐉",
    "Hunter": "🏹",
    "Mage": "❄️",
    "Monk": "🧘",
    "Paladin": "✝️",
    "Priest": "🕊️",
    "Rogue": "🗡️",
    "Shaman": "⚡",
    "Warlock": "💀",
    "Warrior": "⚔️"
}
