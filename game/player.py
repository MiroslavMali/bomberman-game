"""
Player - Handles player movement, bomb placement, and collision detection
"""

import pygame
from settings import TILE_SIZE, PLAYER_SIZE, PLAYER_SPEED

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
        self.max_bombs = 3
        
    def handle_input(self, keys):
        """Handle keyboard input for movement"""
        self.dx = 0
        self.dy = 0
        
        # Get primary movement direction
        primary_dx = 0
        primary_dy = 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            primary_dy = -self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            primary_dy = self.speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            primary_dx = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            primary_dx = self.speed
        
        # Set primary direction
        self.dx = primary_dx
        self.dy = primary_dy
        
        # Check if we can move in primary direction
        if self.can_move_to(self.x + self.dx, self.y + self.dy):
            return  # Primary movement is possible, no cornering needed
        
        # Primary movement blocked - try diagonal movement for cornering
        if primary_dx != 0:  # Moving horizontally
            # Try diagonal movement by adding vertical component
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                # Try diagonal up-left or up-right
                if self.can_move_diagonally(self.x + self.dx, self.y - self.speed):
                    self.dy = -self.speed
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                # Try diagonal down-left or down-right
                if self.can_move_diagonally(self.x + self.dx, self.y + self.speed):
                    self.dy = self.speed
        elif primary_dy != 0:  # Moving vertically
            # Try diagonal movement by adding horizontal component
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                # Try diagonal left-up or left-down
                if self.can_move_diagonally(self.x - self.speed, self.y + self.dy):
                    self.dx = -self.speed
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                # Try diagonal right-up or right-down
                if self.can_move_diagonally(self.x + self.speed, self.y + self.dy):
                    self.dx = self.speed
    
    def can_move_diagonally(self, x, y):
        """Check if player can move diagonally (more permissive for cornering)"""
        # For diagonal movement, we're more permissive
        # Check multiple positions around the target to allow for slight misalignment
        
        # Check the target position
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        
        # Check bounds
        if (tile_x < 0 or tile_x >= self.map_manager.get_width() or 
            tile_y < 0 or tile_y >= self.map_manager.get_height()):
            return False
        
        # Check if the target tile is walkable
        if not self.map_manager.is_walkable(tile_x, tile_y):
            return False
        
        # Also check if we can actually reach this position (not blocked by walls)
        # Use a more permissive collision check for diagonal movement
        half_size = self.size // 2 - 2  # Smaller collision box for diagonal movement
        corners = [
            (x - half_size, y - half_size),  # Top-left
            (x + half_size, y - half_size),  # Top-right
            (x - half_size, y + half_size),  # Bottom-left
            (x + half_size, y + half_size)   # Bottom-right
        ]
        
        # Check if most corners are within walkable tiles (allow some overlap)
        walkable_corners = 0
        for corner_x, corner_y in corners:
            corner_tile_x = int(corner_x // TILE_SIZE)
            corner_tile_y = int(corner_y // TILE_SIZE)
            
            # Check bounds
            if (corner_tile_x < 0 or corner_tile_x >= self.map_manager.get_width() or 
                corner_tile_y < 0 or corner_tile_y >= self.map_manager.get_height()):
                continue
            
            # Check if tile is walkable
            if self.map_manager.is_walkable(corner_tile_x, corner_tile_y):
                walkable_corners += 1
        
        # Allow movement if at least 3 out of 4 corners are walkable
        return walkable_corners >= 3
    
    def can_move_to(self, x, y):
        """Check if player can move to position"""
        # Calculate the corners of the player's bounding box
        half_size = self.size // 2 + 1 # Increased buffer to reduce wiggle
        corners = [
            (x - half_size, y - half_size),  # Top-left
            (x + half_size, y - half_size),  # Top-right
            (x - half_size, y + half_size),  # Bottom-left
            (x + half_size, y + half_size)   # Bottom-right
        ]
        
        # Check if all corners are within walkable tiles
        for corner_x, corner_y in corners:
            tile_x = int(corner_x // TILE_SIZE)
            tile_y = int(corner_y // TILE_SIZE)
            
            # Check bounds
            if (tile_x < 0 or tile_x >= self.map_manager.get_width() or 
                tile_y < 0 or tile_y >= self.map_manager.get_height()):
                return False
            
            # Check if tile is walkable
            if not self.map_manager.is_walkable(tile_x, tile_y):
                return False
        
        return True
    
    def move(self):
        """Update player position"""
        # Calculate new position
        new_x = self.x + self.dx
        new_y = self.y + self.dy
        
        # Check if we can move to the new position
        can_move_x = self.can_move_to(new_x, self.y)
        can_move_y = self.can_move_to(self.x, new_y)
        
        # Update position based on what's allowed
        if can_move_x:
            self.x = new_x
        if can_move_y:
            self.y = new_y
        
        # Snap to grid when not moving
        if self.dx == 0 and self.dy == 0:
            self.snap_to_grid()
    
    def snap_to_grid(self):
        """Snap player to nearest tile center"""
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        target_x = tile_x * TILE_SIZE + TILE_SIZE // 2
        target_y = tile_y * TILE_SIZE + TILE_SIZE // 2
        
        # Only snap if close enough (within 3 pixels)
        if abs(self.x - target_x) < 3:
            self.x = target_x
        if abs(self.y - target_y) < 3:
            self.y = target_y
    
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
        # Calculate position to center player sprite on tile
        render_x = self.x - self.size // 2
        render_y = self.y - self.size // 2
        
        # Get player sprite and scale it to player size
        player_sprite = self.sprite_manager.get_sprite('player')
        if player_sprite:
            # Scale to player size for good visual fit
            scaled_sprite = pygame.transform.scale(player_sprite, (self.size, self.size))
            screen.blit(scaled_sprite, (render_x, render_y))
        else:
            # Fallback rectangle
            pygame.draw.rect(screen, (255, 0, 0), (render_x, render_y, self.size, self.size))
        
        # Debug: Draw collision box
        DEBUG_COLLISION = False  # Set to True to see collision boxes
        if DEBUG_COLLISION:
            pygame.draw.rect(screen, (255, 255, 0), (render_x, render_y, self.size, self.size), 2) 