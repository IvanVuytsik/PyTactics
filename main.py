import sys
import pygame
from settings import *
from debug import *
from world import NewWorld
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('PyTactics')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.display_surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        #cursor
        pygame.mouse.set_visible(False)
        self.cursor_img = pygame.image.load("./graphics/cursor/cursor.png").convert_alpha()
        self.mouse_pos = (0, 0)
        self.l_mouse_clicked = False
        self.r_mouse_clicked = False

        #create game world
        self.world = NewWorld()

        #create level
        #self.level = Level(self.world.player)


    def create_cursor(self):
        cursor_pos = pygame.mouse.get_pos()
        self.display_surface.blit(self.cursor_img, cursor_pos)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #=========keys=======
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if self.world.world_state == "overworld":
                        if event.key == pygame.K_SPACE:
                            self.world.toggle_pause()



                    if self.world.world_state == "tactical":
                        if event.key == pygame.K_z:
                            self.world.toggle_overworld_mode()

            #=========mouse=========
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.l_mouse_clicked = True
                        #self.mouse_pos = pygame.mouse.get_pos()
                        #self.pos_x = self.mouse_pos[0] // TILESIZE
                        #self.pos_y = self.mouse_pos[1] // TILESIZE
                        #print('Left Click!', self.mouse_pos, self.l_mouse_clicked,self.pos_x, self.pos_y)

                    if event.button == 3:
                        self.r_mouse_clicked = True
                        #self.mouse_pos = pygame.mouse.get_pos()
                        #print('Right Click!', self.mouse_pos, self.r_mouse_clicked)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.l_mouse_clicked = False
                    if event.button == 3:
                        self.r_mouse_clicked = False

            #screen and display
            self.screen.fill(MAP_EDGE_COLOR)
            #run map
            self.world.run([self.l_mouse_clicked, self.r_mouse_clicked, self.mouse_pos])

            #run level
            #self.level.run([self.l_mouse_clicked, self.r_mouse_clicked, self.mouse_pos])

            # ==========create_cursor=============
            self.mouse_pos = pygame.mouse.get_pos()
            self.create_cursor()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__=='__main__':
    game = Game()
    game.run()