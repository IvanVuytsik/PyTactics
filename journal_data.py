from settings import *

CHAPTERS = [
    "Homecoming",
    "Troubles in the Land",
    "Charlatan Kings",
    "Blood and Ink",
    "Burden of The Crown",
    "The Expedition",
    "Games with Snakes",
    "Faith in Ones Hands",
]

#"Path of the Seeker",
#"Path of the Loyalist",
#"Path of the Vagrant"
QUESTS = {
    "A Letter from Afar": {
        "chapter": CHAPTERS[0],
        "desc": import_text("./text/stories/a_letter_from_afar.txt"),
        "image": None,
        "status": "unlocked"},
    "Long Way Home": {
        "chapter": CHAPTERS[0],
        "desc":
            """ - Meet your brother in Eastcliff \n - Collect your belongings 
            """,
        "image": load_image_and_scale("./graphics/stories/1.png", 5 * DOUBLETILE, 3 * DOUBLETILE),
        "status": "unlocked"},
}