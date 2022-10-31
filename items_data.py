from importCSV import load_image

items_lib = {
    "Leather Armor": {
        "health": 0, "armor": 20, "might": 0, "fortitude": 6, "reflex": 1, "will": 0,
        "cost": 450, "type": "armor",
        "image": load_image("./graphics/items/leatherarmor.png")
    },
    "Gambeson": {
        "health": 10, "armor": 30, "might": 0, "fortitude": 8, "reflex": 3, "will": 0,
        "cost": 750, "type": "armor",
        "image": load_image("./graphics/items/gambeson.png")
    },
    "Night Armor": {
        "health": 0, "armor": 30, "might": 0, "fortitude": 6, "reflex": 6, "will": 0,
        "cost": 900, "type": "armor",
        "image": load_image("./graphics/items/nightarmor.png")
    },
    "Captain Armor": {
        "health": 20, "armor": 40, "might": 0, "fortitude": 10, "reflex": 3, "will": 5,
        "cost": 2750, "type": "armor",
        "image": load_image("./graphics/items/captainarmor.png")
    },
    "Black Plate": {
        "health": 30, "armor": 120, "might": 0, "fortitude": 25, "reflex": -10, "will": 0,
        "cost": 5000, "type": "armor",
        "image": load_image("./graphics/items/blackplate.png")
    },
    "Crimson Armor": {
        "health": 25, "armor": 80, "might": 0, "fortitude": 20, "reflex": -5, "will": 5,
        "cost": 3000, "type": "armor",
        "image": load_image("./graphics/items/crimsonarmor.png")
    },
    "Robe": {
        "health": 0, "armor": 10, "might": 0, "fortitude": 3, "reflex": 1, "will": 3,
        "cost": 250, "type": "armor",
        "image": load_image("./graphics/items/robe.png")
    },
    "Magi Robe": {
        "health": 20, "armor": 20, "might": 0, "fortitude": 6, "reflex": 3, "will": 12,
        "cost": 1700, "type": "armor",
        "image": load_image("./graphics/items/magirobe.png")
    },
    "Night Cloak": {
        "health": 0, "armor": 5, "might": 0, "fortitude": 1, "reflex": 3, "will": 6,
        "cost": 750, "type": "cloak",
        "image": load_image("./graphics/items/nightcloak.png")
    },
    "Leather Gloves": {
        "health": 0, "armor": 5, "might": 0, "fortitude": 3, "reflex": 1, "will": 0,
        "cost": 250, "type": "gloves",
        "image": load_image("./graphics/items/leathergloves.png")
    },
    "Forest Gloves": {
        "health": 0, "armor": 10, "might": 2, "fortitude": 2, "reflex": 2, "will": 0,
        "cost": 650, "type": "gloves",
        "image": load_image("./graphics/items/forestgloves.png")
    },
    "Dragon Claws": {
        "health": 10, "armor": 25, "might": 10, "fortitude": 6, "reflex": 1, "will": 0,
        "cost": 2500, "type": "gloves",
        "image": load_image("./graphics/items/dradonclaws.png")
    },
    "Leather Boots": {
        "health": 0, "armor": 5, "might": 0, "fortitude": 3, "reflex": 1, "will": 0,
        "cost": 250, "type": "boots",
        "image": load_image("./graphics/items/leatherboots.png")
    },
    "Raider Helmet": {
        "health": 0, "armor": 5, "might": 0, "fortitude": 3, "reflex": 1, "will": 0,
        "cost": 250, "type": "helmet",
        "image": load_image("./graphics/items/raiderhelmet.png")
    },
    "Silver Amulet": {
        "health": 10, "armor": 0, "might": 0, "fortitude": 0, "reflex": 0, "will": 1,
        "cost": 350, "type": "amulet",
        "image": load_image("./graphics/items/silveramulet.png")
    },
    "Bloodstone": {
        "health": 40, "armor": 0, "might": 0, "fortitude": 4, "reflex": 0, "will": 0,
        "cost": 2000, "type": "amulet",
        "image": load_image("./graphics/items/bloodstone.png")
    },
    "Crystal Ring": {
        "health": 0, "armor": 0, "might": 0, "fortitude": 0, "reflex": 0, "will": 20,
        "cost": 1750, "type": "ring",
        "image": load_image("./graphics/items/crystalring.png")
    },
    "Commander Ring": {
        "health": 10, "armor": 10, "might": 3, "fortitude": 3, "reflex": 3, "will": 3,
        "cost": 2500, "type": "ring",
        "image": load_image("./graphics/items/leaderring.png")
    },
    "Common Ring": {
        "health": 5, "armor": 5, "might": 0, "fortitude": 0, "reflex": 0, "will": 0,
        "cost": 300, "type": "ring",
        "image": load_image("./graphics/items/ring.png")
    },
    "Ring of Defence": {
        "health": 0, "armor": 12, "might": 0, "fortitude": 3, "reflex": 1, "will": 0,
        "cost": 900, "type": "ring",
        "image": load_image("./graphics/items/ringofdefence.png")
    },
    "Wooden Shield": {
        "health": 0, "armor": 10, "might": 0, "fortitude": 10, "reflex": 3, "will": 0,
        "cost": 500, "type": "shield",
        "image": load_image("./graphics/items/woodenshield.png")
    },
    "Crimson Buckler": {
        "health": 0, "armor": 25, "might": 0, "fortitude": 15, "reflex": 3, "will": 5,
        "cost": 1200, "type": "shield",
        "image": load_image("./graphics/items/crimsonbuckler.png")
    },
    "Hunting Knife": {
        "health": 0, "armor": 0, "might": 10, "fortitude": 0, "reflex": 0, "will": 0,
        "cost": 500, "type": "weapon",
        "image": load_image("./graphics/items/huntingknife.png")
    },
    "Ambush Bow": {
        "health": 0, "armor": 0, "might": 15, "fortitude": 0, "reflex": 0, "will": 0,
        "cost": 750, "type": "bow",
        "image": load_image("./graphics/items/ambushbow.png")
    },
    "Crimson Bow": {
        "health": 10, "armor": 0, "might": 30, "fortitude": 0, "reflex": 0, "will": 0,
        "cost": 2250, "type": "bow",
        "image": load_image("./graphics/items/crimsonbow.png")
    },
    "Wand": {
        "health": 0, "armor": 0, "might": 15, "fortitude": 0, "reflex": 0, "will": 5,
        "cost": 650, "type": "wand",
        "image": load_image("./graphics/items/wand.png")
    },
    "Gold": {
        "health": 0, "armor": 0, "might": 0, "fortitude": 0, "reflex": 0, "will": 0,
        "cost": 250, "type": "misc",
        "image": load_image("./graphics/items/bagofgold.png")
    },
    "Coins": {
        "health": 0, "armor": 0, "might": 0, "fortitude": 0, "reflex": 0, "will": 0,
        "cost": 50, "type": "misc",
        "image": load_image("./graphics/items/gold.png")
    },
    "Evercoin": {
        "health": 0, "armor": 0, "might": 0, "fortitude": 0, "reflex": 2, "will": 2,
        "cost": 700, "type": "trinket",
        "image": load_image("./graphics/items/evercoin.png")
    },
    "Bottomless Mug": {
        "health": 0, "armor": 20, "might": 10, "fortitude": 10, "reflex": -5, "will": -10,
        "cost": 1200, "type": "trinket",
        "image": load_image("./graphics/items/mug.png")
    },
    "Firebird Feather": {
        "health": 0, "armor": 0, "might": 0, "fortitude": 0, "reflex": 0, "will": 6,
        "cost": 850, "type": "trinket",
        "image": load_image("./graphics/items/firebirdfeather.png")
    },
    "Symbol of Peace": {
        "health": 0, "armor": 0, "might": 0, "fortitude": 0, "reflex": 0, "will": 3,
        "cost": 300, "type": "trinket",
        "image": load_image("./graphics/items/symbolofpeace.png")
    },
    "Clover": {
        "health": 0, "armor": 0, "might": 1, "fortitude": 1, "reflex": 1, "will": 1,
        "cost": 600, "type": "trinket",
        "image": load_image("./graphics/items/clover.png")
    },
    "Lucky Horseshoe": {
        "health": 0, "armor": 0, "might": 0, "fortitude": 0, "reflex": 3, "will": 0,
        "cost": 500, "type": "trinket",
        "image": load_image("./graphics/items/horseshoe.png")
    },
    "Lamp": {
        "health": 10, "armor": 10, "might": 5, "fortitude": 5, "reflex": 5, "will": -20,
        "cost": 2350, "type": "trinket",
        "image": load_image("./graphics/items/lamp.png")
    },
    "Flute": {
        "health": 0, "armor": 0, "might": 0, "fortitude": 0, "reflex": 3, "will": 3,
        "cost": 850, "type": "trinket",
        "image": load_image("./graphics/items/flute.png")
    },
    "Sextant": {
        "health": 0, "armor": 0, "might": 0, "fortitude": 4, "reflex": 0, "will": 4,
        "cost": 800, "type": "trinket",
        "image": load_image("./graphics/items/sextant.png")
    },
    "Taro Cards": {
        "health": 10, "armor": 0, "might": 4, "fortitude": 4, "reflex": 2, "will": -5,
        "cost": 1400, "type": "trinket",
        "image": load_image("./graphics/items/tarocards.png")
    },
    "Alchemist Heart": {
        "health": 30, "armor": 0, "might": 0, "fortitude": 3, "reflex": 0, "will": 0,
        "cost": 1200, "type": "trinket",
        "image": load_image("./graphics/items/magicheart.png")
    },
    "Vitality Potion": {
        "health": 15, "armor": 0, "might": 0, "fortitude": 1, "reflex": 0, "will": 0,
        "cost": 600, "type": "trinket",
        "image": load_image("./graphics/items/vitalitypotion.png")
    },

}