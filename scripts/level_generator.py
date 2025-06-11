#!/usr/bin/env python3
"""
Enhanced Procedural Level Generator - Day 2 FIXED
=================================================
Fixed tree placement, simplified collectibles, and improved grass coverage
to match the target game screenshots.
"""

import random
import os
import sys
import pygame
from typing import List
from settings import screen_width, screen_height

class EnhancedLevelGenerator:
    def __init__(self, emotion='neutral'):
        self.width = 60
        self.height = 11
        self.emotion = emotion.lower()
        self.first_platform_x = None  # Track first platform position
        self.terrain_tiles = {
            'platform_top_left': 0,
            'platform_top_mid': 1, 
            'platform_top_right': 2,
            'pillar_top': 3,
            'platform_left': 4,
            'ground_fill': 5,
            'platform_right': 6,
            'pillar_mid': 7,
            'pillar_bottom': 8,
            'floating_left': 12,
            'floating_mid': 13,
            'floating_right': 14,
            'single_block': 15
        }
        self._set_emotion_parameters(self.emotion)

    def _set_emotion_parameters(self, emotion):
        # Set everything per mood!
        if emotion == 'joy':
            self.platform_min_length = 6
            self.platform_max_length = 12
            self.gap_min_size = 3
            self.gap_max_size = 5
            self.floating_platform_chance = 0.55
            self.fg_tree_chance = 0.22
            self.bg_tree_chance = 0.33
            self.grass_chance = 0.95
            self.coin_chance = 0.6
        elif emotion == 'fear':
            self.platform_min_length = 2      # Very small platforms (single blocks)
            self.platform_max_length = 3      # Maximum 2-tile platforms (still very small)
            self.gap_min_size = 1             # Minimal gaps (just 1 tile)
            self.gap_max_size =  2            # Small gaps (maximum 2 tiles)
            self.floating_platform_chance = 0.1  # Very few floating platforms (focus on ground)
            self.fg_tree_chance = 0.08
            self.bg_tree_chance = 0.17
            self.grass_chance = 0.55
            self.coin_chance = 0.3
        elif emotion == 'anger':
            self.platform_min_length = 1
            self.platform_max_length = 8
            self.gap_min_size = 3
            self.gap_max_size = 7
            self.floating_platform_chance = 0.77
            self.fg_tree_chance = 0.09
            self.bg_tree_chance = 0.15
            self.grass_chance = 0.45
            self.coin_chance = 0.15
        else:  # neutral/default
            self.platform_min_length = 4
            self.platform_max_length = 10
            self.gap_min_size = 2
            self.gap_max_size = 4
            self.floating_platform_chance = 0.4
            self.fg_tree_chance = 0.15
            self.bg_tree_chance = 0.25
            self.grass_chance = 0.85
            self.coin_chance = 0.3
        self.ground_level = 8
        
    def generate_enhanced_level(self) -> dict:
        print(f"Generating enhanced level for mood: **{self.emotion.upper()}** ...")
        terrain_grid = self._create_empty_grid()
        self._generate_ground_platforms(terrain_grid)
        self._generate_strategic_floating_platforms(terrain_grid)
        grass_grid = self._generate_proper_grass(terrain_grid)
        bg_palms_grid = self._generate_proper_background_trees(terrain_grid)
        fg_palms_grid = self._generate_proper_foreground_trees(terrain_grid)
        coins_grid = self._generate_simple_coins(terrain_grid, fg_palms_grid, grass_grid)
        player_grid = self._generate_player_layer(terrain_grid)  # Pass terrain to find safe spawn
        return {
            'terrain': self._grid_to_csv(terrain_grid),
            'coins': self._grid_to_csv(coins_grid),
            'player': self._grid_to_csv(player_grid),
            'fg_palms': self._grid_to_csv(fg_palms_grid),
            'bg_palms': self._grid_to_csv(bg_palms_grid),
            'grass': self._grid_to_csv(grass_grid),
            'crates': self._generate_empty_layer(),
            'enemies': self._generate_empty_layer(),
            'constraints': self._generate_empty_layer()
        }
    
    def _create_empty_grid(self) -> List[List[int]]:
        """Create an empty grid filled with 0s"""
        return [[0 for _ in range(self.width)] for _ in range(self.height)]
    
    def _generate_ground_platforms(self, grid: List[List[int]]):
        """Generate the main ground level with platforms and gaps"""
        x = 0
        first_platform_created = False
        
        while x < self.width:
            platform_length = random.randint(self.platform_min_length, self.platform_max_length)
            platform_length = min(platform_length, self.width - x)
            
            # Always create the first platform at the start for player spawn
            if not first_platform_created and x < 5:
                platform_length = max(platform_length, 3)  # Ensure first platform is at least 3 tiles
                self.first_platform_x = x  # Track first platform position
                first_platform_created = True
            
            if platform_length >= 1:  # Allow single blocks for fear emotion
                self._create_platform(grid, x, self.ground_level, platform_length)
                x += platform_length
                
                if x < self.width - 5:
                    gap_size = random.randint(self.gap_min_size, self.gap_max_size)
                    gap_size = min(gap_size, self.width - x - 5)
                    x += gap_size
            else:
                x += 1
        
        # Ensure level ends with solid ground
        if x >= self.width - 5:
            for end_x in range(max(0, self.width - 5), self.width):
                self._create_single_column(grid, end_x, self.ground_level)
    
    def _generate_strategic_floating_platforms(self, grid: List[List[int]]):
        """Generate floating platforms with strategic placement"""
        platform_rows = [4, 5, 6, 7]
        
        for row in platform_rows:
            x = random.randint(8, 12)
            
            while x < self.width - 10:
                if random.random() < self.floating_platform_chance:
                    if row <= 5:
                        platform_size = random.randint(2, 4)
                    else:
                        platform_size = random.randint(3, 6)
                    
                    if x + platform_size < self.width - 5:
                        if self._can_place_platform(grid, x, row, platform_size):
                            self._create_floating_platform(grid, x, row, platform_size)
                
                x += random.randint(6, 12)
        
        self._add_challenging_single_blocks(grid)
    
    def _can_place_platform(self, grid: List[List[int]], x: int, y: int, length: int) -> bool:
        """Check if we can place a platform without overlapping"""
        for check_x in range(max(0, x-1), min(self.width, x + length + 1)):
            for check_y in range(max(0, y-1), min(self.height, y + 2)):
                if grid[check_y][check_x] != 0:
                    return False
        return True
    
    def _add_challenging_single_blocks(self, grid: List[List[int]]):
        """Add single floating blocks for advanced platforming"""
        for _ in range(random.randint(2, 4)):
            x = random.randint(10, self.width - 10)
            y = random.randint(4, 6)
            
            if (self._is_area_clear(grid, x, y, 1, 1) and
                self._has_nearby_platform(grid, x, y)):
                grid[y][x] = self.terrain_tiles['single_block']
    
    def _is_area_clear(self, grid: List[List[int]], x: int, y: int, width: int, height: int) -> bool:
        """Check if an area is clear of terrain"""
        for check_y in range(y, min(self.height, y + height)):
            for check_x in range(x, min(self.width, x + width)):
                if grid[check_y][check_x] != 0:
                    return False
        return True
    
    def _has_nearby_platform(self, grid: List[List[int]], x: int, y: int) -> bool:
        """Check if there's a platform within jumping distance"""
        search_range = 5
        for check_x in range(max(0, x - search_range), min(self.width, x + search_range)):
            for check_y in range(max(0, y - 1), min(self.height, y + 3)):
                if grid[check_y][check_x] != 0:
                    return True
        return False
    
    def _generate_proper_grass(self, terrain_grid: List[List[int]]) -> List[List[int]]:
        """
        FIXED: Generate grass decorations properly on top of ALL platform surfaces
        """
        grass_grid = self._create_empty_grid()
        
        # Place grass on TOP of solid terrain (directly above solid blocks)
        for row in range(self.height - 1):
            for col in range(self.width):
                # Check if there's solid terrain below AND air at current position
                if (terrain_grid[row + 1][col] != 0 and      # Solid terrain below
                    terrain_grid[row][col] == 0 and          # Air at current position
                    random.random() < self.grass_chance):    # High probability
                    
                    # Use different grass tile types for variety
                    grass_types = [19, 20, 21, 22, 23]
                    grass_grid[row][col] = random.choice(grass_types)
        
        return grass_grid
    
    def _generate_proper_background_trees(self, terrain_grid: List[List[int]]) -> List[List[int]]:
        """
        Place bg palms **only** on the ground or on top of platforms, and in small clusters.
        """
        bg_tree_grid = self._create_empty_grid()
        for col in range(0, self.width, 2):
            for row in range(self.height - 2, 2, -1):  # Scan from bottom up
                # Place a bg palm if this is air and the tile below is solid (i.e., surface)
                if terrain_grid[row][col] == 0 and terrain_grid[row + 1][col] != 0:
                    if random.random() < self.bg_tree_chance:
                        cluster_size = random.choice([1, 2])  # Cluster of 1 or 2
                        for offset in range(cluster_size):
                            c = col + offset
                            if c < self.width and bg_tree_grid[row][c] == 0:
                                bg_tree_grid[row][c] = 25  # 25 = bg palm
                    break  # Don't place more in this column (surface only)
        return bg_tree_grid

    
    def _generate_proper_foreground_trees(self, terrain_grid: List[List[int]]) -> List[List[int]]:
        """
        FIXED: Generate foreground trees ONLY on solid ground, never floating
        """
        fg_tree_grid = self._create_empty_grid()
        
        # Method 1: Place trees ON TOP of existing terrain (where grass would go)
        for row in range(self.height - 1):
            for col in range(self.width):
                # Only place trees where there's solid ground below
                if (terrain_grid[row + 1][col] != 0 and      # Solid terrain below
                    terrain_grid[row][col] == 0 and          # Air at current position
                    random.random() < self.fg_tree_chance):  # Lower chance for trees
                    
                    # Use small foreground palm trees
                    fg_tree_grid[row][col] = 23  # Small foreground palm
        
        # Method 2: Add a few trees specifically on floating platforms
        for row in range(3, 8):  # Floating platform area
            for col in range(self.width):
                # Check if this is a floating platform surface
                if (terrain_grid[row][col] != 0 and          # This IS solid terrain
                    row > 0 and                              # Not top row
                    terrain_grid[row - 1][col] == 0 and      # Air above platform
                    fg_tree_grid[row - 1][col] == 0 and      # No tree already placed
                    random.random() < 0.2):                  # 20% chance on platforms
                    
                    # Place tree on top of the platform
                    fg_tree_grid[row - 1][col] = 23  # Small foreground palm
        
        return fg_tree_grid
    
    def _generate_simple_coins(self, terrain_grid: List[List[int]], 
                              fg_palms_grid: List[List[int]],
                              grass_grid: List[List[int]]) -> List[List[int]]:
        """
        FIXED: Generate simple collectibles (just one type, no cats/dogs)
        """
        coins_grid = self._create_empty_grid()
        
        # Place coins above solid terrain, avoiding trees and grass conflicts
        for row in range(self.height - 1):
            for col in range(self.width):
                # Place coins above solid terrain
                if (terrain_grid[row + 1][col] != 0 and      # Solid below
                    terrain_grid[row][col] == 0 and          # Air at this position
                    fg_palms_grid[row][col] == 0 and         # No foreground tree here
                    random.random() < self.coin_chance):     # Coin chance
                    
                    # FIXED: Just one type of collectible
                    coins_grid[row][col] = 16  # Simple collectible
        
        # Add some challenge coins in mid-air between platforms
        self._add_challenge_coins(coins_grid, terrain_grid, fg_palms_grid)
        
        return coins_grid
    
    def _add_challenge_coins(self, coins_grid: List[List[int]], 
                           terrain_grid: List[List[int]], 
                           fg_palms_grid: List[List[int]]):
        """Add coins in challenging locations for skilled players"""
        for row in range(2, 6):  # High up in the air
            for col in range(5, self.width - 5):
                # Add coins in mid-air between platforms (risky to collect)
                if (terrain_grid[row][col] == 0 and         # Air
                    fg_palms_grid[row][col] == 0 and        # No tree
                    coins_grid[row][col] == 0 and           # No coin already
                    self._is_between_platforms(terrain_grid, col, row) and
                    random.random() < 0.08):                # 8% chance for challenge coins
                    
                    coins_grid[row][col] = 16  # Simple collectible
    
    def _is_between_platforms(self, terrain_grid: List[List[int]], x: int, y: int) -> bool:
        """Check if position is between two platforms"""
        left_platform = False
        right_platform = False
        
        # Look for platforms to the left and right
        for check_x in range(max(0, x - 6), x):
            if terrain_grid[y + 1][check_x] != 0 or terrain_grid[y + 2][check_x] != 0:
                left_platform = True
                break
        
        for check_x in range(x + 1, min(self.width, x + 6)):
            if terrain_grid[y + 1][check_x] != 0 or terrain_grid[y + 2][check_x] != 0:
                right_platform = True
                break
        
        return left_platform and right_platform
    
    def _generate_player_layer(self, terrain_grid: List[List[int]]) -> List[List[int]]:
        """Generate player spawn and goal positions - spawn on first platform"""
        grid = self._create_empty_grid()
        
        # Find the first solid platform to spawn player on
        spawn_x = 1  # Default fallback
        spawn_y = self.ground_level - 1  # One tile above ground level
        
        # Look for the first solid platform starting from the left
        for col in range(self.width):
            if terrain_grid[self.ground_level][col] != 0:  # Found solid ground
                spawn_x = col
                spawn_y = self.ground_level - 1  # Spawn above the platform
                break
        
        # Ensure spawn position is safe (not at the very edge)
        spawn_x = max(1, min(spawn_x, self.width - 2))
        
        grid[spawn_y][spawn_x] = 27  # Player spawn on first platform
        grid[5][self.width - 3] = 28  # Goal
        
        print(f"Player spawned at position ({spawn_x}, {spawn_y}) on first platform")
        return grid
    
    def _create_platform(self, grid: List[List[int]], start_x: int, start_y: int, length: int):
        """Create a platform with proper tile types"""
        if length < 1:
            return
            
        if length == 1:
            grid[start_y][start_x] = self.terrain_tiles['single_block']
        elif length == 2:
            grid[start_y][start_x] = self.terrain_tiles['platform_top_left']
            grid[start_y][start_x + 1] = self.terrain_tiles['platform_top_right']
        else:
            grid[start_y][start_x] = self.terrain_tiles['platform_top_left']
            for i in range(1, length - 1):
                grid[start_y][start_x + i] = self.terrain_tiles['platform_top_mid']
            grid[start_y][start_x + length - 1] = self.terrain_tiles['platform_top_right']
        
        # Fill below with ground
        for y in range(start_y + 1, self.height):
            if length == 1:
                if y == self.height - 1:
                    grid[y][start_x] = self.terrain_tiles['pillar_bottom']
                else:
                    grid[y][start_x] = self.terrain_tiles['pillar_mid']
            elif length == 2:
                grid[y][start_x] = self.terrain_tiles['platform_left']
                grid[y][start_x + 1] = self.terrain_tiles['platform_right']
            else:
                grid[y][start_x] = self.terrain_tiles['platform_left']
                for i in range(1, length - 1):
                    grid[y][start_x + i] = self.terrain_tiles['ground_fill']
                grid[y][start_x + length - 1] = self.terrain_tiles['platform_right']
    
    def _create_single_column(self, grid: List[List[int]], x: int, start_y: int):
        """Create a single column of terrain"""
        for y in range(start_y, self.height):
            if y == start_y:
                grid[y][x] = self.terrain_tiles['platform_top_mid']
            else:
                grid[y][x] = self.terrain_tiles['ground_fill']
    
    def _create_floating_platform(self, grid: List[List[int]], start_x: int, y: int, length: int):
        """Create a floating platform"""
        if length == 1:
            grid[y][start_x] = self.terrain_tiles['single_block']
        elif length == 2:
            grid[y][start_x] = self.terrain_tiles['floating_left']
            grid[y][start_x + 1] = self.terrain_tiles['floating_right']
        else:
            grid[y][start_x] = self.terrain_tiles['floating_left']
            for i in range(1, length - 1):
                grid[y][start_x + i] = self.terrain_tiles['floating_mid']
            grid[y][start_x + length - 1] = self.terrain_tiles['floating_right']
    
    def _grid_to_csv(self, grid: List[List[int]]) -> str:
        """Convert grid to CSV string"""
        csv_lines = []
        for row in grid:
            csv_lines.append(','.join(str(cell) for cell in row))
        return '\n'.join(csv_lines) + '\n'
    
    def _generate_empty_layer(self) -> str:
        """Generate an empty layer"""
        grid = self._create_empty_grid()
        return self._grid_to_csv(grid)
    
    def load_emotion_sky(self):
        """Load emotion-specific sky background."""
        sky_files = {
            'joy': '../graphics/decoration/sky/sky_joy.png',
            'fear': '../graphics/decoration/sky/sky_fear.png', 
            'anger': '../graphics/decoration/sky/sky_anger.png',
            'neutral': '../graphics/decoration/sky/sky_neutral.png'
        }
        
        sky_path = sky_files.get(self.emotion, sky_files['neutral'])
        
        if os.path.exists(sky_path):
            sky_surface = pygame.image.load(sky_path).convert()
            scaled_sky = pygame.transform.scale(sky_surface, (screen_width, screen_height))
            print(f"Loaded {self.emotion.upper()} sky")
            return scaled_sky
        else:
            print(f"{self.emotion.upper()} sky not found")
            return None
    
    def get_emotion_fallback_colors(self):
        """Get fallback gradient colors for each emotion."""
        emotion_colors = {
            'joy': {'top': (255, 223, 0), 'bottom': (135, 206, 250)},
            'fear': {'top': (25, 25, 112), 'bottom': (0, 0, 0)},
            'anger': {'top': (220, 20, 60), 'bottom': (139, 0, 0)},
            'neutral': {'top': (135, 206, 235), 'bottom': (135, 206, 235)}
        }
        return emotion_colors.get(self.emotion, emotion_colors['neutral'])

    def save_level_to_files(self, level_data: dict, level_number: int, output_dir: str = "levels"):
        level_dir = os.path.join(output_dir, str(level_number))
        os.makedirs(level_dir, exist_ok=True)
        file_mapping = {
            'terrain': f'level_{level_number}_terrain.csv',
            'coins': f'level_{level_number}_coins.csv',
            'player': f'level_{level_number}_player.csv',
            'fg_palms': f'level_{level_number}_fg_palms.csv',
            'bg_palms': f'level_{level_number}_bg_palms.csv',
            'grass': f'level_{level_number}_grass.csv',
            'crates': f'level_{level_number}_crates.csv',
            'enemies': f'level_{level_number}_enemies.csv',
            'constraints': f'level_{level_number}_constraints.csv'
        }
        for layer_name, filename in file_mapping.items():
            filepath = os.path.join(level_dir, filename)
            with open(filepath, 'w') as f:
                f.write(level_data[layer_name])
        print(f"Level {level_number} for mood '{self.emotion}' saved to {level_dir}/")
        return level_dir


def main():
    print("Enhanced Level Generator - Now With Emotions!")
    print("=" * 45)
    emotion = sys.argv[1] if len(sys.argv) > 1 else 'neutral'
    print(f"Selected mood: {emotion.upper()}")
    generator = EnhancedLevelGenerator(emotion)
    level_data = generator.generate_enhanced_level()
    output_dir = generator.save_level_to_files(level_data, 0, "generated_levels")
    print("\nGeneration complete!")
    print(f"Files saved to: {output_dir}")
    print("\nTry: python level_generator.py joy / fear / anger / neutral")


if __name__ == "__main__":
    main()