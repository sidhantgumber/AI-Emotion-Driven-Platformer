import pygame
from support import import_player_folder
from settings import tile_size, screen_height, LEVEL_HEIGHT
from audio_manager import get_audio_manager

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, emotion='neutral'):
        super().__init__()
        self.emotion = emotion.lower()
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'idle'
        self.facing_right = True
        self.audio = get_audio_manager()
        self.is_dead = False
        self.death_y_threshold = LEVEL_HEIGHT * tile_size + 100  # Below level + buffer
        self.spawn_position = pos  

        # Game state
        self.score = 0
        self.coins_needed = 5
        self.has_won = False
        self.reached_goal = False

        # Set image and rect
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        # Physics - set based on emotion
        self.direction = pygame.math.Vector2(0, 0)
        self.set_emotion_physics(self.emotion)
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def set_emotion_physics(self, emotion):
        """Set physics parameters based on detected emotion."""
        if emotion == 'joy':
            # Joy: Light, bouncy, energetic movement
            self.speed = 6           
            self.gravity = 0.4       
            self.jump_speed = -16    
            self.max_fall_speed = 8 
            self.animation_speed = 0.2  
            print(f"Player tuned for JOY: Fast & bouncy movement")
        
        elif emotion == 'fear':
            # Fear: Sluggish, heavy, cautious movement
            self.speed = 4           
            self.gravity = 1.3       
            self.jump_speed = -20    
            self.max_fall_speed = 18 
            self.animation_speed = 0.1  
            print(f"Player tuned for FEAR: Sluggish & heavy movement")
        
        elif emotion == 'anger':
            # Anger: Aggressive, sharp, intense movement
            self.speed = 9           
            self.gravity = 1.3       
            self.jump_speed = -28    
            self.max_fall_speed = 20 
            self.animation_speed = 0.25 # Very fast animation
            print(f"Player tuned for ANGER: Aggressive & intense movement")
        
        else:  
            # Neutral: Balanced, standard movement
            self.speed = 5          
            self.gravity = .9      
            self.jump_speed = -20    
            self.max_fall_speed = 18 
            self.animation_speed = 0.15 
            print(f"Player tuned for NEUTRAL: Balanced movement")

    def import_assets(self):
        character_path = '../graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            self.animations[animation] = import_player_folder(character_path + animation)

    def collect_coin(self):
        """Collect a coin and update score."""
        self.score += 1
        self.audio.play_coin_collect()  # Play coin sound
        print(f"Coin collected! Score: {self.score}/{self.coins_needed}")

    def check_win_condition(self):
        """Check if player has met win conditions."""
        if self.score >= self.coins_needed and self.reached_goal and not self.has_won:
            self.has_won = True
            self.audio.play_game_win()  # Play victory sound
            print("Congratulations! You won!")
            return True
        return False

    def reset_game_state(self):
        """Reset game state for new level."""
        self.score = 0
        self.has_won = False
        self.reached_goal = False

    def input(self):
        # Don't process input if dead or won
        if self.is_dead or self.has_won:
            return
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.jump()

    def check_death(self):
        """Check if player has fallen below the death threshold"""
        if self.rect.y > self.death_y_threshold and not self.is_dead:
            self.die()

    def die(self):
        """Handle player death"""
        self.is_dead = True
        self.direction.x = 0
        self.direction.y = 0
        self.audio.play_game_over()  # Play death sound
        print("Player died! Press R to restart.")

    def respawn(self):
        """Respawn player at spawn position"""
        self.is_dead = False
        self.has_won = False
        self.reached_goal = False
        self.rect.topleft = self.spawn_position
        self.direction = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        print("Player respawned!")

    def draw_death_screen(self, surface, camera_x=0, camera_y=0):
        """Draw death message overlay"""
        if not self.is_dead:
            return
            
        # Create semi-transparent overlay
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Draw death message
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        # Main death message
        death_text = font_large.render("YOU DIED", True, (255, 50, 50))
        death_rect = death_text.get_rect(center=(surface.get_width()//2, surface.get_height()//2 - 40))
        surface.blit(death_text, death_rect)
        
        # Restart instruction
        restart_text = font_small.render("Press R to Restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(surface.get_width()//2, surface.get_height()//2 + 20))
        surface.blit(restart_text, restart_rect)

    def draw_win_screen(self, surface, camera_x=0, camera_y=0):
        """Draw win message overlay"""
        if not self.has_won:
            return
            
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(150)
        overlay.fill((0, 50, 0))  # Green tint for victory
        surface.blit(overlay, (0, 0))
        
        # Draw win message
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        # Main win message
        win_text = font_large.render("YOU WON!", True, (0, 255, 0))
        win_rect = win_text.get_rect(center=(surface.get_width()//2, surface.get_height()//2 - 60))
        surface.blit(win_text, win_rect)
        
        # Score display
        score_text = font_small.render(f"Final Score: {self.score} coins", True, (200, 255, 200))
        score_rect = score_text.get_rect(center=(surface.get_width()//2, surface.get_height()//2 - 10))
        surface.blit(score_text, score_rect)
        
        # Continue instruction
        continue_text = font_small.render("Press R for New Experience", True, (200, 255, 200))
        continue_rect = continue_text.get_rect(center=(surface.get_width()//2, surface.get_height()//2 + 40))
        surface.blit(continue_text, continue_rect)

    def get_status(self):
        # Don't change status if dead or won
        if self.is_dead or self.has_won:
            return
            
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def animate(self):
        # Don't animate if dead or won
        if self.is_dead or self.has_won:
            return
            
        animation = self.animations[self.status]
        if len(animation) > 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0

            image = animation[int(self.frame_index)]
            if not self.facing_right:
                image = pygame.transform.flip(image, True, False)
            self.image = image

    def apply_gravity(self):
        # Don't apply gravity if dead or won
        if self.is_dead or self.has_won:
            return
            
        self.direction.y += self.gravity
        if self.direction.y > self.max_fall_speed:
            self.direction.y = self.max_fall_speed

    def jump(self):
        if not self.is_dead and not self.has_won:
            self.direction.y = self.jump_speed
            self.audio.play_jump()  # Play jump sound

    def is_solid_tile(self, tile_value):
        """Check if a tile is solid (can be stood on/collided with)"""
        solid_tiles = {
            '1', '2', '3', '4', '5', '6', '7', '8',  # Basic terrain
            '12', '13', '14', '15'  # Floating platforms and single blocks
        }
        return str(tile_value) in solid_tiles

    def horizontal_movement_collision(self, terrain_layout):
        """Handle horizontal collision detection"""
        if self.is_dead or self.has_won:
            return
            
        self.on_left = False
        self.on_right = False
        
        # Move horizontally
        self.rect.x += self.direction.x * self.speed
        
        # Check for horizontal collisions
        for row_idx in range(len(terrain_layout)):
            for col_idx in range(len(terrain_layout[row_idx])):
                if self.is_solid_tile(terrain_layout[row_idx][col_idx]):
                    tile_rect = pygame.Rect(col_idx * tile_size, row_idx * tile_size, tile_size, tile_size)
                    
                    if self.rect.colliderect(tile_rect):
                        if self.direction.x > 0:  # Moving right
                            self.rect.right = tile_rect.left
                            self.on_right = True
                        elif self.direction.x < 0:  # Moving left
                            self.rect.left = tile_rect.right
                            self.on_left = True

    def vertical_movement_collision(self, terrain_layout):
        """Handle vertical collision detection"""
        if self.is_dead or self.has_won:
            return
            
        self.on_ground = False
        self.on_ceiling = False
        
        # Apply gravity and move vertically
        self.apply_gravity()
        self.rect.y += self.direction.y
        
        # Check for vertical collisions
        for row_idx in range(len(terrain_layout)):
            for col_idx in range(len(terrain_layout[row_idx])):
                if self.is_solid_tile(terrain_layout[row_idx][col_idx]):
                    tile_rect = pygame.Rect(col_idx * tile_size, row_idx * tile_size, tile_size, tile_size)
                    
                    if self.rect.colliderect(tile_rect):
                        if self.direction.y > 0:  # Falling down
                            self.rect.bottom = tile_rect.top
                            self.direction.y = 0
                            self.on_ground = True
                        elif self.direction.y < 0:  # Jumping up
                            self.rect.top = tile_rect.bottom
                            self.direction.y = 0
                            self.on_ceiling = True

    def update(self, terrain_layout=None):
        self.input()
        self.get_status()
        self.animate()
        
        if terrain_layout:
            self.horizontal_movement_collision(terrain_layout)
            self.vertical_movement_collision(terrain_layout)
        else:
            # If no terrain layout, just apply basic movement
            if not self.is_dead and not self.has_won:
                self.rect.x += self.direction.x * self.speed
                self.apply_gravity()
                self.rect.y += self.direction.y
        
        # Always check for death regardless of terrain
        self.check_death()