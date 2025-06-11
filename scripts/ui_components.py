#!/usr/bin/env python3
"""
UI Components for the Emotion-Based Level Viewer
===============================================
Reusable UI components for the game interface.
"""

import pygame


class TextInputBox:
    def __init__(self, x, y, width, height, prompt_text=""):
        """Initialize text input box."""
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color(100, 100, 100)
        self.color_active = pygame.Color(200, 200, 200)
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.font = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 32)
        self.prompt_text = prompt_text
        self.prompt_font = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 20)
        
        # Cursor
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # Return entered text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Add character if printable
                    if len(self.text) < 80 and event.unicode.isprintable():
                        self.text += event.unicode
        
        return None
    
    def update(self, dt):
        """Update cursor blink."""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # Blink every 500ms
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, surface):
        """Draw the input box."""
        # Draw prompt text above box
        if self.prompt_text:
            prompt_surface = self.prompt_font.render(self.prompt_text, True, (255, 255, 255))
            surface.blit(prompt_surface, (self.rect.x, self.rect.y - 30))
        
        # Draw input box
        pygame.draw.rect(surface, self.color, self.rect, 2)
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        
        # Draw text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 10))
        
        # Draw cursor
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + text_surface.get_width()
            pygame.draw.line(surface, (255, 255, 255), 
                           (cursor_x, self.rect.y + 5), 
                           (cursor_x, self.rect.y + self.rect.height - 5), 2)
    
    def clear(self):
        """Clear the input text."""
        self.text = ''
