"""
Player - Handles player movement, bomb placement, and collision detection
"""

import pygame
from config import TILE_SIZE, PLAYER_SIZE, PLAYER_SPEED

class Player:
    def __init__(self, x, y, sprite_manager, map_manager):
        self.x = x * TILE_SIZE + TILE_SIZE // 2  # Center in tile
        self.y = y * TILE_SIZE + TILE_SIZE // 2
        self.sprite_manager = sprite_manager
        self.map_manager = map_manager
        self.speed = PLAYER_SPEED
        self.size = PLAYER_SIZE
        
        # Movement
        self.dx = 0
        self.dy = 0
        
        # Bomb placement
        self.bombs = []
        self.max_bombs = 1
        
    def handle_input(self, keys):
        """Handle keyboard input for movement"""
        self.dx = 0
        self.dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dy = self.speed
    
    def move(self):
        """Move the player with improved collision detection"""
        new_x = self.x + self.dx
        new_y = self.y + self.dy
        
        # Check collision for X movement
        if self.can_move_to(new_x, self.y):
            self.x = new_x
        
        # Check collision for Y movement
        if self.can_move_to(self.x, new_y):
            self.y = new_y
    
    def can_move_to(self, x, y):
        """Check if player can move to position using bounding box collision"""
        # Calculate player bounding box
        half_size = self.size // 2
        left = x - half_size
        right = x + half_size
        top = y - half_size
        bottom = y + half_size
        
        # Check all four corners of the player bounding box
        corners = [
            (left, top),      # Top-left
            (right, top),     # Top-right
            (left, bottom),   # Bottom-left
            (right, bottom)   # Bottom-right
        ]
        
        for corner_x, corner_y in corners:
            # Convert to tile coordinates
            tile_x = int(corner_x // TILE_SIZE)
            tile_y = int(corner_y // TILE_SIZE)
            
            # Check if any corner hits a wall
            if not self.map_manager.is_walkable(tile_x, tile_y):
                return False
        
        return True
    
    def place_bomb(self):
        """Place a bomb at current position"""
        if len(self.bombs) < self.max_bombs:
            # Get tile coordinates
            tile_x = int(self.x // TILE_SIZE)
            tile_y = int(self.y // TILE_SIZE)
            
            # Check if there's already a bomb here
            for bomb in self.bombs:
                if bomb.tile_x == tile_x and bomb.tile_y == tile_y:
                    return False
            
            # Create new bomb
            from game.bomb import Bomb
            bomb = Bomb(tile_x, tile_y, self.map_manager)
            self.bombs.append(bomb)
            return True
        return False
    
    def update_bombs(self, dt):
        """Update all bombs"""
        for bomb in self.bombs[:]:  # Copy list to avoid modification during iteration
            bomb.update(dt)
            if bomb.finished:  # Use the new finished state
                self.bombs.remove(bomb)
    
    def get_grid_position(self):
        """Get player's grid position"""
        return (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))
    
    def render(self, screen):
        """Render the player"""
        # Calculate position to center player sprite
        render_x = self.x - self.size // 2
        render_y = self.y - self.size // 2
        
        # Get player sprite and scale it
        player_sprite = self.sprite_manager.get_sprite('player')
        if player_sprite:
            scaled_sprite = pygame.transform.scale(player_sprite, (self.size, self.size))
            screen.blit(scaled_sprite, (render_x, render_y))
        else:
            # Fallback rectangle
            pygame.draw.rect(screen, (255, 0, 0), (render_x, render_y, self.size, self.size))
        
        # Debug: Draw collision box
        from config import DEBUG_COLLISION
        if DEBUG_COLLISION:
            pygame.draw.rect(screen, (255, 255, 0), (render_x, render_y, self.size, self.size), 2) 