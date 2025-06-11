#!/usr/bin/env python3
"""
Emotion-Based Level Viewer with AI Integration
==============================================
Main game loop and coordination for the emotion-based platformer.
Integrates ML emotion detection with procedural level generation.
"""

import pygame
import sys
from settings import screen_width, screen_height
from level_viewer import EmotionLevelViewer


def main():
    """Main function with in-game text input."""
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("AI Emotion-Based Level Generator")
    clock = pygame.time.Clock()

    print("AI Emotion-Based Level Generator")
    print("=" * 35)
    print("Use in-game interface to enter experiences!")
    viewer = EmotionLevelViewer(level_number=0, levels_dir="generated_levels")
    
    # Game loop
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            viewer.handle_event(event)

        keys = pygame.key.get_pressed()
        viewer.update_camera(keys)
        viewer.update(dt)
        viewer.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
