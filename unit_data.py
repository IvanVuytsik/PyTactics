from importCSV import load_image

army_lib = {
    'melee': {
        'Militia': {'requirement': 1, 'activate': 20, 'cost': 500, 'unlocked': False,
                    'description': f'Militia. Basic melee troops with light armor and weapons.',
                    'img': load_image('./graphics/ui/troops_icons/militia.png')},
        'Infantry': {'requirement': 2, 'activate': 25, 'cost': 1000, 'unlocked': False,
                     'description': 'Infantry. Regular melee troops with versatile equipment and good defence.',
                     'img': load_image('./graphics/ui/troops_icons/infantry.png')},
        'Heavy Infantry': {'requirement': 3, 'activate': 30, 'cost': 1500, 'unlocked': False,
                           'description': 'Heavy Infantry. Professional, well trained and equipped soldiers.',
                           'img': load_image('./graphics/ui/troops_icons/heavy_infantry.png')},
        'Temple Guards': {'requirement': 4, 'activate': 35, 'cost': 2000, 'unlocked': False,
                          'description': 'Temple Guards. Heavy melee troops trained in arcane arts.',
                          'img': load_image('./graphics/ui/troops_icons/temple_guards.png')},
    },
    'ranged': {
        'Archers': {'requirement': 1, 'activate': 20, 'cost': 500, 'unlocked': False,
                    'description': 'Archers. Basic ranged troops with light armor and bows.',
                    'img': load_image('./graphics/ui/troops_icons/archers.png')},
        'Crossbowmen': {'requirement': 2, 'activate': 25, 'cost': 750, 'unlocked': False,
                        'description': 'Crossbowmen. Regular ranged troops with good protection and powerful weapons.',
                        'img': load_image('./graphics/ui/troops_icons/crossbowmen.png')},
        'Arcane Shooters': {'requirement': 3, 'activate': 30, 'cost': 1500, 'unlocked': False,
                            'description': 'Arcane Shooters. Ranged troops that apply arcane effects to their arrows.',
                            'img': load_image('./graphics/ui/troops_icons/arcane_archer.png')},
        'Mystics': {'requirement': 4, 'activate': 35, 'cost': 2000, 'unlocked': False,
                    'description': 'Mystics. Ranged troops specifically trained in arcane and elemental arts.',
                    'img': load_image('./graphics/ui/troops_icons/mystics.png')},
    },
    'riders': {
        'Horsemen': {'requirement': 1, 'activate': 20, 'cost': 1000, 'unlocked': False,
                     'description': 'Horsemen. Basic cavalry troops with light protection and weapons.',
                     'img': load_image('./graphics/ui/troops_icons/horsemen.png')},
        'Knights': {'requirement': 2, 'activate': 25, 'cost': 1500, 'unlocked': False,
                    'description': 'Knights. Regular cavalry troops with good armor and weapons.',
                    'img': load_image('./graphics/ui/troops_icons/knights.png')},
        'Champions': {'requirement': 3, 'activate': 30, 'cost': 2000, 'unlocked': False,
                      'description': 'Champions. Shock cavalry troops clad in heavy armor and wielding lances.',
                      'img': load_image('./graphics/ui/troops_icons/champions.png')},
        'Paladins': {'requirement': 4, 'activate': 40, 'cost': 3000, 'unlocked': False,
                     'description': 'Paladins. Heavy cavalry troops trained to handle both weapons and arcane.',
                     'img': load_image('./graphics/ui/troops_icons/paladins.png')},
    },
    'support': {
        'Scouts': {'requirement': 1, 'activate': 15, 'cost': 500, 'unlocked': True,
                   'description': 'Scouts. Versatile support troops using both melee and ranged weapons.',
                   'img': load_image('./graphics/ui/troops_icons/scouts.png')},
        'Priests': {'requirement': 2, 'activate': 20, 'cost': 750, 'unlocked': False,
                    'description': 'Priests. They use divine arts to support allies and rely on temple '
                                   'brothers for protection.',
                    'img': load_image('./graphics/ui/troops_icons/priests.png')},
        'Alchemists': {'requirement': 3, 'activate': 25, 'cost': 1500, 'unlocked': False,
                       'description': 'Alchemists. They use potions to summon constructs or affect enemies and allies.',
                       'img': load_image('./graphics/ui/troops_icons/alchemists.png')},
        'Beast Lords': {'requirement': 4, 'activate': 30, 'cost': 2000, 'unlocked': False,
                        'description': 'Beast Lords. A nomadic tribe of monster tamers, warriors and hunters.',
                        'img': load_image('./graphics/ui/troops_icons/beast_lords.png')},
    },
    'siege': {
        'Handthorn': {'requirement': 1, 'activate': 20, 'cost': 750, 'unlocked': False,
                      'description': 'Handthorn. Basic mobile engine similar to a crossbow with heavier projectiles.',
                      'img': load_image('./graphics/ui/troops_icons/handthorn.png')},
        'Lancethrower': {'requirement': 2, 'activate': 25, 'cost': 1500, 'unlocked': False,
                         'description': 'Lancethrower. Siege engine intended for long range attacks of enemy troops.',
                         'img': load_image('./graphics/talents/5.png')},
        'Stonebarrel': {'requirement': 3, 'activate': 30, 'cost': 2000, 'unlocked': False,
                        'description': 'Stonebarrel. Siege engine capable of launching heavy objects.',
                        'img': load_image('./graphics/ui/troops_icons/stonebarrel.png')},
        'Longarm': {'requirement': 4, 'activate': 35, 'cost': 3000, 'unlocked': False,
                    'description': 'Longarm. Siege engine created for breaking protected defences like walls.',
                    'img': load_image('./graphics/talents/5.png')},
    },
}

squad_lib = {"Scouts": {'scout': 4, 'journeyman': 2},
             "Militia": {'militia': 8, 'pikeman': 4},
             "Infantry": {'swordsman': 6, 'helbardier': 3, 'maceman': 3},
             "Heavy Infantry": {'footknight': 6, 'linebreaker': 4},
             "Archers": {'archer': 4, 'marksman': 2},
             "Crossbowmen": {'crossbowman': 6},
             "Horsemen": {'horseman': 6},
             "Knights": {'knight': 6},
             }

unit_id = {
    0: "rowan", 1: "dreadknight", 2: "blackwolf", 3: "bowman", 4: "brigand",
    5: "horseman", 6: "crossbowman", 7: "dunstan", 8: "executioner", 9: "sellsword",
    10: "spearman", 11: "mercenary", 12: "linebreaker", 13: "footknight",
    14: "marksman", 15: "militia", 16: "thief", 17: "knight", 18: "archer",
    19: "scout", 20: "journeyman", 21: "severin", 22: "pikeman", 23: "swordsman",
    24: "thug", 25: "helbardier", 26: "wizard", 27: "wolf", 28: "maceman",
    29: "blademaster",
}

unit_lib = {
    "rowan": {
        "health": 100, "armor": 0, "will": 10, "might": 10,
        "reflex": 10, "fortitude": 10, "speed": 1, "range": 10, 'size': 'normal',
        "notice": 200, "weapon": "blade", "special_effect": "bleeding"
    },
    "dunstan": {
        "health": 200, "armor": 0, "will": 0, "might": 20,
        "reflex": 0, "fortitude": 10, "speed": 1, "range": 10, 'size': 'normal',
        "notice": 200, "weapon": "longsword", "special_effect": "bleeding"
    },
    "regina": {
        "health": 100, "armor": 0, "will": 5, "might": 20,
        "reflex": 10, "fortitude": 5, "speed": 1, "range": 200, 'size': 'normal',
        "notice": 200, "weapon": "arrow", "special_effect": "poisoned"
    },
    "anselm": {
        "health": 200, "armor": 0, "will": 5, "might": 20,
        "reflex": 0, "fortitude": 5, "speed": 1, "range": 10, 'size': 'normal',
        "notice": 200, "weapon": "blunt", "special_effect": "weakened"
    },
    "alba": {
        "health": 100, "armor": 0, "will": 20, "might": 10,
        "reflex": 10, "fortitude": 0, "speed": 1, "range": 200, 'size': 'normal',
        "notice": 200, "weapon": "ice", "special_effect": "frozen"
    },
    "severin": {
        "health": 100, "armor": 0, "will": 20, "might": 20,
        "reflex": 0, "fortitude": 0, "speed": 1, "range": 300, 'size': 'normal',
        "notice": 300, "weapon": "flame", "special_effect": "burning"
    },
    "bowman": {"health": 50, "armor": 20, "will": 5, "might": 20,
               "reflex": 20, "fortitude": 20, "speed": 1, 'range': 200, 'size': 'normal',
               "notice": 200, "weapon": "arrow", "special_effect": "bleeding"
               },
    "archer": {"health": 60, "armor": 30, "will": 5, "might": 25,
               "reflex": 30, "fortitude": 40, "speed": 1, 'range': 200, 'size': 'normal',
               "notice": 200, "weapon": "arrow", "special_effect": "bleeding"
               },
    "marksman": {"health": 80, "armor": 40, "will": 5, "might": 30,
                 "reflex": 45, "fortitude": 50, "speed": 1, 'range': 200, 'size': 'normal',
                 "notice": 200, "weapon": "arrow", "special_effect": "blinded"
                 },
    "crossbowman": {"health": 100, "armor": 60, "will": 10, "might": 40,
                    "reflex": 10, "fortitude": 40, "speed": 1, 'range': 200, 'size': 'normal',
                    "notice": 200, "weapon": "arrow", "special_effect": "bleeding"
                    },
    "journeyman": {"health": 70, "armor": 30, "will": 10, "might": 25,
                   "reflex": 40, "fortitude": 50, "speed": 1, 'range': 200, 'size': 'normal',
                   "notice": 200, "weapon": "arrow", "special_effect": "bleeding"
                   },
    "wizard": {"health": 120, "armor": 300, "will": 60, "might": 55,
               "reflex": 20, "fortitude": 100, "speed": 1, 'range': 200, 'size': 'normal',
               "notice": 200, "weapon": "spell", "special_effect": "cursed"
               },
    "militia": {"health": 70, "armor": 40, "will": 5, "might": 25,
                "reflex": 15, "fortitude": 25, "speed": 1, 'range': 10, 'size': 'normal',
                "notice": 200, "weapon": "blade", "special_effect": "bleeding"
                },
    "pikeman": {"health": 60, "armor": 30, "will": 5, "might": 25,
                "reflex": 25, "fortitude": 30, "speed": 1, 'range': 40, 'size': 'normal',
                "notice": 200, "weapon": "blade", "special_effect": "bleeding"
                },
    "spearman": {"health": 80, "armor": 60, "will": 5, "might": 30,
                 "reflex": 40, "fortitude": 55, "speed": 1, 'range': 20, 'size': 'normal',
                 "notice": 200, "weapon": "blade", "special_effect": "bleeding"
                 },
    "scout": {"health": 90, "armor": 40, "will": 10, "might": 30,
              "reflex": 35, "fortitude": 50, "speed": 1, 'range': 20, 'size': 'normal',
              "notice": 200, "weapon": "blade", "special_effect": "bleeding"
              },
    "mercenary": {"health": 90, "armor": 60, "will": 5, "might": 30,
                  "reflex": 20, "fortitude": 40, "speed": 1, 'range': 10, 'size': 'normal',
                  "notice": 200, "weapon": "sword", "special_effect": "bleeding"
                  },
    "blademaster": {"health": 120, "armor": 90, "will": 10, "might": 45,
                    "reflex": 30, "fortitude": 60, "speed": 1, 'range': 20, 'size': 'normal',
                    "notice": 200, "weapon": "longsword", "special_effect": "bleeding"
                    },
    "sellsword": {"health": 100, "armor": 80, "will": 10, "might": 40,
                  "reflex": 25, "fortitude": 60, "speed": 1, 'range': 10, 'size': 'normal',
                  "notice": 200, "weapon": "sword", "special_effect": "bleeding"
                  },
    "thug": {"health": 80, "armor": 30, "will": 5, "might": 35,
             "reflex": 10, "fortitude": 30, "speed": 1, 'range': 10, 'size': 'normal',
             "notice": 200, "weapon": "axe", "special_effect": "bleeding"
             },
    "brigand": {"health": 50, "armor": 30, "will": 5, "might": 25,
                "reflex": 15, "fortitude": 25, "speed": 1, 'range': 10, 'size': 'normal',
                "notice": 200, "weapon": "axe", "special_effect": "bleeding"
                },
    "thief": {"health": 80, "armor": 40, "will": 5, "might": 30,
              "reflex": 40, "fortitude": 50, "speed": 1, 'range': 10, 'size': 'normal',
              "notice": 200, "weapon": "sword", "special_effect": "bleeding"
              },
    "swordsman": {"health": 120, "armor": 80, "will": 10, "might": 40,
                  "reflex": 20, "fortitude": 60, "speed": 1, 'range': 10, 'size': 'normal',
                  "notice": 200, "weapon": "blade", "special_effect": "bleeding"
                  },
    "maceman": {"health": 100, "armor": 100, "will": 10, "might": 50,
                "reflex": 10, "fortitude": 50, "speed": 1, 'range': 10, 'size': 'normal',
                "notice": 200, "weapon": "blunt", "special_effect": "weakened"
                },
    "helbardier": {"health": 100, "armor": 60, "will": 10, "might": 35,
                   "reflex": 30, "fortitude": 50, "speed": 1, 'range': 30, 'size': 'normal',
                   "notice": 200, "weapon": "axe", "special_effect": "bleeding"
                   },
    "footknight": {"health": 200, "armor": 160, "will": 20, "might": 50,
                   "reflex": 25, "fortitude": 75, "speed": 1, 'range': 10, 'size': 'normal',
                   "notice": 200, "weapon": "blade", "special_effect": "bleeding"
                   },
    "linebreaker": {"health": 200, "armor": 140, "will": 20, "might": 65,
                   "reflex": 15, "fortitude": 60, "speed": 1, 'range': 20, 'size': 'normal',
                   "notice": 200, "weapon": "blunt", "special_effect": "weakened"
                   },
    "executioner": {"health": 300, "armor": 200, "will": 40, "might": 70,
                    "reflex": 30, "fortitude": 80, "speed": 1, 'range': 10, 'size': 'normal',
                    "notice": 200, "weapon": "axe", "special_effect": "cursed"
                    },
    "dreadknight": {"health": 300, "armor": 250, "will": 40, "might": 55,
                    "reflex": 40, "fortitude": 80, "speed": 1, 'range': 10, 'size': 'normal',
                    "notice": 200, "weapon": "blade", "special_effect": "cursed"
                    },
    "blackwolf": {"health": 60, "armor": 0, "will": 10, "might": 30,
                  "reflex": 35, "fortitude": 0, "speed": 1, 'range': 10, 'size': 'normal',
                  "notice": 200, "weapon": "snarl", "special_effect": "bleeding"
                  },
    "wolf": {"health": 40, "armor": 0, "will": 5, "might": 20,
             "reflex": 25, "fortitude": 0, "speed": 1, 'range': 10, 'size': 'normal',
             "notice": 200, "weapon": "snarl", "special_effect": "bleeding"
             },
    "knight": {"health": 300, "armor": 200, "will": 30, "might": 60,
               "reflex": 30, "fortitude": 65, "speed": 1, 'range': 20, 'size': 'big',
               "notice": 200, "weapon": "blade", "special_effect": "bleeding"
               },
    "horseman": {"health": 220, "armor": 80, "will": 10, "might": 40,
                 "reflex": 20, "fortitude": 40, "speed": 1, 'range': 20, 'size': 'big',
                 "notice": 200, "weapon": "blade", "special_effect": "bleeding"
                 },
}
