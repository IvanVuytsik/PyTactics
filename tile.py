import pygame
from settings import *
from entity import IndicationBar


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface

        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.hitbox = self.rect.inflate(-QUARTERTILE, -QUARTERTILE)

        match sprite_type:
            case 'mine': self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
            case _:
                pass


class Biome(Tile):
    def __init__(self, pos, groups, sprite_type, surface, biome_type):
        super().__init__(pos, groups, sprite_type, surface)
        self.biome_type = biome_type


class Marker(Tile):
    def __init__(self, pos, groups, sprite_type, surface):
        super().__init__(pos, groups, sprite_type, surface)
        self.belongs = None


class LevelTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.hitbox = self.rect.inflate(-HALFTILE, -HALFTILE)

        match sprite_type:
            case 'tree': #64x96
                self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILEANDHALF))
                self.hitbox = self.rect.inflate(-(self.rect.width * 0.6), -(self.rect.height * 0.5))
            case 'prop': #64x64
                self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - HALFTILE))
                self.hitbox = self.rect.inflate(-(self.rect.width * 0.7), -(self.rect.height * 0.7))
            case 'building': #128x128
                self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - DOUBLETILE))
                self.hitbox = self.rect.inflate(-(self.rect.width * 0.7), -(self.rect.height * 0.7))
            case _:
                pass


class FogTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface=pygame.Surface((DOUBLETILE, DOUBLETILE))):
        super().__init__(groups)
        self.image = surface
        self.rect = pygame.Rect(pos[0], pos[1], DOUBLETILE, DOUBLETILE)


class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, animation_type):
        super().__init__(groups)
        self.animated_data = {
            '': import_folder(''),
        }

        self.sprite_type = sprite_type
        self.frame_index = 0
        self.animation_speed = 0.25
        self.frames = self.animated_data[animation_type]
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-QUARTERTILE, -QUARTERTILE)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()


class Construction(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, entity_type, surface, display, offset,
                 params, particles, controllable=False, faction=0):
        super().__init__(groups)
        self.offset = offset
        self.display_surface = display
        self.particles = particles
        self.visible_sprites = groups[0]
        self.obstacle_sprites = groups[1]
        self.description_font = pygame.font.Font(TEXT_FONT, TEXT_FONT_MD)
        self.show_indicators = False
        self.faction = faction
        self.controllable = controllable
        self.sprite_type = sprite_type
        self.entity_type = entity_type
        self.image = surface
        self.rect = self.image.get_rect()
        self.banner = BANNERS[self.faction]
        self.selected = False
        self.health = params["health"]
        self.max_health = self.health
        self.fortitude = 100
        self.notice_area = 100
        self.armor = 0
        self.alive = True
        self.hit = False
        self.engaged = False
        self.mode = None

        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.hitbox = self.rect.inflate(-(self.rect.width * 0.7), -(self.rect.height * 0.7))

        self.healthBar = IndicationBar(self.display_surface, self.rect.width, QUARTERTILE,
                                       HEALTH_COLOR_POSITIVE, HEALTH_COLOR_NEGATIVE)

        self.spawn_rect = self.spawn_field()

    def spawn_field(self):
        spawn_rect = pygame.rect.Rect(self.rect.x - DOUBLETILE - self.offset[0],
                                      self.rect.y + DOUBLETILE - self.offset[1],
                                      FIVETILES, FIVETILES)
        return spawn_rect

    def draw_selection(self):
        a = (self.rect.midtop - pygame.math.Vector2(0, 40)) - self.offset
        b = (self.rect.topright - pygame.math.Vector2(20, 20)) - self.offset
        c = (self.rect.topleft + pygame.math.Vector2(20, -20)) - self.offset

        if all([self.alive and self.selected]):
            pygame.draw.polygon(self.display_surface, SELECTION_COLOR, [a, b, c])
        if all([self.alive and self.show_indicators]):
            self.healthBar.draw(self.rect.x, self.rect.y - QUARTERTILE,
                                self.offset, self.health, self.max_health)
        self.spawn_field()

    def check_status(self):
        if self.health < 0:
            self.health = 0
            self.alive = False
            sound_manager(SOUND_BANK["ruined"])
            self.particles.create_particles("smoke", self.rect.center, self.visible_sprites)
            self.kill()
        if self.armor < 0:
            self.armor = 0

    def entity_ai(self, *args):
        pass

    def find_target(self, *args):
        pass

    def alert_others(self, *args):
        pass

    def set_destination(self, *args):
        pass

    def draw_banner(self):
        self.display_surface.blit(self.banner, (self.rect.x - self.offset[0],
                                                self.rect.y - self.offset[1] - DOUBLETILE))

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        if all([self.rect.collidepoint(mouse_pos + self.offset),
                pygame.mouse.get_pressed()[0], self.controllable]):
            self.selected = True
        if all([pygame.mouse.get_pressed()[2]]):
            self.selected = False

    def update(self):
        self.check_status()
        self.input()
        self.draw_banner()
        self.draw_selection()

