# wow_data.py

# Character data from provided list
CHARACTER_MAP = {
    4343606: "Hannox",
    4509395: "Insebtion",
    4509392: "Iyásu",
    3938881: "Dengø",
    4342796: "Pudu",
    4509469: "Greenmelt",
    4389535: "Hugeheals",
    4509394: "Thalvir",
    4225318: "Akaï",
    4339466: "Balest",
    4511399: "Eichelherr",
    4511400: "Jozsef",
    4511392: "Qlaun",
    4330503: "Valeeh",
    4397102: "Lattenseppi",
    4157476: "Böllercolada",
    4509473: "Farnis",
    3938886: "Stormi",
    4509467: "Bloody",
    4154328: "Balî",
    4507210: "Hyutra",
    3799853: "Naish",
    4414793: "Narune",
    4463918: "Nedbigbi",
    4509466: "Noirrion",
    4500257: "Sorfilia",
    4414724: "Thylin",
    4509246: "Vanitas",
    3938887: "Zidina",
    4505701: "Soriba",
    3969334: "Senkai",
    4285787: "Taypsi",
    4509393: "Lavalexi",
    3938880: "Huntjinn",
    4011638: "Justíce",
    4509470: "Kraftbrühe",
    4505171: "Zilas",
    4509248: "Æoreth",
    4413813: "Sneakerz"
}

CHARACTER_NAME_TO_ID = {v: k for k, v in CHARACTER_MAP.items()}

CHARACTER_CLASSES = {
    "Hannox": ("Hunter", "Ranged"),
    "Insebtion": ("Death Knight", "Melee"),
    "Iyásu": ("Shaman", "Heal"),
    "Dengø": ("Paladin", "Melee"),
    "Pudu": ("Paladin", "Heal"),
    "Greenmelt": ("Evoker", "Ranged"),
    "Hugeheals": ("Paladin", "Melee"),
    "Thalvir": ("Death Knight", "Melee"),
    "Akaï": ("Monk", "Melee"),
    "Balest": ("Shaman", "Heal"),
    "Eichelherr": ("Druid", "Ranged"),
    "Jozsef": ("Rogue", "Melee"),
    "Qlaun": ("Warlock", "Ranged"),
    "Valeeh": ("Priest", "Heal"),
    "Lattenseppi": ("Warrior", "Melee"),
    "Böllercolada": ("Warlock", "Ranged"),
    "Farnis": ("Druid", "Ranged"),
    "Stormi": ("Death Knight", "Melee"),
    "Bloody": ("Warrior", "Melee"),
    "Balî": ("Shaman", "Heal"),
    "Hyutra": ("Mage", "Ranged"),
    "Naish": ("Priest", "Ranged"),
    "Narune": ("Druid", "Ranged"),
    "Nedbigbi": ("Death Knight", "Melee"),
    "Noirrion": ("Hunter", "Ranged"),
    "Sorfilia": ("Demon Hunter", "Melee"),
    "Thylin": ("Monk", "Tank"),
    "Vanitas": ("Mage", "Ranged"),
    "Zidina": ("Shaman", "Ranged"),
    "Soriba": ("Druid", "Melee"),
    "Senkai": ("Warlock", "Ranged"),
    "Taypsi": ("Priest", "Heal"),
    "Lavalexi": ("Druid", "Heal"),
    "Huntjinn": ("Hunter", "Ranged"),
    "Justíce": ("Paladin", "Melee"),
    "Kraftbrühe": ("Paladin", "Melee"),
    "Zilas": ("Demon Hunter", "Melee"),
    "Æoreth": ("Warrior", "Tank"),
    "Sneakerz": ("Rogue", "Melee")
}

# Group by raid role (based on "role" in data)
CHARACTER_ROLES = {
    "Tanks und Heiler": [
        "Pudu", "Iyásu", "Balest", "Valeeh", "Balî", "Thylin", "Æoreth",
        "Taypsi", "Lavalexi"
    ],
    "Melees": [
        "Insebtion", "Dengø", "Hugeheals", "Thalvir", "Akaï", "Lattenseppi",
        "Bloody", "Nedbigbi", "Sorfilia", "Justíce", "Kraftbrühe", "Zilas",
        "Sneakerz", "Jozsef", "Soriba", "Stormi"
    ],
    "Ranges": [
        "Hannox", "Greenmelt", "Eichelherr", "Qlaun", "Böllercolada", "Farnis",
        "Hyutra", "Naish", "Narune", "Noirrion", "Vanitas", "Zidina",
        "Senkai", "Huntjinn"
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
