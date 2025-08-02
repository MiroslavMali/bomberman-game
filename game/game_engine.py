"""
Game Engine - Main game loop and coordination
"""

import pygame
import sys
from config import *
from game.sprite_manager import SpriteManager
from game.map_manager import MapManager
from game.player import Player

class GameEngine:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.sprite_manager = SpriteManager()
        self.map_manager = MapManager(self.sprite_manager)
        
        # Create player (start in top-left corner)
        self.player = Player(1, 1, self.sprite_manager, self.map_manager)
        
        # Game state
        self.running = True
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.place_bomb()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self, dt):
        """Update game state"""
        # Handle input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # Update player
        self.player.move()
        self.player.update_bombs(dt)
    
    def render(self):
        """Render everything to screen"""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Render map
        self.map_manager.render(self.screen)
        
        # Render player bombs
        for bomb in self.player.bombs:
            bomb.render(self.screen, self.sprite_manager)
        
        # Render player
        self.player.render(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        try:
            while self.running:
                # Calculate delta time
                dt = self.clock.tick(FPS)
                
                # Handle events
                self.handle_events()
                
                # Update game state
                self.update(dt)
                
                # Render everything
                self.render()
                
        except Exception as e:
            print(f"Error in game loop: {e}")
        finally:
            pygame.quit()
            sys.exit() 