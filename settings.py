import random
from importCSV import *
from unit_data import army_lib, unit_lib, squad_lib, unit_id
from skills_data import talent_lib
from items_data import items_lib

from debug import debug

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 32
DOUBLETILE = TILESIZE * 2
HALFTILE = TILESIZE // 2
TRIPLETILE = TILESIZE * 3
QUARTERTILE = TILESIZE // 4
SEMITILE = TILESIZE * 0.75
TILEANDHALF = TILESIZE * 1.5
TILEANDQUARTER = TILESIZE * 1.25
FOURTILES = TILESIZE * 4
FIVETILES = TILESIZE * 5

# ui
TEXT_FONT = './graphics/font/Montserrat-Medium.otf'
TEXT_FONT_Mini = 16
TEXT_FONT_SM = 18
TEXT_FONT_MD = 20
TEXT_FONT_LG = 24

DESC_FONT = './graphics/font/KELMSCOT.ttf'
DESC_FONT_Mini = 18
DESC_FONT_SM = 20
DESC_FONT_MD = 22
DESC_FONT_LG = 24

UI_FONT = './graphics/font/ESKARGOT.ttf'
UI_FONT_SM = 20
UI_FONT_MD = 26
UI_FONT_LG = 32

BAR_HEIGHT = 20
BAR_WIDTH = 100
ITEM_BOX_SIZE = TILESIZE

# ui colors
UI_BG_COLOR = '#404040'
UI_BORDER_COLOR = '#d2a421'
PAPER_COLOR = '#d5bc79'
TEXT_COLOR = '#FFCB42'
BONE_COLOR = '#F2EBE9'
PANEL_COLOR = '#213456'
UI_BORDER_COLOR_ACTIVE = 'gold'

ACTION_PRIMARY = "#712B75"
ACTION_SECONDARY = "#FCF9C6"

SELECTION_COLOR = "#9EB23B"

# map edge color
MAP_EDGE_COLOR = '#192740'

# bar colors
HEALTH_COLOR_NEGATIVE = 'red'
HEALTH_COLOR_POSITIVE = 'green'
EXP_COLOR = 'blue'
BAG_COLOR = '#9b6232'

# upgrade menu colors
TEXT_COLOR_SELECTED = '#192740'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'
BOOK_COLOR = "#3d2622"
LORE_COLOR = "#a92f08"

# import data libs
TALENT_DATA = talent_lib
ITEMS_DATA = items_lib
ARMY_DATA = army_lib
UNIT_DATA = unit_lib
SQUAD_DATA = squad_lib
UNIT_ID = unit_id



def music_manager(theme):
    themes = {
        "map": {
            "file": './sound/exploration.mp3', "volume": 0.05, "loop": -1
        },
        "menu":  {
            "file": './sound/menu.mp3', "volume": 0.1, "loop": -1
        },
        "battle_0":  {
            "file": f'./sound/battle_0.mp3', "volume": 0.05, "loop": -1
        },
        "battle_1":  {
            "file": f'./sound/battle_1.mp3', "volume": 0.05, "loop": -1
        },
        "battle_2":  {
            "file": f'./sound/battle_2.mp3', "volume": 0.05, "loop": -1
        },
        "ambush":  {
            "file": './sound/assassins.mp3', "volume": 0.05, "loop": -1
        },
    }
    pygame.mixer.music.load(themes[theme]["file"])
    pygame.mixer.music.set_volume(themes[theme]["volume"])
    pygame.mixer.music.play(loops=themes[theme]["loop"])


def calculate_mouse_pos(pure=True):
    mouse_pos = pygame.mouse.get_pos()
    pos_x = mouse_pos[0] // TILESIZE
    pos_y = mouse_pos[1] // TILESIZE
    return mouse_pos if pure else pos_x, pos_y


def show_info(surface, information, font, color, x, y,
              layout=False, layout_primary=MAP_EDGE_COLOR, layout_secondary=TEXT_COLOR):
    info_surf = font.render(str(information), False, color)
    info_rect = info_surf.get_rect(topleft=(x, y))
    if layout:
        pygame.draw.rect(surface, layout_primary, info_rect)
        pygame.draw.rect(surface, layout_secondary, info_rect, 3)
    surface.blit(info_surf, info_rect)


def draw_story(display_surface, text, font, x, y, spacing):
    message_list = []
    line_spacing = 0
    for line in text.split('\n'):
        message = font.render(line, True, BOOK_COLOR)
        message_list.append(message)
        line_spacing += spacing
        display_surface.blit(message, (x, y + line_spacing))


UI_ElEMENTS = {
    'coinbag': load_image("./graphics/ui/coinbag.png"),
    'questbook': load_image_and_scale("./graphics/ui/questbook.png", 14 * DOUBLETILE, 9 * DOUBLETILE),
    'lorebook': load_image_and_scale("./graphics/ui/lorebook.png", 14 * DOUBLETILE, 9 * DOUBLETILE),
    'map': load_image_and_scale("./graphics/map/map.png", 16 * DOUBLETILE, 8.5 * DOUBLETILE),
    'booksection': load_image_and_scale("./graphics/ui/booksection.png", 1.5 * DOUBLETILE, 2 * DOUBLETILE),
    'victory_icon': load_image_and_scale("./graphics/ui/victory_icon.png", TILESIZE, TILESIZE),
    'defense_icon': load_image_and_scale("./graphics/ui/defmode_icon.png", HALFTILE, HALFTILE),
    'offense_icon': load_image_and_scale("./graphics/ui/aggr_icon.png", HALFTILE, HALFTILE),
    'patrol_icon': load_image_and_scale("./graphics/ui/patrol_icon.png", HALFTILE, HALFTILE),
    'explore': load_image_and_scale("./graphics/ui/explore.png", TILESIZE, TILESIZE),
    'explore_location': load_image_and_scale("./graphics/ui/explore_location.png", TILESIZE, TILESIZE),
}

BANNERS = {
    0: load_image_and_scale("./graphics/banners/03.png", TILESIZE, TRIPLETILE),
    1: load_image_and_scale("./graphics/banners/02.png", TILESIZE, TRIPLETILE),
    2: load_image_and_scale("./graphics/banners/01.png", TILESIZE, TRIPLETILE),
    3: load_image_and_scale("./graphics/banners/00.png", TILESIZE, TRIPLETILE),
}


LIBRARY = {
    "health": {
        "desc": "Health. Character will become unconscious if this indicator drops to 0.",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/0_health.png', DOUBLETILE, DOUBLETILE)},
    "armor": {
        "desc": "Armor. Takes a share of damage instead of Health. The exact share is defined by Fortitude.",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/1_armor.png', DOUBLETILE, DOUBLETILE)},
    "might": {
        "desc": "Might. Power of standard melee and ranged attacks.",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/2_might.png', DOUBLETILE, DOUBLETILE)},
    "fortitude": {
        "desc": "Fortitude. Efficiency of using armor and resistance to body afflictions such as "
                "weakness, poison, corrode, bleeding or blind.",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/3_fortitude.png', DOUBLETILE, DOUBLETILE)},
    "reflex": {
        "desc": "Reflex. Speed of actions and chance to dodge or deflect attacks.",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/4_reflex.png', DOUBLETILE, DOUBLETILE)},
    "will": {
        "desc": "Will. Resistance to elemental and mind afflictions such as fire, frost, energy, "
                "curse, bloodthirsty or charm.",
        "image": load_image_and_scale('./graphics/ui/inventory_icons/5_will.png', DOUBLETILE, DOUBLETILE)},
}


SOUND_BANK = {
    'blade': pygame.mixer.Sound('./sound/effects/blade.wav'),
    'arrow': pygame.mixer.Sound('./sound/effects/arrow.wav'),
    'axe': pygame.mixer.Sound('./sound/effects/axe.wav'),
    'blunt': pygame.mixer.Sound('./sound/effects/blunt.wav'),
    'block': pygame.mixer.Sound('./sound/effects/block.wav'),
    'explosion': pygame.mixer.Sound('./sound/effects/bomb.wav'),
    'snarl': pygame.mixer.Sound('./sound/effects/snarl.wav'),
    'roar': pygame.mixer.Sound('./sound/effects/roar.wav'),
    'bubbles': pygame.mixer.Sound('./sound/effects/bubbles.wav'),
    'acid': pygame.mixer.Sound('./sound/effects/acid.wav'),
    'catapult': pygame.mixer.Sound('./sound/effects/catapult.wav'),
    'flame': pygame.mixer.Sound('./sound/effects/flame.wav'),
    'burn': pygame.mixer.Sound('./sound/effects/burn.wav'),
    'ice': pygame.mixer.Sound('./sound/effects/ice.wav'),
    'energy': pygame.mixer.Sound('./sound/effects/energy.wav'),
    'dream': pygame.mixer.Sound('./sound/effects/dream.wav'),
    'waterdrop': pygame.mixer.Sound('./sound/effects/waterdrop.wav'),
    'spell': pygame.mixer.Sound('./sound/effects/spell.wav'),
    'sword': pygame.mixer.Sound('./sound/effects/sword.wav'),
    'longsword': pygame.mixer.Sound('./sound/effects/longsword.wav'),
    'rapier': pygame.mixer.Sound('./sound/effects/rapier.wav'),
    'coins': pygame.mixer.Sound('./sound/effects/coins.wav'),
    'chorus': pygame.mixer.Sound('./sound/effects/chorus.wav'),
    'bomb': pygame.mixer.Sound('./sound/effects/bomb.wav'),
    'healing': pygame.mixer.Sound('./sound/effects/healing.wav'),
    'leveup': pygame.mixer.Sound('./sound/effects/levelUp.wav'),
    'locked': pygame.mixer.Sound('./sound/effects/locked.wav'),
    'page': pygame.mixer.Sound('./sound/effects/page.wav'),
    'openpotion': pygame.mixer.Sound('./sound/effects/openPotion.wav'),
    'glass': pygame.mixer.Sound('./sound/effects/potionBreak.wav'),
    'scroll': pygame.mixer.Sound('./sound/effects/scroll.wav'),
    'openchest': pygame.mixer.Sound('./sound/effects/openChest.wav'),
    'take': pygame.mixer.Sound('./sound/effects/take.wav'),
    'trap': pygame.mixer.Sound('./sound/effects/trap.wav'),
    'tavern': pygame.mixer.Sound('./sound/effects/tavern.wav'),
    'trader': pygame.mixer.Sound('./sound/effects/trader.wav'),
    'smith': pygame.mixer.Sound('./sound/effects/smith.wav'),
    'alchemy': pygame.mixer.Sound('./sound/effects/alchemy.wav'),
    'port': pygame.mixer.Sound('./sound/effects/port.wav'),
    'town': pygame.mixer.Sound('./sound/effects/town.wav'),
    'ruined': pygame.mixer.Sound('./sound/effects/ruined.wav'),
}



STATUS = {
    'bleeding': {'image': load_image_and_scale("./graphics/ui/status/bleed.png", HALFTILE, HALFTILE),
                 'effect': ['health'], 'power': 10, 'timer': 1, 'duration': 100, 'resistance': 'fortitude',
                 'sound': 'waterdrop'
                 },
    'blinded': {'image': load_image_and_scale("./graphics/ui/status/blinded.png", HALFTILE, HALFTILE),
                'effect': ['action_points'], 'power': 100, 'timer': 1, 'duration': 300, 'resistance': 'fortitude',
                'sound': 'waterdrop'
                },
    'poisoned': {'image': load_image_and_scale("./graphics/ui/status/poison.png", HALFTILE, HALFTILE),
                 'effect': ['health'], 'power': 5, 'timer': 1, 'duration': 100, 'resistance': 'fortitude',
                 'sound': 'bubbles'
                 },
    'weakened': {'image': load_image_and_scale("./graphics/ui/status/weakness.png", HALFTILE, HALFTILE),
                 'effect': ['fortitude', 'might'], 'power': 3, 'timer': 1, 'duration': 500, 'resistance': 'fortitude',
                 'sound': 'dream'
                 },
    'corrosion': {'image': load_image_and_scale("./graphics/ui/status/corrosion.png", HALFTILE, HALFTILE),
                  'effect': ['armor'], 'power': 20, 'timer': 1, 'duration': 100, 'resistance': 'fortitude',
                  'sound': 'acid'
                  },
    'dying': {'image': load_image_and_scale("./graphics/ui/status/deathmark.png", HALFTILE, HALFTILE),
              'effect': ['health'], 'power': 1000, 'timer': 0.1, 'duration': 1000, 'resistance': 'fortitude',
              'sound': 'spell'
              },
    'bloodthirsty': {'image': load_image_and_scale("./graphics/ui/status/bloodthirst.png", HALFTILE, HALFTILE),
                     'effect': ['faction'], 'power': 3, 'timer': 1, 'duration': 300, 'resistance': 'will',
                     'sound': 'spell'
                     },
    'burning': {'image': load_image_and_scale("./graphics/ui/status/burn.png", HALFTILE, HALFTILE),
                'effect': ['health'], 'power': 5, 'timer': 1, 'duration': 100, 'resistance': 'will',
                'sound': 'flame'
                },
    'cursed': {'image': load_image_and_scale("./graphics/ui/status/curse.png", HALFTILE, HALFTILE),
               'effect': ['will', 'reflex'], 'power': 3, 'timer': 1, 'duration': 500, 'resistance': 'will',
               'sound': 'spell'
               },
    'electrified': {'image': load_image_and_scale("./graphics/ui/status/electrical.png", HALFTILE, HALFTILE),
                    'effect': ['health', 'armor'], 'power': 10, 'timer': 1, 'duration': 300, 'resistance': 'will',
                    'sound': 'energy'
                    },
    'frozen': {'image': load_image_and_scale("./graphics/ui/status/frost.png", HALFTILE, HALFTILE),
               'effect': ['health', 'action_points'], 'power': 10, 'timer': 1, 'duration': 300, 'resistance': 'will',
               'sound': 'ice'
               },
    'confused': {'image': load_image_and_scale("./graphics/ui/status/mindspell.png", HALFTILE, HALFTILE),
                 'effect': ['faction'], 'power': 0, 'timer': 1, 'duration': 1000, 'resistance': 'will',
                 'sound': 'dream'
                 },
}