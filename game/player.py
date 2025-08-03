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
        self.max_bombs = 1
        
    def handle_input(self, keys):
        """Handle keyboard input for movement"""
        # Check if any movement keys are pressed
        pressed_keys = []
        if keys[pygame.K_UP] or keys[pygame.K_w]: pressed_keys.append("UP")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: pressed_keys.append("DOWN")
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: pressed_keys.append("LEFT")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: pressed_keys.append("RIGHT")
        
        # If no keys are pressed, stop movement
        if not pressed_keys:
            self.dx = 0
            self.dy = 0
            return
        
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
        target_x = self.x + self.dx
        target_y = self.y + self.dy
        can_move_primary = self.can_move_to(target_x, target_y)
        
        # If only one key pressed, use primary movement
        if len(pressed_keys) == 1:
            if not can_move_primary:
                self.dx = 0
                self.dy = 0
            return
        
        # Multiple keys pressed - try diagonal movement for smooth cornering
        if primary_dx != 0:  # Moving horizontally
            # Try diagonal movement by adding vertical component
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                diagonal_x = self.x + self.dx
                diagonal_y = self.y - self.speed
                can_diagonal = self.can_move_diagonally(diagonal_x, diagonal_y)
                if can_diagonal:
                    self.dy = -self.speed
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                diagonal_x = self.x + self.dx
                diagonal_y = self.y + self.speed
                can_diagonal = self.can_move_diagonally(diagonal_x, diagonal_y)
                if can_diagonal:
                    self.dy = self.speed
        elif primary_dy != 0:  # Moving vertically
            # Try diagonal movement by adding horizontal component
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                diagonal_x = self.x - self.speed
                diagonal_y = self.y + self.dy
                can_diagonal = self.can_move_diagonally(diagonal_x, diagonal_y)
                if can_diagonal:
                    self.dx = -self.speed
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                diagonal_x = self.x + self.speed
                diagonal_y = self.y + self.dy
                can_diagonal = self.can_move_diagonally(diagonal_x, diagonal_y)
                if can_diagonal:
                    self.dx = self.speed
        
        # If diagonal movement failed, fall back to primary movement if possible
        if self.dx == primary_dx and self.dy == primary_dy and not can_move_primary:
            self.dx = 0
            self.dy = 0
    
    def is_on_bomb(self):
        """Check if player is currently on a bomb"""
        # Check if any part of the player is on a bomb
        half_size = self.size // 2 - 1
        
        # Check all four corners of the player
        corners = [
            (self.x - half_size, self.y - half_size),  # Top-left
            (self.x + half_size, self.y - half_size),  # Top-right
            (self.x - half_size, self.y + half_size),  # Bottom-left
            (self.x + half_size, self.y + half_size)   # Bottom-right
        ]
        
        for bomb in self.bombs:
            if not bomb.is_placeable():  # Bomb is still active
                # Check if any corner of the player is on this bomb
                for corner_x, corner_y in corners:
                    corner_tile_x = int(corner_x // TILE_SIZE)
                    corner_tile_y = int(corner_y // TILE_SIZE)
                    
                    if bomb.tile_x == corner_tile_x and bomb.tile_y == corner_tile_y:
                        return True
        
        return False
    
    def can_move_diagonally(self, x, y):
        """More permissive collision check for diagonal movement"""
        # Check the target tile first
        target_tile_x = int(x // TILE_SIZE)
        target_tile_y = int(y // TILE_SIZE)
        
        # Check bounds
        if (target_tile_x < 0 or target_tile_x >= self.map_manager.get_width() or 
            target_tile_y < 0 or target_tile_y >= self.map_manager.get_height()):
            return False
        
        target_tile_type = self.map_manager.get_tile_type(target_tile_x, target_tile_y)
        
        # If target is not walkable, definitely can't move there
        if target_tile_type != 0:  # Not grass
            return False
        
        # NEW LOGIC: If we're currently on a bomb, allow movement to any walkable tile
        on_bomb = self.is_on_bomb()
        if on_bomb:
            return True
        
        # If we're not on a bomb, check if target has a bomb
        for bomb in self.bombs:
            if bomb.tile_x == target_tile_x and bomb.tile_y == target_tile_y:
                if not bomb.is_placeable():  # Bomb is still active
                    return False
        
        # Check if we're in a corner situation (adjacent to 2+ walls)
        current_tile_x = int(self.x // TILE_SIZE)
        current_tile_y = int(self.y // TILE_SIZE)
        
        adjacent_walls = 0
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
            check_x = current_tile_x + dx
            check_y = current_tile_y + dy
            if (0 <= check_x < self.map_manager.get_width() and 
                0 <= check_y < self.map_manager.get_height()):
                tile_type = self.map_manager.get_tile_type(check_x, check_y)
                if tile_type != 0:  # Wall
                    adjacent_walls += 1
        
        # Use smaller collision box for cornering
        if adjacent_walls >= 2:
            half_size = (self.size // 2) - 6  # Very small collision box for cornering
        else:
            half_size = (self.size // 2) - 4  # Normal small collision box
        
        # Check center and corners of the collision box
        check_points = [
            (x, y),  # Center
            (x - half_size, y - half_size),  # Top-left
            (x + half_size, y - half_size),  # Top-right
            (x - half_size, y + half_size),  # Bottom-left
            (x + half_size, y + half_size)   # Bottom-right
        ]
        
        walkable_points = 0
        
        for check_x, check_y in check_points:
            tile_x = int(check_x // TILE_SIZE)
            tile_y = int(check_y // TILE_SIZE)
            
            # Check bounds
            if (tile_x < 0 or tile_x >= self.map_manager.get_width() or 
                tile_y < 0 or tile_y >= self.map_manager.get_height()):
                continue
            
            tile_type = self.map_manager.get_tile_type(tile_x, tile_y)
            if tile_type == 0:  # Grass is walkable
                walkable_points += 1
        
        # Be permissive for diagonal movement - require center and at least 1 other point
        return walkable_points >= 2
    
    def can_move_to(self, x, y):
        """Check if player can move to the given position"""
        # Calculate the tile coordinates that the player would occupy
        half_size = self.size // 2 - 1
        
        # Check all four corners of the player
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
            
            # Check if tile is walkable (0 = grass, 1 = unbreakable wall, 2 = breakable brick)
            tile_type = self.map_manager.get_tile_type(tile_x, tile_y)
            if tile_type != 0:  # Not walkable if not grass
                return False
        
        # NEW LOGIC: If we're currently on a bomb, allow movement to any walkable tile
        on_bomb = self.is_on_bomb()
        if on_bomb:
            return True
        
        # If we're not on a bomb, check if any corner would land on a bomb
        for corner_x, corner_y in corners:
            tile_x = int(corner_x // TILE_SIZE)
            tile_y = int(corner_y // TILE_SIZE)
            
            for bomb in self.bombs:
                if bomb.tile_x == tile_x and bomb.tile_y == tile_y:
                    if not bomb.is_placeable():  # Bomb is still active
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
            
            # Check if there's already a bomb here that blocks placement
            for bomb in self.bombs:
                if bomb.tile_x == tile_x and bomb.tile_y == tile_y:
                    if not bomb.is_placeable():
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
        # Calculate render position (center of player)
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