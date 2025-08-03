import pygame
from settings import *
from sprite_manager import SpriteManager
from map_manager import MapManager
from player import Player
from bomb import Bomb
from death_screen import DeathScreen

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
        self.player_dead = False
        
        # Death screen
        self.death_screen = DeathScreen(display_surface, game_state_manager)
        
        # Font for UI
        self.font = pygame.font.Font(None, FONT_SIZE)

    def handle_input(self, events):
        """Handle pygame events"""
        if self.player_dead:
            self.death_screen.handle_input(events)
            return
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.place_bomb()
    
    def handle_movement(self):
        """Handle continuous movement input"""
        if self.player_dead:
            return
            
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.move()

    def update(self, dt):
        """Update game state"""
        if self.player_dead:
            self.death_screen.update()
            return
            
        # Update player bombs
        self.player.update_bombs(dt)
        
        # Check for player death
        self.check_player_death()
        
        # Check for chain reactions
        self.check_chain_reactions()

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
        
        # Draw death screen if player is dead
        if self.player_dead:
            self.death_screen.draw()

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
        self.player_dead = False
    
    def check_player_death(self):
        """Check if player is hit by any explosion"""
        if self.player_dead:
            return
            
        # Check all bombs for explosion collision
        for bomb in self.player.bombs:
            if bomb.is_player_hit_by_explosion(self.player.x, self.player.y, self.player.size):
                self.player_dead = True
                self.death_screen.start_death_sequence()
                return
    
    def check_chain_reactions(self):
        """Check if any exploding bombs should trigger other bombs"""
        # Check each bomb that is currently exploding
        for bomb in self.player.bombs:
            if bomb.exploded and not bomb.finished:
                # Check if this explosion hits any other bombs
                for other_bomb in self.player.bombs:
                    if other_bomb != bomb and not other_bomb.exploded:
                        # Check if other bomb is in this explosion's area
                        if self.is_bomb_in_explosion_area(other_bomb, bomb):
                            # Trigger the other bomb to explode immediately
                            other_bomb.explode()
    
    def is_bomb_in_explosion_area(self, bomb, exploding_bomb):
        """Check if a bomb is in the explosion area of another bomb"""
        # Check if the bomb's tile position is in the explosion positions
        for explosion_x, explosion_y in exploding_bomb.explosion_positions:
            if bomb.tile_x == explosion_x and bomb.tile_y == explosion_y:
                return True
        return False

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