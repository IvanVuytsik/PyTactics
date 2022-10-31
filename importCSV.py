import os
from csv import reader
from os import walk
import pygame
import time
import random


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')

        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_music_theme(path):
    music_theme = pygame.mixer.Sound(path)
    return music_theme


def sound_manager(theme, volume=0.5):
    music_theme = theme
    music_theme.set_volume(volume)
    music_theme.play(0)


def load_image_and_scale(path, scale_x, scale_y):
    image_base = pygame.image.load(path)
    image_surf = pygame.transform.scale(image_base, (scale_x, scale_y))
    return image_surf


def load_image(path, scale_x=64, scale_y=64):
    image_base = pygame.image.load(path)
    image_surf = pygame.transform.scale(image_base, (scale_x, scale_y))
    return image_surf


def import_text(path):
    read_text = open(path, 'r')
    text = read_text.read()
    read_text.close()
    return text


def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


def import_folder_and_scale(path, scale_x, scale_y):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_base = pygame.image.load(full_path)
            image_surf = pygame.transform.scale(image_base, (scale_x, scale_y)).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

#use only for numbered file names (e.g. _0, _1, etc.
#structure: folder_name('name') / file_name(name_0.png)
def import_indexed_animations(path, scale_x, scale_y):
    surface_list = []
    folder_name = path.split('/')[-1]
    _,__,img_files = next(os.walk(path))
    file_count = len(img_files)

    for i in range(file_count):
        full_path = path + '/' + folder_name + f'_{i}' + '.png'
        base_img = pygame.image.load(full_path)
        img = pygame.transform.scale(base_img, (scale_x, scale_y)).convert_alpha()
        surface_list.append(img)
    return surface_list


def load_animations(entity_type, animation_types, scale_x, scale_y, path="./graphics/characters"):
    #path - provide as follows: ./path/{character_type}/...
    #animation types should correspond to ones in the folder
    animation_list = []
    animation_types = animation_types
    for animation in animation_types:
        num_of_frames = len(os.listdir(f'{path}/{entity_type}/{animation}'))
        for i in range(num_of_frames):
            img = pygame.image.load(f'{path}/{entity_type}/{animation}/{i}.png')
            # img = pygame.transform.scale(img, (scale_x, scale_y)).convert_alpha()
            animation_list.append(img)
    return animation_list


