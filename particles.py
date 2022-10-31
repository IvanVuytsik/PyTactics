from settings import *


class Particles:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.frames = {
            'bleeding': import_folder_and_scale(f'graphics/particles/blood', TILESIZE, DOUBLETILE),
            'burning': import_folder_and_scale(f'graphics/particles/fire', DOUBLETILE, DOUBLETILE),
            'thunder': import_folder_and_scale(f'graphics/particles/thunder', TILESIZE, DOUBLETILE),
            'blinded': import_folder_and_scale(f'graphics/particles/aura', DOUBLETILE, DOUBLETILE),
            'poisoned': import_folder_and_scale(f'graphics/particles/aura', DOUBLETILE, DOUBLETILE),
            'weakened': import_folder_and_scale(f'graphics/particles/aura', DOUBLETILE, DOUBLETILE),
            'corrosion': import_folder_and_scale(f'graphics/particles/aura', DOUBLETILE, DOUBLETILE),
            'dying': import_folder_and_scale(f'graphics/particles/aura', DOUBLETILE, DOUBLETILE),
            'bloodthirsty': import_folder_and_scale(f'graphics/particles/aura', DOUBLETILE, DOUBLETILE),
            'cursed': import_folder_and_scale(f'graphics/particles/darkness', DOUBLETILE, DOUBLETILE),
            'electrified': import_folder_and_scale(f'graphics/particles/aura', DOUBLETILE, DOUBLETILE),
            'frozen': import_folder_and_scale(f'graphics/particles/aura', DOUBLETILE, DOUBLETILE),
            'confused': import_folder_and_scale(f'graphics/particles/aura', DOUBLETILE, DOUBLETILE),
            'smoke': import_folder_and_scale(f'graphics/particles/smoke', DOUBLETILE, DOUBLETILE),
        }

    def create_particles(self, particle_type, pos, groups):
        animation_frames = self.frames[particle_type]
        ParticleEffect(animation_frames, pos, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, animation_frames, pos, groups):
        super().__init__(groups)
        self.surface = pygame.display.get_surface()
        self.frame_index = 0
        self.animation_speed = 0.2
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()


