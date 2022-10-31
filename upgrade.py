from functools import reduce
from settings import *
from importCSV import *

class PartyUpgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # stat info
        self.stat_number = len(player.stats)
        self.stat_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_MD)
        # generate items
        self.width = self.display_surface.get_size()[0] // 6
        self.height = self.display_surface.get_size()[1] * 0.1
        self.item_list = self.create_items()

        # selection
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.characters = list(player.personal_stats.keys())
        # talent info
        self.branch_number = len(TALENT_DATA)
        self.talent_data = list(TALENT_DATA.values())  # branch / talent
        self.branch_names = list(TALENT_DATA.keys())  # branch
        self.talent_names = self.get_talent_names()  # list_2d
        self.talent_names_flat = reduce(lambda x, y: x + y, self.talent_names)  # list

    def get_talent_names(self):
        talents_list = []
        index = -1
        for talent in range(len(TALENT_DATA)):
            index += 1
            data = list(TALENT_DATA[self.branch_names[index]].keys())
            talents_list.append(data)
        return talents_list

    def create_items(self):
        item_list = []
        for index, stat in enumerate(range(self.stat_number)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.stat_number

            left = (index * increment) + (increment - self.width) // 2
            top = int(self.display_surface.get_size()[1] * 0.13) - HALFTILE

            item = PartyItem(left, top, self.width, self.height, index, self.font)
            item_list.append(item)
        return item_list

    def input(self, input_metadata):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].raise_stat(self.player)

        self.match_index_character(self.player)

        for item in self.item_list:
            if all([item.rect.collidepoint(input_metadata[2]), input_metadata[0]]):
                self.player.selected_character = self.characters[item.index]
                time.sleep(0.1)
                sound_manager(SOUND_BANK["take"])

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    # def match_selected_character(self, player):
    #     match self.selection_index:
    #         case 0: player.selected_character = "rowan"
    #         case 1: player.selected_character = "dunstan"
    #         case 2: player.selected_character = "anselm"
    #         case 3: player.selected_character = "regina"
    #         case 4: player.selected_character = "severin"
    #         case 5: player.selected_character = "alba"
    #         case _: player.selected_character = "rowan"

    def match_index_character(self, player):
        match player.selected_character:
            case "rowan": self.selection_index = 0
            case "dunstan": self.selection_index = 1
            case "anselm": self.selection_index = 2
            case "regina": self.selection_index = 3
            case "severin": self.selection_index = 4
            case "alba": self.selection_index = 5
            case "rowan": self.selection_index = 0

    def display(self, input_metadata):
        self.input(input_metadata)
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.stat_names[index]
            value = self.player.get_value_by_index(index)
            max_values = self.max_values[index]
            cost = self.player.get_cost_by_index(index)

            item.display(self.display_surface, self.selection_index, name, value, max_values, cost, self.talent_names)


# =========item class==========
class PartyItem:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
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
            milestones = [10, 20, 35, 45, 60, 70, 85, 100]
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

    def display_skill_grid(self, surface, name, value, talent_names, selected):
        mod_pos = self.rect.midbottom - pygame.math.Vector2(85, 160)
        mouse_pos = pygame.mouse.get_pos()
        color = MAP_EDGE_COLOR
        increment = self.rect.width // 2
        img_index = -1

        if selected:
            for col in range(2):
                for row in range(4):
                    img_index += 1
                    talent_rect = pygame.draw.rect(surface, color,
                                                   (mod_pos[0] + (col * increment),
                                                    mod_pos[1] - (row * increment),
                                                    DOUBLETILE, DOUBLETILE))
                    # #draw talent icon
                    surface.blit(TALENT_DATA[name][talent_names[self.index][img_index]]["img"],
                                 (talent_rect.x, talent_rect.y))

                    # active / nonactive
                    if value >= TALENT_DATA[name][talent_names[self.index][img_index]]["requirement"]:
                        TALENT_DATA[name][talent_names[self.index][img_index]]["unlocked"] = True
                        pygame.draw.rect(surface, TEXT_COLOR, talent_rect, 4)
                    else:
                        pygame.draw.rect(surface, BONE_COLOR, talent_rect, 4)

                    # draw information
                    if talent_rect.collidepoint(mouse_pos):
                        show_info(surface, TALENT_DATA[name][talent_names[self.index][img_index]]["description"],
                                  self.description_font, TEXT_COLOR, HALFTILE, 5)

    def raise_stat(self, player):
        up_stat = list(player.stats.keys())[self.index]
        if player.stats[up_stat] < player.max_stats[up_stat]:
            if player.experience >= player.upgrade_cost[up_stat]:
                player.experience -= player.upgrade_cost[up_stat]
                player.stats[up_stat] += 1
                sound_manager(SOUND_BANK["take"])

    def display(self, surface, selection_num, name, value, max_values, cost, talent_names):
        if self.index == selection_num:
            pygame.draw.rect(surface, PANEL_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, MAP_EDGE_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, value, cost, self.index == selection_num)
        self.display_bar(surface, value, max_values, self.index == selection_num)
        self.display_skill_grid(surface, name, value, talent_names, self.index == selection_num)
