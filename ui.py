import time
from settings import *
from importCSV import *
from button import Button


class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SM)
        self.width = self.display_surface.get_size()[0]
        self.height = self.display_surface.get_size()[1]
        # personal cards data
        self.character_cards = self.get_character_cards(player)
        # UI rect elements
        self.stat_bars = {
            'wealth': {
                'image': load_image_and_scale('./graphics/ui/coinbar.png', TILESIZE * 4.75, TILEANDHALF),
                'min': 100, 'max': 100, 'color_primary': BAG_COLOR, 'color_secondary': BONE_COLOR,
            },
            'experience': {
                'image': load_image_and_scale('./graphics/ui/expbar.png', TILESIZE * 4.75, TILEANDHALF),
                'min': 100, 'max': 100, 'color_primary': EXP_COLOR, 'color_secondary': BONE_COLOR,
            },
            'leadership': {
                'image': load_image_and_scale('./graphics/ui/leadbar.png', TILESIZE * 4.75, TILEANDHALF),
                'min': player.party_command, 'max': player.max_party_command, 'color_primary': MAP_EDGE_COLOR,
                'color_secondary': UI_BG_COLOR,
            },
            'health': {
                'image': load_image_and_scale('./graphics/ui/healthbar.png', TILESIZE * 4.75, TILEANDHALF),
                'min': player.party_health, 'max': player.max_party_health, 'color_primary': SELECTION_COLOR,
                'color_secondary': HEALTH_COLOR_NEGATIVE,
            },
        }
        self.stat_list = self.create_stats()

        self.menu_buttons = {
            'Experience':
                {'image': load_image_and_scale("./graphics/ui/experience_icon.png", TILESIZE, TILESIZE)},
            'Inventory':
                {'image': load_image_and_scale("./graphics/ui/inventory_icon.png", TILESIZE, TILESIZE)},
            'Journal':
                {'image': load_image_and_scale("./graphics/ui/questbook_icon.png", TILESIZE, TILESIZE)},
            'Troops':
                {'image': load_image_and_scale("./graphics/ui/troops_icon.png", TILESIZE, TILESIZE)},
            'Lore':
                {'image': load_image_and_scale("./graphics/ui/lorebook_icon.png", TILESIZE, TILESIZE)},
            'Map':
                {'image': load_image_and_scale("./graphics/ui/map_icon.png", TILESIZE, TILESIZE)},
            'Explore':
                {'image': UI_ElEMENTS["explore"]},
        }

        self.button_list = self.create_menu_buttons()

        # timewheel
        self.timewheel_frame_index = 0
        self.timewheel_animation_speed = 0.01
        self.animated_data = {
            'timewheel': import_indexed_animations('./graphics/timewheel', 6 * TILESIZE, 3 * TILESIZE),
        }
        self.timewheel_frames = self.animated_data['timewheel']
        self.timewheel_image = self.timewheel_frames[self.timewheel_frame_index]

    def animate_timewheel(self, x, y, active):
        if active:
            self.timewheel_frame_index += self.timewheel_animation_speed
        if self.timewheel_frame_index >= len(self.timewheel_frames):
            self.timewheel_frame_index = 0
        else:
            self.timewheel_image = self.timewheel_frames[int(self.timewheel_frame_index)]
        self.display_surface.blit(self.timewheel_image, (x, y))

    def display_info_panel(self):
        width = int(self.display_surface.get_size()[0])
        pygame.draw.rect(self.display_surface, MAP_EDGE_COLOR, (0, 0, width, TILESIZE))
        pygame.draw.rect(self.display_surface, PAPER_COLOR, (0, 0, width, TILESIZE), 3)

    def get_character_cards(self, player):
        height = int(self.display_surface.get_size()[1]) - DOUBLETILE
        cards_data = []
        for index, character in enumerate(player.personal_stats.keys()):
            if player.personal_stats[character]['unlocked']:
                card_rect = pygame.Rect((DOUBLETILE * index) + (index * QUARTERTILE), height, DOUBLETILE, DOUBLETILE)
                card_portrait = player.personal_stats[character]['portrait']
                cards_data.append([str(character), card_rect, card_portrait])
        return cards_data

    def display_character_cards(self, player):
        for index, card in enumerate(self.character_cards):
            portrait_name, portrait_img, portrait_rect = card[0], card[2], card[1]
            # draw card
            pygame.draw.rect(self.display_surface, MAP_EDGE_COLOR, portrait_rect)
            # draw portrait
            self.display_surface.blit(portrait_img, portrait_rect)
            # draw fame
            pygame.draw.rect(self.display_surface,
                             TEXT_COLOR if portrait_name == player.selected_character else PAPER_COLOR,
                             portrait_rect, 3)

    def select_character_card(self, player, input_metadata):
        mouse_pos = pygame.mouse.get_pos()
        for name, rect, portrait in self.character_cards:
            if rect.collidepoint(mouse_pos) and input_metadata[0]:
                player.selected_character = name

    def create_stats(self):
        stat_list = []
        data = self.stat_bars
        for index, stat in enumerate(self.stat_bars.keys()):
            new_stat = Stat(self.width * 0.38 + (FIVETILES * index), self.height * 0.95,
                            data[stat]['image'], data[stat]['color_primary'],
                            data[stat]['color_secondary'], stat)
            stat_list.append(new_stat)
        return stat_list

    def create_menu_buttons(self):
        button_list = []
        height = self.display_surface.get_size()[1] * 0.05
        for index, button in enumerate(self.menu_buttons.keys()):
            new_button = MenuButton((TILEANDQUARTER * index), height,
                                    self.menu_buttons[button]['image'], button)
            button_list.append(new_button)
        return button_list

    def show_party_stats(self, player):
        for item in self.stat_list:
            match item.type:
                case 'wealth':
                    data = player.wealth
                    minimum = 100
                    maximum = 100
                case 'experience':
                    data = player.experience
                    minimum = 100
                    maximum = 100
                case 'health':
                    data = None
                    minimum = player.party_health
                    maximum = player.max_party_health
                case 'leadership':
                    data = player.party_command
                    minimum = player.party_command
                    maximum = player.max_party_command
                case _:
                    minimum = 100
                    maximum = 100
                    data = None
            item.draw(self.display_surface, self.font, data, minimum, maximum)

    def show_buttons(self, input_metadata):
        for item in self.button_list:
            item.draw(self.display_surface, input_metadata)

    def display(self, player, input_metadata):
        # stats
        self.show_party_stats(player)
        # info panel
        self.display_info_panel()
        self.show_buttons(input_metadata)
        # character panel
        self.display_character_cards(player)
        self.select_character_card(player, input_metadata)


class MenuButton:
    def __init__(self, x, y, image, button_type):
        self.button_type = button_type
        self.description_font = pygame.font.Font(TEXT_FONT, TEXT_FONT_MD)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.active = False

    def input(self, surface, input_metadata):
        action = False
        if self.rect.collidepoint(input_metadata[2]):
            show_info(surface, self.button_type, self.description_font, TEXT_COLOR, HALFTILE, 5)
            if all([input_metadata[0], self.clicked is False]):
                time.sleep(0.1)
                action = True
                self.clicked = True
            if all([input_metadata[0] is False]):
                self.clicked = False
        return action

    def draw(self, surface, input_metadata):
        self.input(surface, input_metadata)
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        pygame.draw.rect(surface, SELECTION_COLOR if self.active else UI_BORDER_COLOR, self.rect, 3)
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Stat:
    def __init__(self, x, y, image, col_pm, col_sd, stat_type):
        self.bar_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        self.type = stat_type
        self.image = image
        self.col_pm = col_pm
        self.col_sd = col_sd

    def show_bar(self, display_surface, minimum=100, maximum=100):
        pygame.draw.rect(display_surface, self.col_sd, self.bar_rect)
        ratio = minimum / maximum
        current_width = self.bar_rect.width * ratio
        current_rect = self.bar_rect.copy()
        current_rect.width = current_width
        # draw bar
        pygame.draw.rect(display_surface, self.col_pm, current_rect)
        # draw rect border if not at 100%
        if minimum == maximum:
            pygame.draw.rect(display_surface, UI_BORDER_COLOR, self.bar_rect, 3)
        # draw image
        display_surface.blit(self.image, (self.bar_rect.x - TILEANDQUARTER, self.bar_rect.y - 20))

    def show_data(self, display_surface, font, data, color=TEXT_COLOR):
        text_surf = font.render(str(int(data)), False, color)
        text_rect = text_surf.get_rect(topleft=(self.bar_rect.x + SEMITILE, self.bar_rect.y - 5))
        display_surface.blit(text_surf, text_rect)

    def draw(self, display_surface, font, data, minimum, maximum):
        self.show_bar(display_surface, minimum, maximum)
        if data is not None:
            self.show_data(display_surface, font, data)
