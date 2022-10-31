import random
from settings import *
from importCSV import *
from tile import Tile, LevelTile, Construction, Marker
from level_ui import LevelUI
from global_ai import GlobalAI
from debug import debug
from particles import Particles
from entity import Entity


class Level(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.level_menu_state = None
        self.level_paused = False
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.width = self.display_surface.get_size()[0]
        self.height = self.display_surface.get_size()[1]
        #sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.surface_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.marker_sprites = pygame.sprite.Group()

        self.faction_ally = pygame.sprite.Group()
        self.faction_enemy = pygame.sprite.Group()
        self.faction_neutral = pygame.sprite.Group()
        self.faction_omni_hostile = pygame.sprite.Group()

        # ---------selection box---------
        self.drawing = False
        self.pos_x = 0
        self.pos_y = 0
        self.box_rect = [0, 0, 0, 0]

        self.selected_units = 0
        self.metadata = {}
        #offset
        self.offset = self.visible_sprites.offset
        #particles
        self.particles = Particles()

        #world funcs
        self.create_level()
        #center starting position
        self.visible_sprites.center_on_target(self.main_hero)
        #ui
        self.levelUI = LevelUI(self.display_surface, self.offset, [self.visible_sprites, self.surface_sprites])
        #ai
        self.enemy_ai = self.create_global_ai(2, self.enemy_building)

    def create_level(self):
        layouts = {
            'boundary': import_csv_layout('graphics/level/0_level/_Block.csv'),
            'marker': import_csv_layout('graphics/level/0_level/_Markers.csv'),
            'tile': import_csv_layout('graphics/level/0_level/_Ground.csv'),
            'tree': import_csv_layout('graphics/level/0_level/_Trees.csv'),
            'prop': import_csv_layout('graphics/level/0_level/_Props.csv'),
            'building': import_csv_layout('graphics/level/0_level/_Buildings.csv'),
            'camp': import_csv_layout('graphics/level/0_level/_Camp.csv'),
            'character': import_csv_layout('graphics/level/0_level/_Characters.csv'),
            'enemy_building': import_csv_layout('graphics/level/0_level/_Enemy_Buildings.csv'),
            'enemy_character': import_csv_layout('graphics/level/0_level/_Enemy_Characters.csv'),
            'ally_character': import_csv_layout('graphics/level/0_level/_Ally_Characters.csv'),
            'ally_building': import_csv_layout('graphics/level/0_level/_Ally_Buildings.csv'),
            'critter': import_csv_layout('graphics/level/0_level/_Critters.csv'),
            'lair': import_csv_layout('graphics/level/0_level/_Lairs.csv'),
        }

        graphics = {
             'tiles': import_folder('./graphics/level/tiles'),
             'buildings': import_folder('./graphics/level/buildings'),
             'trees': import_folder_and_scale('./graphics/level/trees', DOUBLETILE, TRIPLETILE),
             'camps': import_folder_and_scale('./graphics/level/camp', TRIPLETILE, DOUBLETILE),
             'props': import_folder_and_scale('./graphics/level/props', DOUBLETILE, DOUBLETILE),
             'characters': import_folder_and_scale('./graphics/level/characters', DOUBLETILE, DOUBLETILE),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = (col_index - row_index) * TILESIZE
                        y = (col_index + row_index) * HALFTILE
                        match style:
                            case "boundary": Tile((x, y), [self.obstacle_sprites], 'invisible', pygame.Surface((DOUBLETILE, TILESIZE)))
                            case "marker":
                                Marker((x, y), [self.marker_sprites], 'invisible', pygame.Surface((DOUBLETILE, TILESIZE)))
                            case "tile":
                                surf = graphics['tiles'][int(col)]
                                Tile((x, y), [self.surface_sprites], 'tile', surf)
                            case "tree":
                                surf = graphics['trees'][int(col)]
                                LevelTile((x, y), [self.visible_sprites, self.obstacle_sprites], 'tree', surf)
                            case "prop":
                                surf = graphics['props'][int(col)]
                                LevelTile((x, y), [self.visible_sprites, self.obstacle_sprites], 'prop', surf)
                            case "building":
                                surf = graphics['buildings'][int(col)]
                                LevelTile((x, y), [self.visible_sprites, self.obstacle_sprites], 'building', surf)
                            case "camp":
                                surf = graphics['camps'][int(col)]
                                self.camp = Construction((x, y), [self.visible_sprites, self.obstacle_sprites], 'camp',
                                             'construction', surf, self.display_surface, self.offset, {"health": 1000},
                                             self.particles, faction=1, controllable=True)
                            case "enemy_building":
                                surf = graphics['camps'][int(col)]
                                self.enemy_building = [Construction((x, y), [self.visible_sprites, self.obstacle_sprites],
                                             'enemy_building', 'construction', surf, self.display_surface, self.offset,
                                             {"health": 1000}, self.particles, faction=2)]

                            case "ally_building":
                                surf = graphics['camps'][int(col)]
                                self.ally_building = [Construction((x, y), [self.visible_sprites, self.obstacle_sprites],
                                             'ally_building', 'construction', surf, self.display_surface, self.offset,
                                             {"health": 1000}, self.particles, faction=1)]
                            case "character":
                                if int(col) == 0:
                                    self.main_hero = Entity((x, y), [self.visible_sprites],
                                                            [self.obstacle_sprites, self.surface_sprites],
                                                             "rowan", self.offset, self.particles, 1,
                                                            metadata=self.metadata, controllable=True)
                                    self.spawn_heroes(self.main_hero.rect.x, self.main_hero.rect.y)
                                else:
                                    Entity((x, y), [self.visible_sprites], [self.obstacle_sprites, self.surface_sprites],
                                           UNIT_ID[int(col)], self.offset, self.particles, 1,
                                           metadata=self.metadata, controllable=True)
                            case "enemy_character":
                                Entity((x, y), [self.visible_sprites], [self.obstacle_sprites, self.surface_sprites],
                                       UNIT_ID[int(col)], self.offset, self.particles, 2, metadata=self.metadata)
                            case "ally_character":
                                Entity((x, y), [self.visible_sprites], [self.obstacle_sprites, self.surface_sprites],
                                        UNIT_ID[int(col)], self.offset, self.particles, 1, metadata=self.metadata, controllable=False)
                            case "critter":
                                Entity((x, y), [self.visible_sprites], [self.obstacle_sprites, self.surface_sprites],
                                       UNIT_ID[int(col)], self.offset, self.particles, 3, metadata=self.metadata)

    def create_global_ai(self, ai_faction, constructions):
        new_ai = GlobalAI(100, ai_faction, 10, constructions, self.marker_sprites)
        return new_ai

    def spawn_heroes(self, x, y):
        for character, value in self.player.personal_stats.items():
            if value["unlocked"] and character != "rowan":
                Entity((x + random.randint(-TILESIZE, TILESIZE), y + random.randint(-TILESIZE, TILESIZE)),
                       [self.visible_sprites], [self.obstacle_sprites, self.surface_sprites],
                       character, self.offset, self.particles, 1, metadata=self.metadata, controllable=True)

    @staticmethod
    def calculate_location(x, y):
        pos_x = x * TILESIZE
        pos_y = y * TILESIZE
        return pos_x, pos_y

    def put_in_groups(self):
        entity_sprites = [sprite for sprite in self.visible_sprites if hasattr(sprite, "entity_type")]
        for entity in entity_sprites:
            match entity.faction:
                case 0: self.faction_neutral.add(entity)
                case 1: self.faction_ally.add(entity)
                case 2: self.faction_enemy.add(entity)
                case 3: self.faction_omni_hostile.add(entity)
                case _: self.faction_neutral.add(entity)

    #========================spawn============================
    def toggle_unit_buttons(self):
        for button in self.levelUI.action_buttons_list_flat:
            if button.clicked and self.camp.alive:
                if all([self.player.wealth >= button.aux_data["cost"],
                        self.player.party_command >= button.aux_data["activate"]]):
                    self.player.wealth -= button.aux_data["cost"]
                    self.player.party_command -= button.aux_data["activate"]
                    sound_manager(SOUND_BANK["coins"])
                    self.spawn_troops(button.button_type, 1, self.camp.spawn_rect.centerx, self.camp.spawn_rect.centery)

    def spawn_troops(self, toops_type, faction, x, y):
        for key, value in SQUAD_DATA[toops_type].items():
            for unit in range(value):
                Entity((x + random.randint(-DOUBLETILE, DOUBLETILE), y + random.randint(-DOUBLETILE, DOUBLETILE)),
                       [self.visible_sprites], [self.obstacle_sprites, self.surface_sprites],
                       key, self.offset, self.particles, faction, metadata=self.metadata)

    def change_markers_owner(self, entity_list):
        for entity in entity_list:
            for marker in self.marker_sprites:
                if entity.rect.colliderect(marker.rect):
                    marker.belongs = entity.faction

    def switch_behavior(self, entity_list):
        for entity in entity_list:
            for button in self.levelUI.level_button_list:
                if button.clicked and entity.selected:
                    match button.button_type:
                        case "Defence Mode": entity.mode = "defensive"
                        case "Offence Mode": entity.mode = "offensive"
                        case "Patrol Mode": entity.mode = "patrol"

    def input(self):
        entity_sprites = [sprite for sprite in self.visible_sprites if hasattr(sprite, "entity_type")]
        keys = pygame.key.get_pressed()
        # =======================show/hide indicators=======================
        if keys[pygame.K_f]:
            time.sleep(0.1)
            for entity in entity_sprites:
                if entity.selected:
                    entity.show_indicators = not entity.show_indicators
        if keys[pygame.K_g]:
            time.sleep(0.1)
            for entity in entity_sprites:
                entity.show_indicators = not entity.show_indicators

        # =======================deselect=======================
        if pygame.mouse.get_pressed()[2]:
            for entity in entity_sprites:
                entity.selected = False

        self.selected_units = len([entity for entity in entity_sprites if entity.selected])
        #========================input============================
        #selection box
        for entity in entity_sprites:
            if all([entity.rect.colliderect(self.box_rect[0] + self.offset[0],
                                            self.box_rect[1] + self.offset[1],
                                            self.box_rect[2], self.box_rect[3]),
                    entity.controllable, entity.alive]):
                entity.selected = True

    # ======================selection box====================
    def draw_selection_box(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[1] and not self.drawing:
            time.sleep(0.2)
            self.drawing = True
            self.pos_x = mouse_pos[0]
            self.pos_y = mouse_pos[1]

        elif any([pygame.mouse.get_pressed()[1] and self.drawing,
                  pygame.mouse.get_pressed()[2]]):
            time.sleep(0.2)
            self.drawing = False
            self.box_rect = [0, 0, 0, 0]

        if self.drawing:
            self.box_rect = self.create_box((self.pos_x, self.pos_y), (mouse_pos[0], mouse_pos[1]))
            pygame.draw.rect(self.display_surface, (0, 200, 0), self.box_rect, 2)

    @staticmethod
    def create_box(p1, p2):
        x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
        x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
        return pygame.Rect(x1, y1, x2 - x1, y2 - y1)

    #=========================ai update========================
    def ai(self):
        entity_sprites = [sprite for sprite in self.visible_sprites if hasattr(sprite, "entity_type")]
        enemies = [enemy for enemy in self.faction_enemy if enemy.alive]
        allies = [ally for ally in self.faction_ally if ally.alive]
        neutrals = [neutral for neutral in self.faction_neutral if neutral.alive]
        hostiles = [hostile for hostile in self.faction_omni_hostile if hostile.alive]

        # =======================switch behavior=======================
        self.switch_behavior(entity_sprites)
        # =======================change markers=======================
        self.change_markers_owner(entity_sprites)
        # =======================group_ai=======================
        if not self.level_paused:
            for entity in entity_sprites:
                if entity.alive:
                    entity.entity_ai()
                    entity.metadata = {"selected_units": self.selected_units}
        #targeting
        for neutral in neutrals:
            neutral.find_target(hostiles)
            neutral.alert_others(neutrals)
        for enemy in enemies:
            enemy.find_target(allies + hostiles)
            enemy.alert_others(enemies)
        for ally in allies:
            ally.find_target(enemies + hostiles)
            ally.alert_others(allies)
        for hostile in hostiles:
            hostile.find_target(enemies + allies + neutrals)
            hostile.alert_others(hostiles)

    #=========================draw obstacles==================
    def draw_obstacles(self):
        for obstacle in self.obstacle_sprites:
            pygame.draw.rect(self.display_surface, (255, 0, 0), (
                obstacle.rect.x - self.offset[0],
                obstacle.rect.y - self.offset[1],
                obstacle.rect.width,
                obstacle.rect.height), 3)

    #==========================================================
    def run(self):
        self.put_in_groups()
        self.visible_sprites.custom_draw(self.main_hero, self.surface_sprites)
        #self.draw_obstacles()
        self.draw_selection_box()
        self.input()
        #pause level and update
        if self.level_paused:
            self.level_menu_state = "pause"
        else:
            self.surface_sprites.update()
            self.visible_sprites.update()
            self.ai()
            self.enemy_ai.run(self.marker_sprites)
            self.toggle_unit_buttons()
            self.level_menu_state = None


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.width = self.display_surface.get_size()[0]
        self.height = self.display_surface.get_size()[1]
        #offset
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 3

        #zoom
        self.zoom_scale = 1
        self.internal_surf_size = (1600, 1600)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_width, self.half_height))

        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_width
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_height

        #box setup
        self.camera_borders = {"left": 20, "right": 20, "top": 50, "bottom": 10}
        left = self.camera_borders["left"]
        top = self.camera_borders["top"]
        width = self.display_surface.get_size()[0] - (self.camera_borders["left"] + self.camera_borders["right"])
        height = self.display_surface.get_size()[1] - (self.camera_borders["top"] + self.camera_borders["bottom"])
        self.camera_rect = pygame.Rect(left, top, width, height)

    #===================cameras======================
    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]

    def player_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_RIGHT]:
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_UP]:
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_DOWN]:
            self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_borders["left"]
        top_border = self.camera_borders["top"]
        right_border = self.display_surface.get_size()[0] - self.camera_borders["right"]
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders["bottom"]

        #===========horizontal adjustment=============
        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x -= self.mouse_speed
            if mouse.x > right_border:
                mouse_offset_vector.x += self.mouse_speed
        #==============corners adjustment==============
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector -= pygame.math.Vector2(self.mouse_speed, self.mouse_speed)
            if mouse.x > right_border:
                mouse_offset_vector += pygame.math.Vector2(self.mouse_speed, -self.mouse_speed)
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector += pygame.math.Vector2(-self.mouse_speed, self.mouse_speed)
            if mouse.x > right_border:
                mouse_offset_vector += pygame.math.Vector2(self.mouse_speed, self.mouse_speed)
        #===========vertical adjustment=============
        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y -= self.mouse_speed
            if mouse.y > bottom_border:
                mouse_offset_vector.y += self.mouse_speed

        self.offset += mouse_offset_vector * self.mouse_speed

    def input(self, target):
        keys = pygame.key.get_pressed()
        #===============zoom=============
        if keys[pygame.K_e]:
            if self.zoom_scale < 1.2:
                self.zoom_scale += 0.02
        if keys[pygame.K_q]:
            if self.zoom_scale > 0.8:
                self.zoom_scale -= 0.02
       #===========center camea=============
        if keys[pygame.K_x]:
            self.center_on_target(target)

    def center_on_target(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, target, surface_sprites):
        #==========camera types============
        #self.box_target_camera(player)
        #self.player_target_camera(player)
        #self.keyboard_control()
        self.mouse_control()
        #---------------zoom--------------
        self.internal_surf.fill(MAP_EDGE_COLOR)
        #==========input keyboard==========
        self.input(target)
        #=========sprites from surfaceSpriteGroup========
        for sprite in surface_sprites:
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            if all([TRIPLETILE < offset_pos[0] < self.width + (TRIPLETILE*2),
                    (TRIPLETILE*4) < offset_pos[1] < self.height + (TRIPLETILE*5)]):
                self.internal_surf.blit(sprite.image, offset_pos)

        #==============rendering sprites===============
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            if all([TILEANDHALF < offset_pos[0] < self.width + (TRIPLETILE*2),
                    (TRIPLETILE*4) < offset_pos[1] < self.height + (TRIPLETILE*5)]):
                self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, (int(self.internal_surf_size[0] * self.zoom_scale),
                                                                  int(self.internal_surf_size[1] * self.zoom_scale)))
        scaled_rect = scaled_surf.get_rect(center=(self.half_width, self.half_height))

        self.display_surface.blit(scaled_surf, scaled_rect)
