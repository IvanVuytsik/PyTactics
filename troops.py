import time
from functools import reduce
from settings import *
from importCSV import *


class TroopsUpgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.unit_types = import_folder('./graphics/ui/troops_types')
        # stat info
        self.stat_number = len(player.army_stats)
        self.stat_names = list(player.army_stats.keys())
        self.max_values = list(player.max_army_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_MD)

        # generate items
        self.width = self.display_surface.get_size()[0] // 6
        self.height = self.display_surface.get_size()[1] * 0.1
        self.item_list = self.create_items()

        # selection
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        # army info
        self.branch_number = len(ARMY_DATA)
        self.troops_data = list(ARMY_DATA.values())
        self.troops_names = list(ARMY_DATA.keys())
        self.squad_names = self.get_troops_names()
        self.squad_names_flat = reduce(lambda x, y: x + y, self.squad_names)

    def get_troops_names(self):
        troops_list = []
        index = -1
        for troop in range(len(ARMY_DATA)):
            index += 1
            data = list(ARMY_DATA[self.troops_names[index]].keys())
            troops_list.append(data)
        return troops_list

    def create_items(self):
        item_list = []
        for index, stat in enumerate(range(self.stat_number)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.stat_number

            left = (index * increment) + (increment - self.width) // 2
            top = int(self.display_surface.get_size()[1] * 0.13) - HALFTILE

            item = TroopsItem(left, top, self.width, self.height, index, self.font, self.unit_types[index])
            item_list.append(item)
        return item_list

    def input(self, input_metadata):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].raise_stat(self.player)

        for item in self.item_list:
            if all([item.rect.collidepoint(input_metadata[2]), input_metadata[0]]):
                self.selection_index = item.index
                time.sleep(0.1)
                sound_manager(SOUND_BANK["take"])

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def display(self, input_metadata):
        self.input(input_metadata)
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.stat_names[index]
            value = self.player.get_army_value_by_index(index)
            max_values = self.max_values[index]
            cost = self.player.get_army_cost_by_index(index)

            item.display(self.display_surface, self.selection_index, name, value, max_values, cost, self.squad_names)


# =========item class==========
class TroopsItem:
    def __init__(self, left, top, width, height, index, font, image):
        self.rect = pygame.Rect(left, top, width, height)
        self.image = image
        self.image_rect = self.rect.x + QUARTERTILE, self.rect.y
        self.index = index
        self.font = font
        self.description_font = pygame.font.Font(TEXT_FONT, TEXT_FONT_MD)

    def display_names(self, surface, name, value, cost, selected):
        color = TEXT_COLOR
        # title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 0))
        # cost
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 30))
        # value
        value_surf = self.font.render(f'{int(value)}', False, color)
        value_rect = value_surf.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 10))
        # draw
        surface.blit(title_surf, title_rect)
        if selected:
            surface.blit(value_surf, value_rect)
            surface.blit(cost_surf, cost_rect)
        else:
            surface.blit(value_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        # drawing setup
        self.rect.height = surface.get_size()[1] * 0.8 if selected else surface.get_size()[1] * 0.1

        # main bar calc
        top = self.rect.midtop + pygame.math.Vector2(0, 80)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 50)
        color = TEXT_COLOR

        # main bar setup
        full_height = bottom[1] - top[1]
        ratio = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 10, bottom[1] - ratio, 20, 10)

        # draw milestones
        def draw_milestones():
            milestones = [1, 2, 3, 4]
            for milestone in milestones:
                milestone_ratio = (milestone / max_value) * full_height
                milestone_rect = pygame.Rect(top[0] - 10, bottom[1] - milestone_ratio, 20, 2)
                pygame.draw.rect(surface, color, milestone_rect)
        # draw elems
        if selected:
            # main bar
            pygame.draw.line(surface, color, top, bottom, 5)
            pygame.draw.rect(surface, color, value_rect)
            draw_milestones()

    def display_troops_grid(self, surface, name, value, squad_names, selected):
        mod_pos = self.rect.midbottom - pygame.math.Vector2(85, 160)
        mouse_pos = pygame.mouse.get_pos()
        color = MAP_EDGE_COLOR
        increment = self.rect.width // 2
        img_index = -1

        if self.image is not None:
            surface.blit(self.image, self.image_rect)

        if selected:
            for col in range(1):
                for row in range(4):
                    img_index += 1
                    squad_rect = pygame.draw.rect(surface, color, (mod_pos[0] + (col * increment),
                                                                   mod_pos[1] - (row * increment),
                                                                   DOUBLETILE, DOUBLETILE))
                    # draw troop icon
                    surface.blit(ARMY_DATA[name][squad_names[self.index][img_index]]["img"],
                                 (squad_rect.x, squad_rect.y))
                    # active / nonactive
                    if value >= ARMY_DATA[name][squad_names[self.index][img_index]]["requirement"]:
                        ARMY_DATA[name][squad_names[self.index][img_index]]["unlocked"] = True
                        pygame.draw.rect(surface, TEXT_COLOR, squad_rect, 3)
                    else:
                        pygame.draw.rect(surface, BONE_COLOR, squad_rect, 3)

                    # draw information
                    if squad_rect.collidepoint(mouse_pos):
                        show_info(surface, ARMY_DATA[name][squad_names[self.index][img_index]]["description"],
                                  self.description_font, TEXT_COLOR, HALFTILE, 5)

    def raise_stat(self, player):
        up_stat = list(player.army_stats.keys())[self.index]
        if player.army_stats[up_stat] < player.max_army_stats[up_stat]:
            if player.wealth >= player.upgrade_army_cost[up_stat]:
                player.wealth -= player.upgrade_army_cost[up_stat]
                player.army_stats[up_stat] += 1
                sound_manager(SOUND_BANK["coins"])

    def display(self, surface, selection_num, name, value, max_values, cost, squad_names):
        if self.index == selection_num:
            pygame.draw.rect(surface, PANEL_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 3)
        else:
            pygame.draw.rect(surface, MAP_EDGE_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 3)

        self.display_names(surface, name, value, cost, self.index == selection_num)
        self.display_bar(surface, value, max_values, self.index == selection_num)
        self.display_troops_grid(surface, name, value, squad_names, self.index == selection_num)
