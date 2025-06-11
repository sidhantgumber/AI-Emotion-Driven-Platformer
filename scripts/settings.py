# Game Settings
# Basic configuration for the platformer

# Grid settings
vertical_tile_number = 11
tile_size = 64
screen_height = vertical_tile_number * tile_size  # 704 pixels
screen_width = 1200

# Player settings
player_sprite_size = (64, 64)

# Game settings
dogCount = 4  # Number of dogs needed to win
FPS = 60

# Level dimensions
LEVEL_WIDTH = 60   # tiles
LEVEL_HEIGHT = 11  # tiles

# Tile type mappings (for visual identification)
TILE_TYPES = {
    0: 'air',
    1: 'platform_top_mid',
    2: 'platform_top_right',
    3: 'pillar_top',
    4: 'platform_left',
    5: 'ground_fill',
    6: 'platform_right',
    7: 'pillar_mid',
    8: 'pillar_bottom',
    12: 'floating_left',
    13: 'floating_mid',
    14: 'floating_right',
    15: 'single_block',
    16: 'dog_coin',
    17: 'cat_coin',
    27: 'player_spawn',
    28: 'goal'
}