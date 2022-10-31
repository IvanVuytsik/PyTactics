from functools import reduce
import pygame.mouse
from settings import *
from importCSV import *


class LevelUI:
    def __init__(self, surface, offset, sprite_groups):
        self.display_surface = surface
        self.offset = offset
        self.visible_sprites = sprite_groups[0]
        self.description_font = pygame.font.Font(TEXT_FONT, TEXT_FONT_MD)
        self.full_width = self.display_surface.get_size()[0]
        self.full_height = self.display_surface.get_size()[1]
        self.show_minimap = False
        self.mouse_pos = pygame.mouse.get_pos()

        self.troops_types = list(ARMY_DATA.keys())
        self.troops_names = self.get_troops_names()

        self.level_menu_buttons = {
            'Leave': {
                "image": load_image_and_scale("./graphics/ui/leave_icon.png", TILESIZE, TILESIZE),
            },
            'MiniMap': {
                "image": load_image_and_scale("./graphics/ui/minimap_icon.png", TILESIZE, TILESIZE)
            },
            'siege': {
                "image": load_image_and_scale("./graphics/ui/troops_types/4.png", TILESIZE, TILESIZE),
                "units": self.troops_names[4]
            },
            'support': {
                "image": load_image_and_scale("./graphics/ui/troops_types/3.png", TILESIZE, TILESIZE),
                "units": self.troops_names[3]
            },
            'riders': {
                "image": load_image_and_scale("./graphics/ui/troops_types/2.png", TILESIZE, TILESIZE),
                "units": self.troops_names[2]
            },
            'ranged': {
                "image": load_image_and_scale("./graphics/ui/troops_types/1.png", TILESIZE, TILESIZE),
                "units": self.troops_names[1]
            },
            'melee': {
                "image": load_image_and_scale("./graphics/ui/troops_types/0.png", TILESIZE, TILESIZE),
                "units": self.troops_names[0]
            },
            'Defence Mode': {
                "image": load_image_and_scale("./graphics/ui/defmode_icon.png", TILESIZE, TILESIZE),
            },
            'Offence Mode': {
                "image": load_image_and_scale("./graphics/ui/aggr_icon.png", TILESIZE, TILESIZE),
            },
            'Patrol Mode': {
                "image": load_image_and_scale("./graphics/ui/patrol_icon.png", TILESIZE, TILESIZE),
            },
        }
        self.level_button_list = self.create_level_menu_buttons()
        self.action_buttons_list = self.create_action_buttons_list()
        self.action_buttons_list_flat = reduce(lambda x, y: x + y, self.action_buttons_list)

    def create_level_menu_buttons(self):
        button_list = []
        height = self.full_height * 0.05
        width = self.full_width * 0.97
        for index, button in enumerate(self.level_menu_buttons.keys()):
            new_button = LevelUIButton(width - (TILEANDQUARTER * index), height,
                                       self.level_menu_buttons[button]['image'], button)
            button_list.append(new_button)
        return button_list

    def create_action_buttons_list(self):
        button_list = []
        for troop_type in self.level_button_list[2: 7]:
            sub_list = []
            for index, unit in enumerate(self.level_menu_buttons[troop_type.button_type]["units"]):
                if ARMY_DATA[troop_type.button_type][unit]['unlocked']:
                    new_button = LevelUIButton(troop_type.rect.x, troop_type.rect.y + TILEANDQUARTER + (TILEANDQUARTER * index),
                                               ARMY_DATA[troop_type.button_type][unit]['img'], unit,
                                               ARMY_DATA[troop_type.button_type][unit])
                    sub_list.append(new_button)
            button_list.append(sub_list)
        return button_list

    def show_level_buttons(self, input_metadata):
        for item in self.level_button_list:
            item.draw(self.display_surface, input_metadata)
            if item.clicked and item.active is False:
                sound_manager(SOUND_BANK["scroll"])
                for button in self.level_button_list:
                    button.active = False
                item.active = not item.active
            elif item.clicked and item.active:
                sound_manager(SOUND_BANK["scroll"])
                item.active = not item.active
            if item.active:
                match item.button_type:
                    case "melee": self.show_unit_buttons(input_metadata, 4)
                    case "ranged": self.show_unit_buttons(input_metadata, 3)
                    case "riders": self.show_unit_buttons(input_metadata, 2)
                    case "support": self.show_unit_buttons(input_metadata, 1)
                    case "siege": self.show_unit_buttons(input_metadata, 0)
                    case "MiniMap": self.draw_mini_map()

    def show_unit_buttons(self, input_metadata, unit_list):
        for item in self.action_buttons_list[unit_list]:
            item.draw(self.display_surface, input_metadata)
            if item.rect.collidepoint(input_metadata[2]):
                show_info(self.display_surface,
                          f'{item.button_type}. Command: {item.aux_data["activate"]}. Cost: {item.aux_data["cost"]}',
                          self.description_font, TEXT_COLOR, HALFTILE, 5)

    def get_troops_names(self):
        troops_list = []
        index = -1
        for troop in range(len(ARMY_DATA)):
            index += 1
            data = list(ARMY_DATA[self.troops_types[index]].keys())
            troops_list.append(data)
        return troops_list

    def draw_mini_map(self):
        height = self.full_height * 0.15
        width = self.full_width * 0.65
        entity_sprites = [sprite for sprite in self.visible_sprites if hasattr(sprite, "entity_type") and sprite.alive]
        if len(entity_sprites) > 0:
            # --------draw map background---------
            map_rect = pygame.draw.rect(self.display_surface, MAP_EDGE_COLOR,
                                        (width, height, DOUBLETILE * 6, DOUBLETILE * 3))
            pygame.draw.rect(self.display_surface, PAPER_COLOR,
                             (map_rect.x, map_rect.y, DOUBLETILE * 6, DOUBLETILE * 3), 5)

            # ------draw entities ---------
            for index, entity in enumerate(entity_sprites):
                match entity.faction:
                    case 0:
                        color = (200, 200, 200)
                    case 1:
                        color = (0, 200, 0)
                    case 2:
                        color = (200, 0, 0)
                    case 3:
                        color = (100, 30, 100)
                    case _:
                        color = (0, 0, 0)
                pygame.draw.circle(self.display_surface, color, (entity.rect.x // 10 + map_rect.centerx,
                                                                 entity.rect.y // 10 + map_rect.y), 5)

    def draw(self, input_metadata):
        self.show_level_buttons(input_metadata)


class LevelUIButton:
    def __init__(self, x, y, image, button_type, aux_data=None):
        self.button_type = button_type
        self.aux_data = aux_data
        self.description_font = pygame.font.Font(TEXT_FONT, TEXT_FONT_MD)
        self.image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.active = False

    def input(self, surface, input_metadata):
        action = False
        if self.rect.collidepoint(input_metadata[2]):
            show_info(surface, self.button_type, self.description_font, TEXT_COLOR, HALFTILE, 5)
            if all([input_metadata[0], self.clicked is False]):
                time.sleep(0.2)
                action = True
                self.clicked = True
            if all([input_metadata[0] is False]):
                self.clicked = False
        return action

    def draw(self, surface, input_metadata):
        self.input(surface, input_metadata)
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        surface.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, SELECTION_COLOR if self.active else UI_BORDER_COLOR, self.rect, 2)

