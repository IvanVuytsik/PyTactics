from settings import *
from importCSV import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.faction = 1

        self.image = pygame.image.load("./graphics/player/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]), center=pos)
        self.hitbox = self.rect.inflate(-TILESIZE, -TILESIZE)

        self.direction = pygame.math.Vector2()
        self.moving = False
        self.can_move = True

        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.05

        self.obstacle_sprites = obstacle_sprites

        self.selected_character = "rowan"

    # stats player
        self.personal_stats = {
            "rowan": {
                'unlocked': True,
                'portrait': load_image('./graphics/portraits/rowan.png'),
                'inventory': ['amulet', 'helmet', 'gloves', 'weapon', 'armor', 'weapon',
                              'ring', 'boots', 'ring', 'trinket', 'trinket', 'trinket']
                },
            "dunstan": {
                'unlocked': True,
                'portrait': load_image('./graphics/portraits/dunstan.png'),
                'inventory': ['amulet', 'helmet', 'gloves', 'weapon', 'armor', 'shield',
                              'ring', 'boots', 'ring', 'trinket', 'trinket', 'trinket']
                },
            "anselm": {
                'unlocked': False,
                'portrait': load_image('./graphics/portraits/anselm.png'),
                'inventory': ['amulet', 'helmet', 'gloves', 'weapon', 'armor', 'shield',
                              'ring', 'boots', 'ring', 'trinket', 'trinket', 'trinket']
            },
            "regina": {
                'unlocked': False,
                'portrait': load_image('./graphics/portraits/regina.png'),
                'inventory': ['amulet', 'helmet', 'gloves', 'bow', 'armor', 'cloak',
                              'ring', 'boots', 'ring', 'trinket', 'trinket', 'trinket']
            },
            "severin": {
                'unlocked': True,
                'portrait': load_image('./graphics/portraits/severin.png'),
                'inventory': ['amulet', 'helmet', 'gloves', 'wand', 'armor', 'cloak',
                              'ring', 'boots', 'ring', 'trinket', 'trinket', 'trinket']
            },
            "alba": {
                'unlocked': False,
                'portrait': load_image('./graphics/portraits/alba.png'),
                'inventory': ['amulet', 'helmet', 'gloves', 'wand', 'armor', 'cloak',
                              'ring', 'boots', 'ring', 'trinket', 'trinket', 'trinket']
            },
        }

    # branch stats
        self.stats = {'opportunist': 0, 'warlord': 0, 'scholar': 0, 'wanderer': 0, 'mystic': 0, 'witch': 0}
        self.max_stats = {'opportunist': 100, 'warlord': 100, 'scholar': 100, 'wanderer': 100, 'mystic': 100, 'witch': 100}
        self.upgrade_cost = {'opportunist': 100, 'warlord': 100, 'scholar': 100, 'wanderer': 100, 'mystic': 100, 'witch': 100}

    # army stats
        self.army_stats = {'melee': 0, 'ranged': 0, 'riders': 0, 'support': 1, 'siege': 0}
        self.max_army_stats = {'melee': 4, 'ranged': 4, 'riders': 4, 'support': 4, 'siege': 4}
        self.upgrade_army_cost = {'melee': 3000, 'ranged': 3000, 'riders': 3000, 'support': 3000, 'siege': 3000}

    # stats party
        self.party_speed = 1
        #-------------
        self.party_health = 100
        self.max_party_health = 100
        #-------------
        self.party_command = 100
        self.max_party_command = 100
        #-------------
        self.experience = 5000
        self.wealth = 50000

    # mutations
        self.regenerate_health = 0.05
        self.restore_command = 0.05

    def import_player_assets(self):
        character_path = "./graphics/player/"
        self.animations = {
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up': [], 'down': [], 'left': [], 'right': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.moving = False
            if 'idle' not in self.status:
                self.status += '_idle'
        else:
            self.moving = True

    def party_regen(self):
        if self.moving:
            if self.party_health < self.max_party_health:
                self.party_health += self.regenerate_health

            if self.party_command < self.max_party_command:
                self.party_command += self.restore_command

        if self.party_health > self.max_party_health:
            self.party_health = self.max_party_health

        if self.party_command > self.max_party_command:
            self.party_command = self.max_party_command

    def draw_rect(self, display, offsetX, offsetY):
        pygame.draw.rect(display, (255, 0, 0), (self.rect.x + offsetX, self.rect.y + offsetY, TILESIZE, TILESIZE), 2)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def input(self):
        keys = pygame.key.get_pressed()
        # x movement
        if self.can_move:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            # y movement
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

    #===============get data for upgrade menu=============
    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    #=========get data for troops upgrade menu============
    def get_army_cost_by_index(self, index):
        return list(self.upgrade_army_cost.values())[index]

    def get_army_value_by_index(self, index):
        return list(self.army_stats.values())[index]

    def move(self, speed):
        if self.direction.magnitude() != 0: # cant normalize 0
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.party_speed)
        self.party_regen()

        #debug(self.selected_character)
        #print(self.selected_character)