#!/usr/bin/env python3
"""
Emotion-Based Level Viewer with Coin Collection & Win Conditions
================================================================
Main level viewing and rendering logic for the emotion-based platformer.
Now includes coin collection, scoring, and win conditions.
"""

import pygame
import os
from level_generator import EnhancedLevelGenerator
from support import importCsvLayout, import_cut_graphics, import_folder
from settings import tile_size, screen_width, screen_height, LEVEL_WIDTH, LEVEL_HEIGHT
from player import Player
from ml_agents import EmotionBrain
from tts import EdgeTTSNarrator
from ui_components import TextInputBox
from audio_manager import get_audio_manager

class EmotionLevelViewer:
    def __init__(self, level_number=0, levels_dir="generated_levels"):
        self.level_number = level_number
        self.levels_dir = levels_dir
        self.emotion = 'neutral'
        self.narrative = "Welcome! Enter your experience above to begin your emotional journey."
        self.camera_x = 0
        self.camera_y = 0
        
        # Game states
        self.state = 'input' 
        self.input_box = TextInputBox(
            x=screen_width//2 - 300,
            y=screen_height//2 - 50,
            width=600,
            height=50,
            prompt_text="Describe what happened in your day:"
        )
        
        self.level_width = LEVEL_WIDTH * tile_size
        self.level_height = LEVEL_HEIGHT * tile_size
        
        self.emotion_brain = EmotionBrain()
        self.narrator = EdgeTTSNarrator()
        
        self.load_real_assets()
        
        self.generate_emotion_level()
        
        print("Emotion Level Viewer initialized")
    
    def process_user_experience(self, user_text):
        """Process user's real-life experience and generate level."""
        print(f"Processing user experience: '{user_text}'")
        result = self.emotion_brain.process_user_input(user_text)
        
        self.emotion = result['emotion']
        self.narrative = result['narrative']
        
        print(f"Detected emotion: {self.emotion}")
        print(f"Generated narrative: {self.narrative}")
        
        print("Starting narrative generation...")
        self.narrator.speak_narrative(self.narrative, self.emotion)
        
        self.generate_emotion_level()
        
        audio = get_audio_manager()
        audio.play_background_music(self.emotion)

        self.state = 'playing'
        
        return result
    
    def generate_emotion_level(self):
        """Generate level based on current emotion."""
        try:
            generator = EnhancedLevelGenerator(self.emotion)
            level_data = generator.generate_enhanced_level()
            generator.save_level_to_files(level_data, 0, self.levels_dir)
            self.load_level()
            print(f"Generated {self.emotion} level successfully")
        except Exception as e:
            print(f"Error generating level: {e}")
    
    def load_emotion_sky(self):
        """Load emotion-specific sky background."""
        generator = EnhancedLevelGenerator(self.emotion)
        sky_surface = generator.load_emotion_sky()
        
        if sky_surface:
            self.assets['sky'] = sky_surface
            print(f"Loaded {self.emotion.upper()} sky")
            return True
        else:
            # Fallback to default sky
            fallback_sky = '../graphics/decoration/sky/sky.png'
            if os.path.exists(fallback_sky):
                sky_surface = pygame.image.load(fallback_sky).convert()
                self.assets['sky'] = pygame.transform.scale(sky_surface, (screen_width, screen_height))
            else:
                self.assets['sky'] = None
            print(f"{self.emotion.upper()} sky not found, using fallback")
            return False
    
    def load_real_assets(self):
        """Load game assets."""
        print("Loading game assets...")
        
        self.assets = {}
        
        # Terrain tiles
        terrain_path = '../graphics/terrain/terrain_tiles.png'
        if os.path.exists(terrain_path):
            self.assets['terrain'] = import_cut_graphics(terrain_path)
            print(f"Loaded terrain tiles: {len(self.assets['terrain'])} tiles")
        else:
            self.assets['terrain'] = None
        
        # Grass tiles  
        grass_path = '../graphics/decoration/grass/grass.png'
        if os.path.exists(grass_path):
            self.assets['grass'] = import_cut_graphics(grass_path)
            print(f"Loaded grass tiles: {len(self.assets['grass'])} tiles")
        else:
            self.assets['grass'] = None
        
        # Coin tiles
        coin_path = '../graphics/coins/coin_tiles.png'
        if os.path.exists(coin_path):
            self.assets['coins'] = import_cut_graphics(coin_path)
            print(f"Loaded coin tiles: {len(self.assets['coins'])} tiles")
        else:
            self.assets['coins'] = None
        
        # Palm trees
        self.assets['palms'] = {}
        
        small_palm_path = '../graphics/terrain/palm_small'
        if os.path.exists(small_palm_path):
            self.assets['palms']['small'] = import_folder(small_palm_path)
        
        large_palm_path = '../graphics/terrain/palm_large'
        if os.path.exists(large_palm_path):
            self.assets['palms']['large'] = import_folder(large_palm_path)
        
        bg_palm_path = '../graphics/terrain/palm_bg'
        if os.path.exists(bg_palm_path):
            self.assets['palms']['bg'] = import_folder(bg_palm_path)
        
        # Player/Goal assets
        self.assets['player_goal'] = {}
        
        player_idle_path = '../graphics/character/idle'
        if os.path.exists(player_idle_path):
            player_frames = import_folder(player_idle_path)
            if player_frames:
                self.assets['player_goal']['player'] = player_frames[0]
        
        hat_path = '../graphics/character/hat.png'
        if os.path.exists(hat_path):
            self.assets['player_goal']['goal'] = pygame.image.load(hat_path).convert_alpha()
        
        # Load sky for current emotion
        self.load_emotion_sky()
    
    def load_level(self):
        """Load level CSV data."""
        level_dir = os.path.join(self.levels_dir, str(self.level_number))
        
        self.terrain_layout = importCsvLayout(os.path.join(level_dir, f"level_{self.level_number}_terrain.csv"))
        self.coins_layout = importCsvLayout(os.path.join(level_dir, f"level_{self.level_number}_coins.csv"))
        self.player_layout = importCsvLayout(os.path.join(level_dir, f"level_{self.level_number}_player.csv"))
        self.fg_palms_layout = importCsvLayout(os.path.join(level_dir, f"level_{self.level_number}_fg_palms.csv"))
        self.bg_palms_layout = importCsvLayout(os.path.join(level_dir, f"level_{self.level_number}_bg_palms.csv"))
        self.grass_layout = importCsvLayout(os.path.join(level_dir, f"level_{self.level_number}_grass.csv"))
        
        self.spawn_player()
        self.load_emotion_sky()  
        
        print("Level data loaded")

    def spawn_player(self):
        """Spawn player at designated position with emotion-based physics."""
        for row_idx, row in enumerate(self.player_layout):
            for col_idx, cell in enumerate(row):
                if cell == '27':
                    x = col_idx * tile_size
                    y = row_idx * tile_size
                    self.player = Player((x, y), self.emotion)  
                    self.player.reset_game_state()  
                    return
        # Fallback spawn position if no spawn tile found
        self.player = Player((tile_size, tile_size), self.emotion)  
        self.player.reset_game_state()

    def check_coin_collisions(self):
        """Check for coin collection."""
        if not hasattr(self, 'player') or self.player.is_dead or self.player.has_won:
            return
            
        player_tile_x = self.player.rect.centerx // tile_size
        player_tile_y = self.player.rect.centery // tile_size
        
        # Check if player is on a coin tile
        if (0 <= player_tile_y < len(self.coins_layout) and 
            0 <= player_tile_x < len(self.coins_layout[player_tile_y])):
            
            if self.coins_layout[player_tile_y][player_tile_x] == '16':
                # Collect the coin
                self.coins_layout[player_tile_y][player_tile_x] = '0'
                self.player.collect_coin()

    def check_goal_collision(self):
        """Check if player reached the goal."""
        if not hasattr(self, 'player') or self.player.is_dead or self.player.has_won:
            return
            
        player_tile_x = self.player.rect.centerx // tile_size
        player_tile_y = self.player.rect.centery // tile_size
        
        # Check if player is on goal tile
        if (0 <= player_tile_y < len(self.player_layout) and 
            0 <= player_tile_x < len(self.player_layout[player_tile_y])):
            
            if self.player_layout[player_tile_y][player_tile_x] == '28':
                self.player.reached_goal = True
                if self.player.check_win_condition():
                    print("Level completed!")
    
    def get_sprite_for_tile(self, layer_type, tile_value):
        """Get sprite for a tile."""
        if str(tile_value) == '0':
            return None
        
        try:
            tile_val = int(tile_value)
            
            if layer_type == 'terrain':
                if self.assets['terrain'] and tile_val < len(self.assets['terrain']):
                    return self.assets['terrain'][tile_val]
            
            elif layer_type == 'grass':
                if self.assets['grass'] and tile_val < len(self.assets['grass']):
                    return self.assets['grass'][tile_val]
            
            elif layer_type == 'coins':
                if self.assets['coins']:
                    return self.assets['coins'][0] if self.assets['coins'] else None
            
            elif layer_type == 'fg_palms':
                if tile_val == 23:
                    if self.assets['palms'].get('small'):
                        return self.assets['palms']['small'][0]
                elif tile_val == 24:
                    if self.assets['palms'].get('large'):
                        return self.assets['palms']['large'][0]
            
            elif layer_type == 'bg_palms':
                if tile_val == 25:
                    if self.assets['palms'].get('bg'):
                        return self.assets['palms']['bg'][0]
            
            elif layer_type == 'player':
                if tile_val == 28:
                    return self.assets['player_goal'].get('goal')
        
        except (ValueError, IndexError, KeyError):
            pass
        
        return None
    
    def draw_layer_with_real_sprites(self, surface, layout, layer_type):
        """Draw layer using real sprites."""
        start_x = max(0, int(self.camera_x // tile_size))
        end_x = min(LEVEL_WIDTH, int((self.camera_x + screen_width) // tile_size + 1))
        start_y = max(0, int(self.camera_y // tile_size))
        end_y = min(LEVEL_HEIGHT, int((self.camera_y + screen_height) // tile_size + 1))
        
        for row in range(start_y, end_y):
            for col in range(start_x, end_x):
                if row < len(layout) and col < len(layout[row]):
                    tile_value = layout[row][col]
                    sprite = self.get_sprite_for_tile(layer_type, tile_value)
                    
                    if sprite:
                        screen_x = (col * tile_size) - self.camera_x
                        screen_y = (row * tile_size) - self.camera_y
                        surface.blit(sprite, (screen_x, screen_y))
    
    def get_emotion_fallback_colors(self):
        """Get fallback gradient colors for each emotion."""
        generator = EnhancedLevelGenerator(self.emotion)
        return generator.get_emotion_fallback_colors()
    
    def draw_background(self, surface):
        """Draw emotion-specific background."""
        if self.assets['sky']:
            surface.blit(self.assets['sky'], (0, 0))
        else:
            colors = self.get_emotion_fallback_colors()
            for y in range(screen_height):
                ratio = y / screen_height
                r = int(colors['top'][0] + (colors['bottom'][0] - colors['top'][0]) * ratio)
                g = int(colors['top'][1] + (colors['bottom'][1] - colors['top'][1]) * ratio)
                b = int(colors['top'][2] + (colors['bottom'][2] - colors['top'][2]) * ratio)
                
                color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
                pygame.draw.line(surface, color, (0, y), (screen_width, y))
    
    def update_camera(self, keys):
        """Update camera position."""
        if self.state != 'playing':
            return
            
        if hasattr(self, 'player'):
            target_x = self.player.rect.centerx - screen_width // 2
            target_y = self.player.rect.centery - screen_height // 2
            
            camera_speed = 0.1
            self.camera_x += (target_x - self.camera_x) * camera_speed
            self.camera_y += (target_y - self.camera_y) * camera_speed
            
            self.camera_x = max(0, min(self.level_width - screen_width, self.camera_x))
            self.camera_y = max(0, min(self.level_height - screen_height, self.camera_y))
        
        manual_speed = 8
        if keys[pygame.K_LEFT]:
            self.camera_x = max(0, self.camera_x - manual_speed)
        if keys[pygame.K_RIGHT]:
            self.camera_x = min(self.level_width - screen_width, self.camera_x + manual_speed)
        if keys[pygame.K_UP]:
            self.camera_y = max(0, self.camera_y - manual_speed)
        if keys[pygame.K_DOWN]:
            self.camera_y = min(self.level_height - screen_height, self.camera_y + manual_speed)
    
    def draw_input_screen(self, surface):
        """Draw the input screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Title
        title_font = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 72)
        title_text = title_font.render("Emotion Based Platformer", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width//2, screen_height//2 - 150))
        surface.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 30)
        subtitle_text = subtitle_font.render("How are you feeling today?", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(screen_width//2, screen_height//2 - 100))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Input box
        self.input_box.draw(surface)
        
        # Instructions
        instruction_font = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 20)
        instructions = [
            "Objective: Collect 5 coins and reach the pirate hat to win!",
            "Press ENTER to generate your emotional journey",
            "Examples: 'I got promoted!', 'Traffic was terrible', 'I'm nervous about tomorrow'"
        ]
        
        for i, instruction in enumerate(instructions):
            text = instruction_font.render(instruction, True, (150, 150, 150))
            text_rect = text.get_rect(center=(screen_width//2, screen_height//2 + 80 + i * 30))
            surface.blit(text, text_rect)
    
    def draw_playing_ui(self, surface):
        """Draw UI elements during gameplay."""
        font = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 36)
        title_text = font.render(f"EMOTION LEVEL - {self.emotion.upper()}", True, (255, 255, 255))
        surface.blit(title_text, (10, 10))
        
        # Score display
        score_font = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 48)
        if hasattr(self, 'player'):
            score_text = score_font.render(f"COINS: {self.player.score}/{self.player.coins_needed}", True, (255, 215, 0))
            surface.blit(score_text, (10, 50))
            
            # Goal status
            goal_font = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 32)
            if self.player.reached_goal:
                goal_text = goal_font.render("GOAL REACHED!", True, (0, 255, 0))
                surface.blit(goal_text, (10, 100))
            
            # Win condition status
            if self.player.score >= self.player.coins_needed and not self.player.reached_goal:
                win_text = goal_font.render("Find the pirate hat to win!", True, (255, 255, 0))
                surface.blit(win_text, (10, 130))
        
        font_small = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 24)
        controls = [
            "WASD/Arrow Keys: Move Player",
            "SPACE/W/UP: Jump",
            "R: New Experience",
            "S: Skip/Stop Narration",
            "ESC: Quit"
        ]
        
        # Show narration status
        if self.narrator.is_speaking():
            controls.insert(2, "Status: Playing narration...")
        elif hasattr(self.narrator, 'is_generating') and self.narrator.is_generating:
            controls.insert(2, "Status: Generating speech...")
        
        for i, control in enumerate(controls):
            text = font_small.render(control, True, (255, 255, 255))
            surface.blit(text, (10, screen_height - 155 + i * 22))
    
    def draw(self, surface):
        """Draw the complete game scene."""
        self.draw_background(surface)
        
        if self.state == 'input':
            self.draw_input_screen(surface)
        else:  # playing state
            self.draw_layer_with_real_sprites(surface, self.bg_palms_layout, 'bg_palms')
            self.draw_layer_with_real_sprites(surface, self.terrain_layout, 'terrain')
            self.draw_layer_with_real_sprites(surface, self.grass_layout, 'grass')
            self.draw_layer_with_real_sprites(surface, self.coins_layout, 'coins')
            self.draw_layer_with_real_sprites(surface, self.fg_palms_layout, 'fg_palms')

            # Player
            if hasattr(self, "player"):
                self.player.update(self.terrain_layout)
                if not self.player.is_dead:
                    player_screen_x = self.player.rect.x - self.camera_x
                    player_screen_y = self.player.rect.y - self.camera_y
                    surface.blit(self.player.image, (player_screen_x, player_screen_y))

            self.draw_layer_with_real_sprites(surface, self.player_layout, 'player')
            self.draw_playing_ui(surface)
            
            # Death screen
            if hasattr(self, "player") and self.player.is_dead:
                self.player.draw_death_screen(surface, self.camera_x, self.camera_y)
            
            # Win screen
            if hasattr(self, "player") and self.player.has_won:
                self.player.draw_win_screen(surface, self.camera_x, self.camera_y)
    
    def handle_event(self, event):
        """Handle game events."""
        if self.state == 'input':
            # Handle text input
            result = self.input_box.handle_event(event)
            if result:  # User pressed Enter
                if result.strip():  # Don't process empty input
                    self.process_user_experience(result.strip())
                    self.input_box.clear()
        
        elif self.state == 'playing':
            # Handle gameplay events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    audio = get_audio_manager()
                    if hasattr(self, 'player') and (self.player.is_dead or self.player.has_won):
                        if self.player.has_won:
                            # Go back to input for new experience
                            if self.narrator.is_speaking():
                                self.narrator.stop_speaking()
                            audio.stop_background_music()
                            self.state = 'input'
                            print("Switched to input mode for new experience")
                        else:
                            # Reload level to reset coins and respawn player
                            self.load_level()
                            audio.play_background_music(self.emotion)

                            print("Level reloaded and player respawned")
                    else:
                        # Stop current narration and go back to input
                        if self.narrator.is_speaking():
                            self.narrator.stop_speaking()
                        self.state = 'input'
                        print("Switched to input mode")
                elif event.key == pygame.K_s:
                    # Skip/stop narration
                    if self.narrator.is_speaking():
                        self.narrator.stop_speaking()
                        print("Narration stopped")
    
    def update(self, dt):
        """Update game state."""
        if self.state == 'input':
            self.input_box.update(dt)
        elif self.state == 'playing':
            # Check game interactions
            self.check_coin_collisions()
            self.check_goal_collision()
