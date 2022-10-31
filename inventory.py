import time
from settings import *


class Inventory:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SM)
        self.rows = 10
        self.cols = 4
        self.max_items = self.rows * self.cols

        self.description_font = pygame.font.Font(TEXT_FONT, TEXT_FONT_MD)
        self.full_width = self.display_surface.get_size()[0]
        self.full_height = self.display_surface.get_size()[1]

        self.grid_list = self.create_grid()
        self.item_stat_icons = import_folder_and_scale('./graphics/ui/inventory_icons', TILESIZE, TILESIZE)
        self.list_of_stats = ["health", "armor", "might", "fortitude", "reflex", "will"]

        self.inventories = self.create_inventories()
        self.equipment_list = []

        self.item_group = pygame.sprite.Group()
        self.mouse_slot = MouseSlot()

        self.create_items(['Leather Armor', 'Night Armor', 'Captain Armor', 'Black Plate', 'Crimson Armor', 'Robe',
                           'Magi Robe', 'Night Cloak', 'Leather Gloves', 'Forest Gloves', 'Dragon Claws',
                           'Leather Boots', 'Raider Helmet', 'Silver Amulet', 'Crystal Ring', 'Commander Ring',
                           'Common Ring', 'Wooden Shield', 'Crimson Buckler', 'Hunting Knife', 'Ambush Bow',
                           'Crimson Bow', 'Wand', 'Gold', 'Coins', 'Evercoin', 'Bottomless Mug', 'Firebird Feather',
                           'Symbol of Peace', 'Clover', 'Lucky Horseshoe', 'Lamp', 'Alchemist Heart', 'Vitality Potion',
                           'Ring of Defence', 'Flute', 'Bloodstone', 'Gambeson', "Sextant", "Taro Cards"],
                          self.grid_list)
        #self.create_items([], self.grid_list)

        #self.get_item_names()
    @staticmethod
    def get_item_names():
        name_list = []
        for item in ITEMS_DATA.keys():
            name_list.append(item)
        print(name_list)

    def draw_inventory_background(self):
        left = int(self.full_width * 0.05)
        top = int(self.full_height * 0.12)
        pygame.draw.rect(self.display_surface, PANEL_COLOR, (left, top, DOUBLETILE * 16.5, DOUBLETILE * 8))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, (left, top, DOUBLETILE * 16.5, DOUBLETILE * 8), 3)

    def draw_stats(self, input_metadata):
        left = int(self.full_width * 0.1)
        top = int(self.full_height * 0.15)
        for index, stat in enumerate(self.list_of_stats):
            stat_rect = pygame.Rect(left + (index * DOUBLETILE) + (index * TILEANDHALF), top, DOUBLETILE, DOUBLETILE)
            self.display_surface.blit(LIBRARY[stat]["image"], stat_rect)
            self.show_data(UNIT_DATA[self.player.selected_character][stat],
                           (stat_rect[0] + HALFTILE, stat_rect[1] + DOUBLETILE))
            if stat_rect.collidepoint(input_metadata[2]):
                show_info(self.display_surface, LIBRARY[stat]["desc"], self.description_font, TEXT_COLOR, HALFTILE, 5)

        # draw portrait
        self.draw_portrait()

    def draw_item_stat_icons(self):
        left = int(self.full_width * 0.2)
        top = int(self.full_height * 0.7)
        for index, stat in enumerate(self.list_of_stats):
            stat_rect = pygame.Rect(left + (index * DOUBLETILE) + (DOUBLETILE * 2.5),
                                    top, TILESIZE, TILESIZE)
            self.display_surface.blit(self.item_stat_icons[index], stat_rect)

    def draw_item_stats(self, input_metadata):
        left = int(self.full_width * 0.2)
        top = int(self.full_height * 0.7)
        for item in self.item_group:
            if all([item.rect.collidepoint(input_metadata[2]),
                    item.belongs == self.player.selected_character or item.belongs == '']):
                self.show_data(item.name, (left - TILESIZE, top))
                self.show_data(item.cost, (left - TILESIZE, top + TILESIZE))
                for index, stat in enumerate(self.list_of_stats):
                    stat_rect = pygame.Rect(left + (index * DOUBLETILE) + (DOUBLETILE * 2.5) + QUARTERTILE,
                                            top + TILESIZE, TILESIZE, TILESIZE)
                    self.show_data(ITEMS_DATA[item.name][stat], (stat_rect[0], stat_rect[1]))

                self.draw_item_stat_icons()

    def draw_portrait(self):
        left = int(self.full_width * 0.65)
        top = int(self.full_height * 0.15)
        portrait_img = self.player.personal_stats[self.player.selected_character]["portrait"]
        portrait_rect = pygame.draw.rect(self.display_surface, MAP_EDGE_COLOR, (left, top, DOUBLETILE, DOUBLETILE))
        pygame.draw.rect(self.display_surface, TEXT_COLOR, portrait_rect, 3)
        self.display_surface.blit(portrait_img, portrait_rect)

        self.show_data(self.player.selected_character, (portrait_rect[0], portrait_rect[1] + DOUBLETILE))

    def show_data(self, data, data_rect, color=TEXT_COLOR):
        text_surf = self.font.render(str(data), False, color)
        text_rect = text_surf.get_rect(topleft=data_rect)
        self.display_surface.blit(text_surf, text_rect)

    def input(self, input_metadata):
        self.mouse_slot.update(input_metadata[2][0], input_metadata[2][1])
        for slot in (self.grid_list + self.equipment_list):
            slot.selected = False
            if all([slot.rect.collidepoint(input_metadata[2]), input_metadata[0] is True, not slot.selected]):
                slot.selected = True
        #makes item first in item_list (draws over other items)
        self.draw_item_over_items()

    def draw_item_over_items(self):
        for index, item in enumerate(self.item_group):
            if item.is_held:
                self.item_group.remove(item)
                self.item_group.add(item)

    def create_grid(self):
        left = int(self.full_width * 0.1)
        top = int(self.full_height * 0.3)
        grid_list = []
        for index_x in range(self.rows):
            for index_y in range(self.cols):
                inv_slot = Slot('item', left + (DOUBLETILE * index_x), top + (DOUBLETILE * index_y))
                grid_list.append(inv_slot)
        # discard slot
        discard_slot = Slot('transmute', left, top + (DOUBLETILE * 4.5), UI_ElEMENTS['coinbag'])
        grid_list.append(discard_slot)
        return grid_list

    def create_inventories(self):
        inventories = []
        for character in self.player.personal_stats.keys():
            new_inventory = self.create_equipment_grid(self.player.personal_stats[character]["inventory"])
            inventories.append(new_inventory)
        return inventories

    def create_equipment_grid(self, slot_types):
        left = int(self.full_width * 0.65)
        top = int(self.full_height * 0.3)
        equipment_list = []
        item_col = 0
        item_row = 0
        for index, slot in enumerate(slot_types):
            img = load_image(f'./graphics/ui/equipment_slots/{slot}.png')
            equipment_slot = Slot(slot, left + (DOUBLETILE * item_col) + (HALFTILE * item_col),
                                  top + (DOUBLETILE * item_row) + (TILESIZE * item_row), img)
            equipment_list.append(equipment_slot)
            item_col += 1
            if item_col >= 3:
                item_row += 1
                item_col = 0
        return equipment_list

    def create_items(self, items, container):
        new_items = len(items)
        for item in items:
            available_slots = [slot for slot in container if slot.contains is False and slot.type == "item"]
            if new_items <= (len(available_slots)):
                new_items -= 1
                slot = random.choice(available_slots)
                Item(item, slot.rect.x, slot.rect.y, self.item_group)
                slot.contains = True

    def draw_grid(self):
        inventory_slots = self.grid_list + self.equipment_list
        for slot in inventory_slots:
            slot.draw_slot(self.display_surface)

    def draw_inventory_grid(self):
        match self.player.selected_character:
            case "rowan": self.equipment_list = self.inventories[0]
            case "dunstan": self.equipment_list = self.inventories[1]
            case "anselm": self.equipment_list = self.inventories[2]
            case "regina": self.equipment_list = self.inventories[3]
            case "severin": self.equipment_list = self.inventories[4]
            case "alba": self.equipment_list = self.inventories[5]
            case _: self.equipment_list = self.inventories[0]

    def display(self, input_metadata, world_metadata):
        self.draw_inventory_background()
        self.draw_inventory_grid()
        self.draw_grid()
        self.draw_stats(input_metadata)
        self.draw_item_stats(input_metadata)
        self.input(input_metadata)
        self.item_group.update(self.display_surface, input_metadata, self.mouse_slot,
                               [self.grid_list, self.equipment_list], self.player, world_metadata)


class Slot:
    def __init__(self, slot_type, x, y, image=None):
        self.type = slot_type
        self.image = image
        self.show_image = True
        self.selected = False
        self.contains = False
        self.rect = pygame.Rect(x, y, DOUBLETILE, DOUBLETILE)
        self.hitbox = self.rect.inflate(-TILEANDHALF, -TILEANDHALF)

    def draw_slot(self, display):
        pygame.draw.rect(display, MAP_EDGE_COLOR, self.rect)
        if self.image is not None and self.show_image:
            display.blit(self.image, self.rect)
        pygame.draw.rect(display, TEXT_COLOR if not self.selected else UI_BORDER_COLOR, self.rect, 3)


class MouseSlot:
    def __init__(self):
        self.hosts = False
        self.rect = pygame.Rect(DOUBLETILE, DOUBLETILE, DOUBLETILE, DOUBLETILE)

    def update(self, x, y):
        self.rect.centerx, self.rect.centery = x, y
        # self.display_surface = pygame.display.get_surface()
        # pygame.draw.rect(self.display_surface, MAP_EDGE_COLOR, self.rect)


class Item(pygame.sprite.Sprite):
    def __init__(self, name, x, y, groups):
        super().__init__(groups)
        self.equipped = False
        self.is_held = False
        self.belongs = ""
        self.name = name
        self.type = ITEMS_DATA[name]["type"]
        self.image = ITEMS_DATA[name]["image"]
        self.cost = ITEMS_DATA[name]["cost"]
        self.list_of_bonuses = ["health", "armor", "might", "fortitude", "reflex", "will"]
        self.rect = pygame.Rect(x, y, DOUBLETILE, DOUBLETILE)
        self.hitbox = self.rect.inflate(-TILEANDHALF, -TILEANDHALF)

    def add_stats(self, character):
        for stat in self.list_of_bonuses:
            UNIT_DATA[character][stat] += ITEMS_DATA[self.name][stat]

    def subtract_stats(self, character):
        for stat in self.list_of_bonuses:
            UNIT_DATA[character][stat] -= ITEMS_DATA[self.name][stat]

    def transmute_item(self, player):
        player.wealth += self.cost
        sound_manager(SOUND_BANK["coins"])
        self.kill()

    def item_input(self, input_metadata, mouse_slot, inventory_slots, player):
        available_slots = inventory_slots[0] + inventory_slots[1]
        for slot in available_slots:
            # discard item
            if all([slot.rect.collidepoint(input_metadata[2]), input_metadata[0] is False,
                    self.is_held, mouse_slot.hosts, slot.type == 'transmute']):
                self.transmute_item(player)
                self.is_held = False
                mouse_slot.hosts = not mouse_slot.hosts
            # pick item
            if all([self.rect.collidepoint(input_metadata[2]), input_metadata[0],
                    self.rect.colliderect(slot.rect),
                    self.is_held is False, mouse_slot.hosts is False]):
                self.is_held = True
                mouse_slot.hosts = not mouse_slot.hosts
                time.sleep(0.1)
                slot.contains = False
                slot.show_image = True
                if all([slot.type == self.type]):
                    self.equipped = False
                    self.belongs = ""
                    self.subtract_stats(player.selected_character)
            # drop item
            if all([slot.rect.collidepoint(input_metadata[2]), input_metadata[0] is False,
                    self.is_held, mouse_slot.hosts, slot.contains is False,
                    slot.type == 'item' or slot.type == self.type]):
                self.is_held = False
                mouse_slot.hosts = not mouse_slot.hosts
                self.rect.centerx, self.rect.centery = slot.rect.centerx, slot.rect.centery
                time.sleep(0.1)
                slot.contains = True
                slot.show_image = False
                if all([slot.type == self.type]):
                    self.equipped = True
                    self.belongs = player.selected_character
                    self.add_stats(player.selected_character)
            # if slot.rect.collidepoint(input_metadata[2]):
            #     print(slot.contains, self.equipped, self.type, self.is_held, self.belongs)
        if self.is_held:
            self.rect.x, self.rect.y = mouse_slot.rect.x, mouse_slot.rect.y

    def update(self, display, input_metadata, mouse_slot, inventory_slots, player, world_metadata):
        if any([self.belongs == player.selected_character, self.belongs == ""]):
            if world_metadata[0] == "overworld":
                self.item_input(input_metadata, mouse_slot, inventory_slots, player)
            display.blit(self.image, self.rect)
