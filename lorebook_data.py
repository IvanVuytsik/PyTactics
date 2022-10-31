from settings import *

DOMAIN = [
    "Controls",
    "Global Map",
    "Tactical Map",
    "World Lore",
    "Melee Units",
    "Ranged Units",
    "Support Units",
    "Siege Units",
]

INFO = {
    "Attributes": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/attributes.png', 5 * DOUBLETILE, 3 * DOUBLETILE),
        "desc": """Every character has six attributes\nthat influence combat abilities:
- Health
- Armor
- Might
- Fortitude
- Reflex
- Will\n
Attributes are modified only by \nequipped items and statuses."""},
    "Health": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/0_health.png', FIVETILES, FIVETILES),
        "desc": """Description"""},
    "Armor": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/1_armor.png', FIVETILES, FIVETILES),
        "desc": """Description"""},
    "Might": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/2_might.png', FIVETILES, FIVETILES),
        "desc": """Description"""},
    "Fortitude": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/3_fortitude.png', FIVETILES, FIVETILES),
        "desc": """Description"""},
    "Reflex": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/4_reflex.png', FIVETILES, FIVETILES),
        "desc": """Description"""},
    "Will": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/5_will.png', FIVETILES, FIVETILES),
        "desc": """Description"""},
    "Deflect Attack": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/0_health.png', 5 * DOUBLETILE, 3 * DOUBLETILE),
        "desc": """Description"""},
    "Action Points": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/0_health.png', 5 * DOUBLETILE, 3 * DOUBLETILE),
        "desc": """Description"""},
    "Critical Strike": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/0_health.png', 5 * DOUBLETILE, 3 * DOUBLETILE),
        "desc": """Description"""},
    "Negative Effects": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/statuses.png', 5 * DOUBLETILE, 1.5 * DOUBLETILE),
        "desc": """Negative effects may be inflicted as\na result of combat abilities, spells\nor critical hits. They are categorized
based on applicable resistance -\nFORTITUDE or WILL. Every\nstatus is negated when its effect 
occurs. If resistance roll succeeds, the\nnegative effect is removed. Otherwise\nit will continue until next turn or
until removed by a combat ability.\n 
- FORTITUDE: bleed, blind, poison, 
weak, corrosion, death
- WILL: burn, frost, energy, berserk, 
curse, charm 
"""},
    "Skills": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/0_health.png', 5 * DOUBLETILE, 3 * DOUBLETILE),
        "desc": """Description"""},
    "NPCs": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/0_health.png', 5 * DOUBLETILE, 3 * DOUBLETILE),
        "desc": """Description"""},
    "Points of Interest": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/0_health.png', 5 * DOUBLETILE, 3 * DOUBLETILE),
        "desc": """Description"""},
    "Mission Objectives": {
        "chapter": DOMAIN[2],
        "status": "unlocked",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/0_health.png', 5 * DOUBLETILE, 3 * DOUBLETILE),
        "desc": """Description"""},
}
