import pygame
from settings import *
from player import Player
from importCSV import *
from tile import Tile, FogTile, Biome
from ui import UI
from journal import Journal
from lorebook import Lorebook
from upgrade import PartyUpgrade
from troops import TroopsUpgrade
from inventory import Inventory
from map import Map
from level import Level
from debug import debug


class NewWorld:
    def __init__(self):
        self.music_state = 'map'
        self.world_state = "overworld"
        self.menu_state = None
        self.game_paused = False
        self.fog_of_war = False
        self.display_surface = pygame.display.get_surface()
        self.width = self.display_surface.get_size()[0]
        self.height = self.display_surface.get_size()[1]

        #sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.fog_sprites = pygame.sprite.Group()
        self.biome_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        #world funcs
        self.create_map()
        #music state manager
        music_manager(self.music_state)

        #level
        self.current_level = None
        #ui
        self.ui = UI(self.player)
        self.journal = Journal()
        self.lorebook = Lorebook()
        self.upgrade = PartyUpgrade(self.player)
        self.troops = TroopsUpgrade(self.player)
        self.inventory = Inventory(self.player)
        self.map = Map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./graphics/map/worldmap_block.csv'),
            'character': import_csv_layout('./graphics/map/worldmap_characters.csv'),
            'mine': import_csv_layout('./graphics/map/worldmap_mines.csv'),
            'biome': import_csv_layout('./graphics/map/worldmap_biome.csv'),
        }
        graphics = {
            'mines': import_folder('./graphics/map/mines')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], 'invisible', pygame.Surface((TILESIZE, TILESIZE)))
                        if style == "biome":
                            Biome((x, y), [self.biome_sprites], 'invisible', pygame.Surface((TILESIZE, TILESIZE)), int(col))
                        if style == 'mine':
                            surf = graphics['mines'][int(col)]
                            Tile((x, y), [self.visible_sprites], 'mine', surf)
                        if style == "character":
                            self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                    else:
                        FogTile((col_index * DOUBLETILE, row_index * DOUBLETILE), [self.fog_sprites])

    #=========================================================
    def toggle_level_buttons(self):
        if self.current_level is not None:
            for button in self.current_level.levelUI.level_button_list:
                if button.clicked:
                    match button.button_type:
                        case "Leave": self.toggle_overworld_mode()
                        case _: self.toggle_default()

    #===========================================================
    def toggle_menu_buttons(self):
        for button in self.ui.button_list:
            if button.clicked and button.active is False:
                sound_manager(SOUND_BANK["scroll"])
                for item in self.ui.button_list:
                    item.active = False
                button.active = not button.active
                self.game_paused = True
            elif button.clicked and button.active:
                sound_manager(SOUND_BANK["scroll"])
                button.active = not button.active
                self.game_paused = False

    def show_menu_interface(self, input_metadata):
        for button in self.ui.button_list:
            if button.active:
                match button.button_type:
                    case "Experience": self.upgrade.display(input_metadata)
                    case "Inventory": self.inventory.display(input_metadata, [self.world_state])
                    case "Journal": self.journal.update(input_metadata)
                    case "Troops": self.troops.display(input_metadata)
                    case "Lore": self.lorebook.update(input_metadata)
                    case "Map": self.map.update(self.player)
                    case _: self.toggle_default()
            elif button.clicked:
                match button.button_type:
                    case "Explore": self.toggle_tactical_mode()
                    case _: self.toggle_default()
                self.menu_state = str(button.button_type)

    def toggle_default(self):
        self.menu_state = None
        self.game_paused = False

    def toggle_pause(self):
        self.game_paused = not self.game_paused
        self.menu_state = "pause"

    def toggle_tactical_mode(self, data=None):
        if self.world_state == "overworld":
            self.game_paused = True
            self.current_level = Level(self.player)
            self.world_state = "tactical"
            #music change
            self.music_state = f"battle_{random.choice([0,1,2])}"
            music_manager(self.music_state)
            self.player.can_move = False

    def toggle_overworld_mode(self, data=None):
        if self.world_state == "tactical":
            self.game_paused = False
            self.current_level = None
            self.world_state = "overworld"
            self.music_state = "map"
            music_manager(self.music_state)
            self.player.can_move = True

    def tactical_mode(self):
        if self.world_state == "tactical":
            self.current_level.run()

        if self.current_level is not None:
            if self.menu_state is not None:
                self.current_level.level_paused = True
            else:
                self.current_level.level_paused = False
            #print(self.world_state, self.menu_state, self.current_level.level_paused)

    # def check_biome(self):
    #     for biome in self.biome_sprites:
    #         if self.player.hitbox.colliderect(biome.rect):
    #             print(biome.biome_type)

    def run(self, input_metadata):
        self.visible_sprites.custom_draw(self.player, self.fog_sprites, self.fog_of_war)
        self.toggle_level_buttons()
        self.toggle_menu_buttons()
        self.tactical_mode()
        #self.check_biome()
        # ==========timewheel=============
        self.ui.animate_timewheel(int(self.width*0.85), int(self.height*0.87), active=self.player.moving)
        self.ui.display(self.player, input_metadata)
        if self.current_level is not None:
            self.current_level.levelUI.draw(input_metadata)
        self.show_menu_interface(input_metadata)

        if self.game_paused:
            self.player.moving = False
        else:
            self.visible_sprites.update()
            self.menu_state = None


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        #offset
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load("./graphics/map/map.png").convert_alpha()

    def custom_draw(self, player, fog, fog_active):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        #=====================fog of war===================
        if fog_active:
            for sprite in fog:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
                if sprite.rect.colliderect(player.rect):
                    sprite.kill()
