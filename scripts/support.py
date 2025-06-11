import os
import pygame
from csv import reader
from settings import tile_size, player_sprite_size
import random

def import_cut_graphics(path):
    """Cut graphics from tileset."""
    try:
        surface = pygame.image.load(path).convert_alpha()
        tile_num_x = int(surface.get_size()[0] / tile_size)
        tile_num_y = int(surface.get_size()[1] / tile_size)

        cut_tiles = []
        for row in range(tile_num_y):
            for col in range(tile_num_x):
                x = col * tile_size
                y = row * tile_size
                new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
                cut_tiles.append(new_surf)

        return cut_tiles
    except Exception as e:
        print(f"Error loading graphics from {path}: {e}")
        return None

def import_folder(path):
    """Import all images from a folder."""
    surface_list = []
    try:
        for _, __, image_files in os.walk(path):
            for image in image_files:
                if image.endswith('.png'):
                    full_path = path + '/' + image
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)
        return surface_list
    except Exception as e:
        print(f"Error loading folder {path}: {e}")
        return []

def import_player_folder(path):
    surface_list = []

    for _,__,image_files in os.walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, player_sprite_size)
            surface_list.append(image_surf)
    
    return surface_list
            

def importCsvLayout(path):
    """Import CSV layout file and return as 2D list"""
    terrain_map = []
    
    if not os.path.exists(path):
        print(f"Warning: CSV file not found: {path}")
        return [['0' for _ in range(60)] for _ in range(11)]
    
    try:
        with open(path, 'r') as map_file:
            level = reader(map_file, delimiter=',')
            for row in level:
                if row:
                    terrain_map.append(list(row))
        
        # Ensure correct dimensions
        while len(terrain_map) < 11:
            terrain_map.append(['0'] * 60)
        
        for row in terrain_map:
            while len(row) < 60:
                row.append('0')
                
        return terrain_map
        
    except Exception as e:
        print(f"Error reading CSV file {path}: {e}")
        return [['0' for _ in range(60)] for _ in range(11)]


