from settings import *


class GlobalAI:
    def __init__(self, resources, faction, decisions, base, markers):
        self.resources = resources
        self.faction = faction
        self.max_decisions = decisions
        self.decisions = 0
        self.base = base
        self.markers = markers
        self.timer = 0
        self.markers_list = []
        self.banners_list = []
        self.max_banners = len(self.markers_list)

    def generate_decision(self):
        self.timer += 0.1
        if self.timer >= 50 and self.decisions < self.max_decisions:
            self.timer = 0
            self.decisions += 1

    def check_markers(self, markers):
        for marker in markers:
            if marker.belongs != self.faction:
                self.markers_list.append(marker)

    def choose_marker(self):
        if self.decisions > 0 and len(self.markers_list) > 0:
            choice = random.choice(self.markers_list)
            self.decisions -= 1
            #print(choice.rect.center)

    def make_decision(self):
        pass
        #new_banner = Banner(choice.rect.center, )

    def run(self, markers):
        self.check_markers(markers)
        self.generate_decision()
        self.choose_marker()


class Banner(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, squad, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.squad = squad
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))

    def check_status(self):
        if len(self.squad) <= 0:
            self.kill()

    def run(self):
        self.check_status()