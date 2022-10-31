import pygame, time


# #---------selection box---------
# drawing = False
# pos_x = 0
# pos_y = 0
#
# #======================selection box====================
# def draw_selection_box(self):
#     mouse_pos = pygame.mouse.get_pos()
#     if pygame.mouse.get_pressed()[1] and not self.drawing:
#         time.sleep(0.1)
#         self.drawing = True
#         self.pos_x = mouse_pos[0]
#         self.pos_y = mouse_pos[1]
#     elif any([pygame.mouse.get_pressed()[1] and self.drawing,
#               pygame.mouse.get_pressed()[2]]):
#         time.sleep(0.1)
#         self.drawing = False
#
#     if self.drawing:
#         self.box_rect = self.create_box((self.pos_x, self.pos_y), (mouse_pos[0], mouse_pos[1]))
#         pygame.draw.rect(self.display_surface, (0, 200, 0), self.box_rect, 2)
#
#
# def create_box(self, p1, p2):
#     x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
#     x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
#     return pygame.Rect(x1, y1, x2-x1, y2-y1)
#
#
# #======drawing========
# draw_selection_box()
#
#
#
# #===============================selection brush=================
# selection_brush = False
#
# def draw_selection_brush(self):
#     mouse_pos = pygame.mouse.get_pos()
#     if pygame.mouse.get_pressed()[1] and not self.selection_brush:
#         time.sleep(0.1)
#         self.selection_brush = True
#
#     elif any([pygame.mouse.get_pressed()[1] and self.selection_brush,
#               pygame.mouse.get_pressed()[2]]):
#         self.selection_brush = False
#
#     if self.selection_brush:
#         pygame.draw.circle(self.surface, (0, 200, 0), mouse_pos, 20, 2)
#         if self.rect.collidepoint(mouse_pos + self.offset):
#             self.selected = True
#
# draw_selection_brush()
#==============================movement=================================
# import pygame as pg
# from pygame.math import Vector2
#
#
# class Player(pg.sprite.Sprite):
#
#     def __init__(self, pos, *groups):
#         super().__init__(*groups)
#         self.image = pg.Surface((30, 50))
#         self.image.fill(pg.Color('dodgerblue1'))
#         self.rect = self.image.get_rect(center=pos)
#         self.vel = Vector2(0, 0)
#         # Store the actual position as another vector because
#         # rect coordinates can only be integers.
#         self.pos = Vector2(pos)
#         self.max_speed = 5
#         self.goal = Vector2(pos)
#         self.goal_radius = 40
#
#     def update(self):
#         self.pos += self.vel  # Update the position vector first.
#         self.rect.center = self.pos  # Update the rect afterwards.
#
#         # This vector points to the goal.
#         heading = self.goal - self.pos
#         distance = heading.length()
#         # Normalize it, so that we can scale it to the desired length/speed below.
#         if heading:  # Can't normalize a zero vector.
#             heading.normalize_ip()
#
#         if distance > self.goal_radius:
#             # Move with maximum speed.
#             self.vel = heading * self.max_speed
#         else:
#             # Slow down when we're approaching the goal.
#             self.vel = heading * (distance/self.goal_radius * self.max_speed)
#
# def main():
#     screen = pg.display.set_mode((640, 480))
#     clock = pg.time.Clock()
#     all_sprites = pg.sprite.Group()
#     player = Player((100, 300), all_sprites)
#
#     done = False
#
#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             elif event.type == pg.MOUSEBUTTONDOWN:
#                 # Set the goal of the player.
#                 player.goal = Vector2(event.pos)
#
#         all_sprites.update()
#         screen.fill((30, 30, 30))
#         all_sprites.draw(screen)
#
#         pg.display.flip()
#         clock.tick(30)
#
# if __name__ == '__main__':
#     pg.init()
#     main()
#     pg.quit()

#======================================================================
# import
# import pygame
#
# # initialize pygame
# pygame.init()
#
# # frame rate variables
# FPS = 120
# clock = pygame.time.Clock()
#
# # game variables
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 800
#
# # colors
# BLUE = (0, 0, 255)
#
# # activate screen
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption('Bonker')
#
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         # init the sprite class
#         pygame.sprite.Sprite.__init__(self)
#         self.rect = pygame.Rect(0, 0, 40, 40)
#         self.rect.x = x
#         self.rect.y = y
#         self.radius = 20
#         self.destination = None
#         self.moving = False
#         self.dx = 0
#         self.dy = 0
#
#     def set_destination(self, pos):
#         self.destination = pos
#         # delta x and delta y
#         self.dx = self.destination[0] - self.rect.centerx
#         self.dy = self.destination[1] - self.rect.centery
#
#         self.moving = True
#
#     def move(self):
#         if self.rect.centerx != self.destination[0]:
#             if self.dx > 0:
#                 self.rect.centerx += 1
#             elif self.dx < 0:
#                 self.rect.centerx -= 1
#
#         if self.rect.centery != self.destination[1]:
#             if self.dy > 0:
#                 self.rect.centery += 1
#             elif self.dy < 0:
#                 self.rect.centery -= 1
#         elif self.rect.center == self.destination:
#             self.moving = False
#
#     def draw(self):
#         # draw the circle
#         pygame.draw.circle(screen, BLUE, self.rect.center, self.radius)
#
#
# # create instances
# # player instance
# player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# player.draw()
#
# # main loop
# run = True
# movetime = 100
# move = False
#
# while run:
#     # run frame rate
#     dt = clock.tick(FPS)
#     movetime -= dt
#     if movetime <= 0:
#         move = True
#         movetime = 400
#
#     # events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_pos = pygame.mouse.get_pos()
#             player.set_destination(mouse_pos)
#
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 run = False
#
#     if player.moving:
#         player.move()
#
#     screen.fill((0, 0, 0))
#     player.draw()
#     pygame.display.update()
#
# pygame.quit()

#======================================================================
# def draw_story(self, lore, xmodifier, ymodifier):
#     msg_list = []
#     line_spacing_count = 0
#     if self.rect.collidepoint(mouse_position) and encounter == False and self.rect.colliderect(player_party.rect):
#         display.blit(self.story_image, (self.rect.x - 120, self.rect.y + 10))
#         gm_draw_text(self.story_text, GM_font_TNR, (255, 225, 100), self.rect.x - 100, self.rect.y + 20)
#         for line in lore.split('\n'):
#             msg = GM_font_Lore.render(line, True, '#2c2d47')
#             msg_list.append(msg)
#             line_spacing_count += 20
#             display.blit(msg, (self.rect.x - xmodifier, self.rect.y + ymodifier + (line_spacing_count * 1)))
#         play_while_sound(scroll_sound)
# # -----------------------------------QuestTexts-----------------------------------
# old_ways_path = open('WorldMap/quest/old_ways.txt', 'r')
# old_ways_lore = old_ways_path.read()
# old_ways_path.close()



# Twelve years. That's a long time. Rowan was
# a promising soldier in his former life - a captain
# of the gray cloaks of His Royal Highness Rorrick IV.
# So how did you end up on this ship of exiles, murderers,
# and traitors to the crown? Though it is surely a
# long story full of drama, but not for my old ears. Not
# after such a long voyage to the mainland. Those island
# pirates almost caught up with us. A little longer and we'd
# have been feeding the sea devil or entertaining the empiri
# in the arenas of Kharfageth. Well, I'm sure you can't wait
# to get off the old Edora and hit the road.

#=======================================================================


# def show_bar(self, current, max_amount, bg_rect, color, bg_color):
#     pygame.draw.rect(self.display_surface, bg_color, bg_rect)
#     # ratio
#     ratio = current / max_amount
#     current_width = bg_rect.width * ratio
#     current_rect = bg_rect.copy()
#     current_rect.width = current_width
#     #draw bar
#     pygame.draw.rect(self.display_surface, color, current_rect)
#     #draw rect border if not at 100%
#     if current == max_amount:
#         pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

#=====================================================================

# def show_data(self, player_data, data_rect, color=TEXT_COLOR):
#     text_surf = self.font.render(str(int(player_data)), False, color)
#     text_rect = text_surf.get_rect(topleft=(data_rect.x, data_rect.y))
#     self.display_surface.blit(text_surf, text_rect)

#def show_party_stats(self):
# for index, stat in enumerate(self.stat_bars.keys()):
#     data = self.stat_bars
#     self.show_bar(data[stat]['min'], data[stat]['max'], data[stat]['rect'],
#                   data[stat]['color_primary'], data[stat]['color_secondary'])
#     self.display_surface.blit(data[stat]['image'],
#                               (data[stat]['rect'][0],
#                                data[stat]['rect'][1]))
#     if data[stat]['data'] is not None:
#         self.show_data(data[stat]['data'], data[stat]['rect'])
#=====================================================================
# if keys[pygame.K_d] and self.selection_index < self.stat_number - 1:
#     self.selection_index += 1
#     self.can_move = False
#     self.selection_time = pygame.time.get_ticks()
# if keys[pygame.K_a] and self.selection_index >= 1:
#     self.selection_index -= 1
#     self.can_move = False
#     self.selection_time = pygame.time.get_ticks()

#===========================status===========================================
# def draw_effects_and_status(self):
#     n = 0
#     if len(self.effects) > 0:
#         for index, effect in enumerate(self.effects):
#             n += 1
#             if n >= 7:
#                 n = 1
#             effect.update(self.rect.x - TILEANDHALF + (n * SEMITILE),
#                           self.rect.y - (TRIPLETILE if effect.resistance == 'will' else DOUBLETILE),
#                           self.offset)
            # effect.update(self.rect.x - (TILESIZE if effect.resistance == 'will' else -DOUBLETILE),
            #               self.rect.y + DOUBLETILE - (n * SEMITILE),
            #               self.offset)
#======================================================================
# class DamageText(pygame.sprite.Sprite):  # sprite is updated automatically
#     def __init__(self, x, y, damage, color):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = fontDMG.render(damage, True, color)
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)
#         self.counter = 0
#
#     def update(self):
#         # move text
#         self.rect.y -= 1
#         # delete after timer
#         self.counter += 1
#         if self.counter > 30:
#             self.kill()
#
# damage_text_group = pygame.sprite.Group()


# ground_sprites = [sprite for sprite in self.ground_sprites if hasattr(sprite, "sprite_type")]
# ---------draw ground tiles-----------
# for index, tile in enumerate(ground_sprites):
#     x = tile.rect.x // 10
#     y = tile.rect.y // 10
#     self.display_surface.blit(tile.image, (x + (DOUBLETILE * 3),
#                                              y + DOUBLETILE))
#===================================================

#def alert_others(self, others_list):
# if self.use_ability:
#     for entity in entity_sprites:
#         if all([self.hit, self.faction == entity.faction]):
#             entity.hit = True
#             entity.use_ability = False
#             self.use_ability = False

#==================================================
# def patrol_around(self, spread=True):
#     starting_point = self.rect.center
#     if not self.selected:
#         self.patrol_timer += 1
#         if self.patrol_timer >= random.randint(1000, 2000):
#             choice = random.choice([0, len(self.patrol_locations) - 1])
#             self.set_destination(self.patrol_locations[choice])
#             if starting_point == self.patrol_locations[choice] and spread:
#                 self.spread_out()
#             self.patrol_timer = 0



#==================================================
# match marker.belongs:
#     case 1: color = (0, 0, 200)
#     case 2: color = (200, 0, 0)
#     case _:  color = (0, 0, 0)
# pygame.draw.rect(self.display_surface, color,
#                  (marker.rect.x - self.offset[0],
#                   marker.rect.y - self.offset[1],
#                   marker.rect.width, marker.rect.height))
#==================================================
import pygame

class Ship(pygame.sprite.Sprite):

    def __init__(self, speed, color):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.set_colorkey((12,34,56))
        self.image.fill((12,34,56))
        pygame.draw.circle(self.image, color, (5, 5), 3)
        self.rect = self.image.get_rect()

        self.pos = pygame.Vector2(0, 0)
        self.set_target((0, 0))
        self.speed = speed

    def set_target(self, pos):
        self.target = pygame.Vector2(pos)

    def update(self):
        move = self.target - self.pos
        move_length = move.length()

        if move_length < self.speed:
            self.pos = self.target
        elif move_length != 0:
            move.normalize_ip()
            move = move * self.speed
            self.pos += move

        self.rect.topleft = list(int(v) for v in self.pos)

def main():
    pygame.init()
    quit = False
    screen = pygame.display.set_mode((300, 300))
    clock = pygame.time.Clock()

    group = pygame.sprite.Group(
        Ship(1.5, pygame.Color('white')),
        Ship(3.0, pygame.Color('orange')),
        Ship(4.5, pygame.Color('dodgerblue')))

    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for ship in group.sprites():
                    ship.set_target(pygame.mouse.get_pos())

        group.update()
        screen.fill((20, 20, 20))
        group.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()