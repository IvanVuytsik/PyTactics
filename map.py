from settings import *
from importCSV import *


class Map:
    def __init__(self):
        self.image = UI_ElEMENTS['map']
        self.rect = self.image.get_rect()
        self.display_surface = pygame.display.get_surface()
        self.full_width = self.display_surface.get_size()[0]
        self.full_height = self.display_surface.get_size()[1]
        self.rect.x = int(self.full_width * 0.1)
        self.rect.y = int(self.full_height * 0.12)

    def update(self, player):

        self.display_surface.blit(self.image, self.rect)
        pygame.draw.rect(self.display_surface, PAPER_COLOR, self.rect, 10)
        pygame.draw.circle(self.display_surface, (0, 200, 0),
                           (player.rect.x // 4 + (TILESIZE * 5.75),
                            player.rect.y // 4 + (TILESIZE * 3)), 5)
