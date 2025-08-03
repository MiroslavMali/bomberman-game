"""
Death Screen - Shows when player dies and provides restart/exit options
"""

import pygame
from settings import *

class DeathScreen:
    def __init__(self, display_surface, game_state_manager):
        self.display_surface = display_surface
        self.game_state_manager = game_state_manager
        
        # Font for text
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        
        # Menu options
        self.options = ["New Game", "Exit"]
        self.selected_option = 0
        
        # Death timer
        self.death_time = None
        self.show_menu = False
        self.menu_delay = 1.5  # Show menu after x seconds
        
    def start_death_sequence(self):
        """Start the death sequence"""
        self.death_time = pygame.time.get_ticks()
        self.show_menu = False
        self.selected_option = 0
        
    def handle_input(self, events):
        """Handle input for death screen"""
        if not self.show_menu:
            return
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()
                    
    def select_option(self):
        """Handle option selection"""
        if self.options[self.selected_option] == "New Game":
            self.game_state_manager.request_reset()
            self.game_state_manager.set_state('level')
        elif self.options[self.selected_option] == "Exit":
            pygame.quit()
            exit()
            
    def update(self):
        """Update death screen state"""
        if self.death_time is None:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.death_time) / 1000.0
        
        if elapsed >= self.menu_delay and not self.show_menu:
            self.show_menu = True
            
    def draw(self):
        """Draw the death screen"""
        # Dark overlay
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        # Death message
        death_text = self.title_font.render("YOU DIED", True, (255, 0, 0))
        death_rect = death_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 100))
        self.display_surface.blit(death_text, death_rect)
        
        # Show menu after delay
        if self.show_menu:
            # Draw menu options
            for i, option in enumerate(self.options):
                color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
                text = self.menu_font.render(option, True, color)
                rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 50 + i * 60))
                self.display_surface.blit(text, rect)
                
            # Draw selection indicator
            if self.selected_option < len(self.options):
                indicator = self.menu_font.render(">", True, (255, 255, 0))
                indicator_rect = indicator.get_rect(center=(DISPLAY_WIDTH // 2 - 100, DISPLAY_HEIGHT // 2 + 50 + self.selected_option * 60))
                self.display_surface.blit(indicator, indicator_rect) 