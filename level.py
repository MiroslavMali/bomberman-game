import pygame
from settings import *
from game.sprite_manager import SpriteManager
from game.map_manager import MapManager
from game.player import Player
from game.bomb import Bomb

class Level:
    def __init__(self, display_surface, game_state_manager, clock):
        self.display_surface = display_surface
        self.game_state_manager = game_state_manager
        self.clock = clock
        
        # Initialize game components
        self.sprite_manager = SpriteManager()
        self.map_manager = MapManager(self.sprite_manager)
        
        # Create player (start in top-left corner)
        self.player = Player(1, 1, self.sprite_manager, self.map_manager)
        
        # Game state
        self.running = True
        
        # Font for UI
        self.font = pygame.font.Font(None, FONT_SIZE)

    def handle_input(self, events):
        """Handle pygame events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.place_bomb()
    
    def handle_movement(self):
        """Handle continuous movement input"""
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.move()

    def update(self, dt):
        """Update game state"""
        # Update player bombs
        self.player.update_bombs(dt)

    def draw(self):
        """Render everything to screen"""
        # Clear screen
        self.display_surface.fill(BLACK)
        
        # Render map
        self.map_manager.render(self.display_surface)
        
        # Render player bombs
        for bomb in self.player.bombs:
            bomb.render(self.display_surface, self.sprite_manager)
        
        # Render player
        self.player.render(self.display_surface)
        
        # Draw UI
        self.draw_ui()

    def draw_ui(self):
        """Draw user interface elements"""
        # Draw controls info
        controls = [
            "WASD/Arrow Keys: Move",
            "Space: Place Bomb",
            "ESC: Pause"
        ]
        
        for i, control in enumerate(controls):
            text = self.font.render(control, True, WHITE)
            self.display_surface.blit(text, (10, 10 + i * 25))

    def reset(self):
        """Reset the level to initial state"""
        # Recreate player at starting position
        self.player = Player(1, 1, self.sprite_manager, self.map_manager)
        
        # Reset map to initial state
        self.map_manager.reset()
        
        # Reset game state
        self.running = True

    def run(self, events):
        """Main level update and render"""
        # Calculate delta time
        dt = self.clock.tick(120)
        
        # Handle events
        self.handle_input(events)
        
        # Handle movement
        self.handle_movement()
        
        # Update game state
        self.update(dt)
        
        # Render everything
        self.draw() 