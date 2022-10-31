import pygame.math
from importCSV import *
from settings import *
from threading import Timer


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, entity_type, offset, particles, faction=0,
                 controllable=True, metadata=None):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.display.get_surface().convert_alpha()
        # ============rendering==================
        self.obstacle_sprites = obstacle_sprites[0]
        self.surface_sprites = obstacle_sprites[1]
        self.offset = offset  # specific to rendering when offset is used
        self.visible_sprites = groups
        self.particles = particles
        # ==============metadata=================
        self.metadata = metadata
        # =======================================
        self.selected = False
        self.controllable = controllable
        self.size = UNIT_DATA[entity_type]["size"]
        self.mode = "offensive"  #  "offensive" "defensive", "passive", "patrol"

        self.import_graphics(entity_type)
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.025

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - HALFTILE), center=pos)
        self.hitbox = self.rect.inflate(-TILESIZE, -TILESIZE)
        # ============================
        self.alive = True
        self.faction = faction
        self.entity_type = entity_type
        # ===========params===========
        self.speed = UNIT_DATA[entity_type]["speed"]

        self.health = UNIT_DATA[entity_type]["health"]
        self.max_health = UNIT_DATA[entity_type]["health"]

        self.armor = UNIT_DATA[entity_type]["armor"]
        self.max_armor = UNIT_DATA[entity_type]["armor"]

        self.will = UNIT_DATA[entity_type]["will"]  # magic/effects resistances
        self.might = UNIT_DATA[entity_type]["might"]  # attack power
        self.reflex = UNIT_DATA[entity_type]["reflex"]  # action restoration, deflection
        self.fortitude = UNIT_DATA[entity_type]["fortitude"]  # defence

        self.range = UNIT_DATA[entity_type]["range"]
        self.weapon = UNIT_DATA[entity_type]["weapon"]
        self.notice = UNIT_DATA[entity_type]["notice"]

        # critical strike and effects
        self.critical_chance = self.might // 5 if self.might > 0 else 0
        self.critical_effect = UNIT_DATA[entity_type]["special_effect"]
        # ==========action points=======
        self.action_timer = 0.25 + (self.reflex / 100) if self.reflex != 0 else 0.25
        self.action_points = 100
        self.max_action_points = 100
        # =============movement=========
        self.moving = False
        self.dx = pos[0]
        self.dy = pos[1]
        self.destination = pos
        # =============actions===========
        self.patrol_timer = 0
        self.patrol_locations = []
        # ==============areas=============
        self.alert_area = self.rect.inflate(self.notice * 2.5, self.notice * 2.5)
        self.normal_area = self.rect.inflate(self.notice, self.notice)
        self.notice_area = self.normal_area
        self.engage_area = self.rect.inflate(self.range, self.range)

        # ===============effects=====================
        self.effects = pygame.sprite.Group()
        # ==============indicators==================
        self.show_indicators = False
        self.healthBar = IndicationBar(self.display_surface, self.hitbox.width, QUARTERTILE, HEALTH_COLOR_POSITIVE,
                                       HEALTH_COLOR_NEGATIVE)
        self.armorBar = IndicationBar(self.display_surface, self.hitbox.width, QUARTERTILE, EXP_COLOR, BONE_COLOR)
        self.actionBar = IndicationBar(self.display_surface, self.hitbox.width, QUARTERTILE, ACTION_PRIMARY,
                                       ACTION_SECONDARY)
        # ============direction===========
        self.direction = pygame.math.Vector2()
        self.flip = False
        self.collision_type = ''
        # ============targeting===========
        self.target = None
        self.hit = False
        # ============engaging============
        self.engaged = False
        # =============sounds=============
        self.sounds = SOUND_BANK

        # for i in STATUS.keys():
        #     self.effects.add(StatusEffect(i))
        # self.effects.add(StatusEffect('bleeding'))

    def import_graphics(self, entity_type):
        full_path = f'./graphics/characters/{entity_type}/'
        self.animations = {'idle': [], "attack": [], "move": [], "dead": []}
        for animation in self.animations.keys():
            if self.size == "big":
                self.animations[animation] = import_folder_and_scale(full_path + animation, TRIPLETILE, TRIPLETILE)
            else:
                self.animations[animation] = import_folder_and_scale(full_path + animation, DOUBLETILE, DOUBLETILE)

    def draw_mode(self):
        match self.mode:
            case "offensive":
                self.display_surface.blit(UI_ElEMENTS["offense_icon"], self.rect.topright - self.offset)
            case "defensive":
                self.display_surface.blit(UI_ElEMENTS["defense_icon"], self.rect.topright - self.offset)
            case "patrol":
                self.display_surface.blit(UI_ElEMENTS["patrol_icon"], self.rect.topright - self.offset)
            case _:
                pass

    def draw_indicators(self):
        # ==========selection================
        a = (self.rect.midtop - pygame.math.Vector2(0, 40)) - self.offset
        b = (self.rect.topright - pygame.math.Vector2(20, 20)) - self.offset
        c = (self.rect.topleft + pygame.math.Vector2(20, -20)) - self.offset

        if all([self.alive and self.selected]):
            pygame.draw.polygon(self.display_surface, SELECTION_COLOR, [a, b, c])

        if all([self.alive and self.show_indicators]):
            # ===============indicators================
            self.healthBar.draw(self.rect.x + HALFTILE, self.rect.y - QUARTERTILE, self.offset, self.health,
                                self.max_health)
            self.armorBar.draw(self.rect.x + HALFTILE, self.rect.y - HALFTILE, self.offset, self.armor,
                               self.max_armor)
            self.actionBar.draw(self.rect.x + HALFTILE, self.rect.y, self.offset, self.action_points,
                                self.max_action_points)
            # ===============statuses/effects================
            self.draw_effects_and_status()
            self.draw_mode()
            # ================destintion line=================
            if self.selected:
                self.draw_destination_line()
        # =============areas======================
        self.draw_engage_area()
        self.draw_notice_area()
        # ===================debug rect/hitbox=====================
        # pygame.draw.rect(self.surface, (250, 0, 0), (self.rect.x - self.offset[0],
        #                                              self.rect.y - self.offset[1],
        #                                              self.rect.width, self.rect.height), 3)
        # pygame.draw.rect(self.surface, (0, 0, 250), (self.hitbox.x - self.offset[0],
        #                                              self.hitbox.y - self.offset[1],
        #                                              self.hitbox.width, self.hitbox.height), 3)

    def update_effects_and_status(self):
        if len(self.effects) > 0:
            for index, effect in enumerate(self.effects):
                effect.update(self.rect.x - QUARTERTILE, self.rect.y + TILEANDHALF - (index * HALFTILE),
                              self.offset, self, self.particles, self.visible_sprites)

    def draw_effects_and_status(self):
        if len(self.effects) > 0:
            self.effects.draw(self.display_surface)

    def draw_notice_area(self):
        self.notice_area.centerx = self.rect.centerx - self.offset[0]
        self.notice_area.centery = self.rect.centery - self.offset[1]
        # pygame.draw.rect(self.surface, (0, 250, 0), self.notice_area, 3)

    def draw_engage_area(self):
        self.engage_area.centerx = self.rect.centerx - self.offset[0]
        self.engage_area.centery = self.rect.centery - self.offset[1]
        # pygame.draw.rect(self.surface, (50, 250, 120), self.engage_area, 3)

    def animate(self):
        animation = self.animations[self.status]
        animation_speed = self.animation_speed * len(animation)
        self.frame_index += animation_speed
        if self.frame_index >= len(animation):
            if not self.alive:
                self.frame_index = len(animation) - 1
            else:
                self.frame_index = 0
        loaded_image = animation[int(self.frame_index)]
        self.image = pygame.transform.flip(loaded_image, self.flip, False)

    def check_direction(self):
        if self.target is not None:
            if all([self.notice_area.collidepoint(self.target.rect.center - self.offset),
                    self.rect.left > self.target.rect.left]):
                self.flip = True
            else:
                self.flip = False
        return self.flip

    @staticmethod
    def update_params(param):
        if param < 0:
            param = 0
        return param

    def restore_status_timer(self):
        t = Timer(2, self.restore_status)
        if any([self.hit]):
            t.start()

    def restore_status(self):
        self.hit = False

    def check_status(self):
        # ===========params===========
        params = [self.will, self.might, self.fortitude, self.reflex,
                  self.action_points]

        map(self.update_params, params)
        # ===========alert===========
        self.alerted()
        self.restore_status_timer()

        # ===========statuses===========
        if self.armor < 0:
            self.armor = 0
        elif self.armor > self.max_armor:
            self.armor = self.max_armor

        if self.health < 0:
            self.health = 0
            self.alive = False
            self.update_status("dead")
        elif self.health > self.max_health:
            self.health = self.max_health

        if self.alive:
            self.update_effects_and_status()

    def update_status(self, new_status):
        if new_status != self.status:
            self.status = new_status
            self.frame_index = 0
        return self.status

    def draw_destination_line(self):
        destination_line = pygame.draw.line(self.display_surface, SELECTION_COLOR,
                                            (self.rect.centerx - self.offset[0], self.rect.centery - self.offset[1]),
                                            (
                                            self.destination[0] - self.offset[0], self.destination[1] - self.offset[1]))
        return destination_line

    def set_destination(self, destination, include_spread=True):
        selected_units = self.metadata["selected_units"] * 3
        a = -(30 + selected_units)
        b = (30 + selected_units)
        self.destination = destination + self.spread(a, b) if include_spread else destination
        self.dx = int(self.destination[0] - self.rect.centerx)
        self.dy = int(self.destination[1] - self.rect.centery)
        if self.dx > 0:
            self.direction[0] = 1
            self.flip = False
        if self.dx < 0:
            self.direction[0] = -1
            self.flip = True
        if self.dy > 0:
            self.direction[1] = -1
        if self.dy < 0:
            self.direction[1] = 1
        self.check_direction()

    def find_target(self, target_list):
        mouse_pos = pygame.mouse.get_pos()
        targets = target_list
        available_targets = []
        if all([self.selected, pygame.mouse.get_pressed()[0]]):
            for target in targets:
                if target.rect.collidepoint(mouse_pos + self.offset):
                    self.target = target
                else:
                    self.target = None
        else:
            for target in targets:
                if all([self.notice_area.collidepoint(target.rect.center - self.offset)]):
                    available_targets.append(target)
            # choosing target from available targets
            if all([len(available_targets) > 0, self.target is None, not self.selected]):
                self.target = random.choice(available_targets)

    @staticmethod
    def throw_dice():
        dice = random.randint(0, 100)
        return dice

    def calculate_damage(self):
        self.target.hit = True
        self.target.armor -= int(self.might * (self.target.fortitude / 100))
        if self.target.armor > self.might:
            self.target.health -= int(self.might * (1 - self.target.fortitude / 100))
        elif 0 < self.target.armor < self.might:
            damage = self.might - self.target.armor
            self.target.health -= damage
        else:
            self.target.health -= self.might

    def critical_strike(self):
        self.target.armor -= self.might * 1.5
        self.target.health -= self.might * 1.5
        self.target.effects.add(StatusEffect(self.critical_effect))
        self.target.hit = True

    def attack(self):
        if all([self.engaged, self.action_points >= self.max_action_points, self.target.alive]):
            match self.target.entity_type:
                case "construction":
                    self.calculate_damage()
                case _:
                    if self.critical_chance >= self.target.throw_dice():
                        self.critical_strike()
                    elif self.target.reflex < self.target.throw_dice():
                        self.calculate_damage()
                        self.particles.create_particles("bleeding", self.target.rect.center, self.visible_sprites)
                    else:
                        self.target.action_points -= 10
            sound_manager(SOUND_BANK[self.weapon])
            self.action_points = 0
        # limit status duration
        if all([self.action_points < 10 + (self.reflex * 0.25)]):
            self.update_status("attack")
        else:
            self.update_status("idle")

    def follow_target(self):
        if all([self.target is not None, not self.selected]):
            if not self.hitbox.colliderect(self.target.hitbox):
                self.set_destination(self.target.hitbox.center + self.spread(-TILESIZE, TILESIZE))
            if not self.notice_area.collidepoint(self.target.rect.center - self.offset):
                self.target = None

    def engage_target(self):
        if self.target is not None and self.target.alive:
            if self.engage_area.collidepoint(self.target.rect.center - self.offset):
                self.engaged = True
                self.stop()
                self.attack()
            else:
                self.engaged = False
        else:
            self.target = None

    def set_patrol_points(self):
        starting_point = self.rect.center
        height = self.display_surface.get_size()[1]
        mouse_pos = pygame.mouse.get_pos()
        if all([pygame.mouse.get_pressed()[0], self.selected,
                not self.rect.collidepoint(mouse_pos + self.offset),
                mouse_pos[1] > height * 0.1]):
            self.patrol_locations = [starting_point]
            new_patrol_point = mouse_pos + self.offset
            self.patrol_locations.append(new_patrol_point)
            # ==========patrol===========
            self.patrol()

    def patrol(self):
        if len(self.patrol_locations) > 0:
            if self.rect.collidepoint(self.patrol_locations[0]) and not self.moving:
                self.set_destination(self.patrol_locations[1], include_spread=False)
            if self.rect.collidepoint(self.patrol_locations[1]) and self.moving:
                self.set_destination(self.patrol_locations[0], include_spread=False)

    def idle_move(self):
        if not self.selected:
            self.patrol_timer += 1
            if self.patrol_timer >= random.randint(100, 300):
                destination = self.rect.center + self.spread(-50, 50)
                for sprite in self.obstacle_sprites:
                    if not sprite.rect.collidepoint(destination + self.offset):
                        self.set_destination(destination)
                self.patrol_timer = 0

    def stop(self):
        self.destination = self.rect.center

    def spread_out(self):
        self.set_destination(self.rect.center + self.spread(-30, 30))

    def move(self):
        # movement x
        if self.rect.centerx != self.destination[0]:
            self.rect.centerx += self.direction[0] * self.speed
        else:
            self.direction[0] = 0
            self.dx = 0
        # movement y
        if self.rect.centery != self.destination[1]:
            self.rect.centery -= self.direction[1] * self.speed
        else:
            self.direction[1] = 0
            self.dy = 0
        # status update
        if self.direction[0] or self.direction[1] != 0:
            self.update_status("move")
            self.moving = True
        else:
            self.moving = False
            if any([self.status != "attack", self.target is None]):
                self.update_status("idle")
        # rect to hitbox
        self.hitbox.center = self.rect.center
        # if self.selected:
        #     print(self.destination, self.direction, self.status, self.dx, self.dy)

    def collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if all([self.direction[0] == 1, self.hitbox.right >= sprite.hitbox.left]):
                    self.rect.right -= 5
                    self.collision_type = "right"
                    if self.rect.centery > sprite.rect.centery:
                        self.rect.y += 5
                    else:
                        self.rect.y -= 5
                elif all([self.direction[0] == -1 and self.hitbox.left <= sprite.hitbox.right]):
                    self.rect.left += 5
                    self.collision_type = "left"
                    if self.rect.centery > sprite.rect.centery:
                        self.rect.y += 5
                    else:
                        self.rect.y -= 5
                if all([self.direction[1] == 1 and self.hitbox.top <= sprite.hitbox.bottom]):
                    self.rect.top += 5
                    self.collision_type = "top"
                    if self.rect.centerx > sprite.rect.centerx:
                        self.rect.x += 5
                    else:
                        self.rect.x -= 5
                elif all([self.direction[1] == -1 and self.hitbox.bottom >= sprite.hitbox.top]):
                    self.rect.bottom -= 5
                    self.collision_type = "bottom"
                    if self.rect.centerx > sprite.rect.centerx:
                        self.rect.x += 5
                    else:
                        self.rect.x -= 5
                # =======stop after collision======
                self.hitbox.center = self.rect.center
                # self.stop()
            else:
                self.collision_type = ""

    def restore_action_points(self):
        if self.action_points < self.max_action_points:
            self.action_points += self.action_timer
        elif self.action_points >= self.max_action_points:
            self.action_points = self.max_action_points

    # =======================actions=======================
    def actions(self):
        self.restore_action_points()
        if self.moving:
            self.collision()
        if all([self.mode == "passive"]):
            self.idle_move()
            self.engage_target()
        if all([self.mode == "patrol"]):
            self.set_patrol_points()
            self.patrol()
            self.engage_target()
        if all([self.mode == "defensive"]):
            self.engage_target()
        if all([self.mode == "offensive"]):
            self.follow_target()
            self.engage_target()

    @staticmethod
    def spread(minimum, maximum):
        random_number = pygame.math.Vector2((random.randint(minimum, maximum),
                                             random.randint(minimum, maximum)))
        return random_number

    # ==========================alert=========================
    def alerted(self):
        if self.hit:
            self.notice_area = self.alert_area
        else:
            self.notice_area = self.normal_area

    # ==================alert_environment=====================
    def alert_others(self, target_list):
        alert_list = target_list
        alert_targets = []
        for target in alert_list:
            if all([self.notice_area.collidepoint(target.rect.center - self.offset)]):
                alert_targets.append(target)
            if self.hit:
                target.hit = True
        #
        # if self.selected:
        #     print(len(alert_targets))

    # ======================mouse control====================
    def mouse_control(self):
        height = self.display_surface.get_size()[1]
        mouse_pos = pygame.mouse.get_pos()
        collision_check = False
        is_surface = False

        # move to position collision check
        if pygame.mouse.get_pressed()[0]:
            for sprite in self.obstacle_sprites:
                if sprite.rect.collidepoint(mouse_pos + self.offset):
                    collision_check = True
            for sprite in self.surface_sprites:
                if sprite.rect.collidepoint(mouse_pos + self.offset):
                    is_surface = True

        # controls
        if all([pygame.mouse.get_pressed()[0],
                self.hitbox.collidepoint(mouse_pos + self.offset),
                self.selected is False, self.controllable is True, self.alive]):
            time.sleep(0.05)
            self.selected = True

        elif all([pygame.mouse.get_pressed()[0],
                  self.hitbox.collidepoint(mouse_pos + self.offset),
                  self.selected]):
            # time.sleep(0.05)
            self.selected = False

        elif all([pygame.mouse.get_pressed()[0],
                  mouse_pos[1] > height * 0.1,
                  not self.hitbox.collidepoint(mouse_pos + self.offset),
                  not collision_check, is_surface, self.selected]):
            destination = mouse_pos + self.offset
            self.set_destination(destination)

    def update(self):
        self.check_status()
        self.animate()
        self.draw_indicators()

    def entity_ai(self):
        self.mouse_control()
        self.move()
        self.actions()


class IndicationBar:
    def __init__(self, surface, length, width, color_primary, color_secondary):
        self.surface = surface
        self.color_primary = color_primary
        self.color_secondary = color_secondary
        self.length = length
        self.width = width

    def draw(self, x, y, offset, param, max_param):
        ratio = param / max_param if param != 0 else 0
        # pygame.draw.rect(self.surface, (225, 225, 0), (self.x - self.offset[0], self.y - self.offset[1], self.length, self.width, 3))
        pygame.draw.rect(self.surface, self.color_secondary, (x - offset[0], y - offset[1], self.length, self.width))
        pygame.draw.rect(self.surface, self.color_primary,
                         (x - offset[0], y - offset[1], self.length * ratio, self.width))


class StatusEffect(pygame.sprite.Sprite):
    def __init__(self, effect_type):
        super().__init__()
        self.effect = effect_type
        self.start_timer = 0
        self.image = STATUS[self.effect]['image']
        self.influences = STATUS[self.effect]['effect']
        self.power = STATUS[self.effect]['power']
        self.timer = STATUS[self.effect]['timer']
        self.duration = STATUS[self.effect]['duration']
        self.resistance = STATUS[self.effect]['resistance']
        self.sound = STATUS[self.effect]['sound']
        self.rect = self.image.get_rect()

    def create_effect(self, target, particles, sprite_group):
        self.start_timer += self.timer
        if self.start_timer >= self.duration:
            self.start_timer = 0
            particles.create_particles(self.effect, target.rect.center, sprite_group)
            sound_manager(SOUND_BANK[self.sound])
            for effect in self.influences:
                match effect:
                    case 'health':
                        target.health -= self.power
                    case 'armor':
                        target.armor -= self.power
                    case 'will':
                        target.will -= self.power
                    case 'might':
                        target.might -= self.power
                    case 'fortitude':
                        target.fortitude -= self.power
                    case 'reflex':
                        target.reflex -= self.power
                    case 'faction':
                        target.faction = self.power
                    case 'action_points':
                        target.action_points -= self.power
                    case _:
                        pass
            # ressist effect
            dice = target.throw_dice()
            if dice <= (target.will if self.resistance == 'will' else target.fortitude):
                self.kill()

    def update(self, x, y, offset, target, particles, sprite_group):
        self.rect.x, self.rect.y = x - offset[0], y - offset[1]
        self.create_effect(target, particles, sprite_group)
