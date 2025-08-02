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
        
        # Smart centering system
        self.is_centering = False
        self.centering_target_x = 0
        self.centering_target_y = 0
        self.pending_direction = None  # Store the direction to move after centering
        
        # Bomb placement
        self.bombs = []
        self.max_bombs = 3
        
    def handle_input(self, keys):
        """Handle keyboard input for movement with smart centering"""
        # If we're currently centering, continue centering
        if self.is_centering:
            print("Currently centering, calling handle_centering()")
            self.handle_centering()
            return
        
        # Check if any movement keys are pressed
        pressed_keys = []
        if keys[pygame.K_UP] or keys[pygame.K_w]: pressed_keys.append("UP")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: pressed_keys.append("DOWN")
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: pressed_keys.append("LEFT")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: pressed_keys.append("RIGHT")
        has_multiple_keys = len(pressed_keys) > 1
        
        print(f"Pressed keys: {pressed_keys}")
        
        # If no keys are pressed, stop movement and return
        if not pressed_keys:
            self.dx = 0
            self.dy = 0
            return
        
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
        
        print(f"Primary direction: ({primary_dx}, {primary_dy})")
        
        # Set primary direction
        self.dx = primary_dx
        self.dy = primary_dy
        
        # Check if we can move in primary direction
        can_move_primary = self.can_move_to(self.x + self.dx, self.y + self.dy)
        print(f"Can move primary: {can_move_primary}")
        
        # Check if we're in a corner situation
        is_corner_situation = self.is_in_corner_situation()
        print(f"Is corner situation: {is_corner_situation}")
        
        # DISABLED: Corner situation centering - it's causing the player to get stuck
        # If we're in a corner situation and trying to move, start centering first
        # if is_corner_situation and (primary_dx != 0 or primary_dy != 0):
        #     # Only start centering if the primary movement would actually be blocked
        #     if not can_move_primary:
        #         print("CORNER SITUATION DETECTED - Starting centering process")
        #         # Store the intended direction
        #         self.pending_direction = (primary_dx, primary_dy)
        #         # Start centering
        #         self.start_centering()
        #         return
        #     else:
        #         print("In corner situation but primary movement is allowed, proceeding normally")
        
        # If only one key pressed, use primary movement
        if not has_multiple_keys:
            if can_move_primary:
                return
            else:
                self.dx = 0
                self.dy = 0
                return
        
        # Multiple keys pressed - try diagonal movement for smooth cornering
        # Try diagonal movement for cornering
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
        
        # If diagonal movement failed, fall back to primary movement if possible
        if self.dx == primary_dx and self.dy == primary_dy and not can_move_primary:
            self.dx = 0
            self.dy = 0
    
    def is_in_corner_situation(self):
        """Check if player is in a corner situation (adjacent to 2+ walls)"""
        # Get current tile position
        current_tile_x = int(self.x // TILE_SIZE)
        current_tile_y = int(self.y // TILE_SIZE)
        
        print(f"Checking corner situation at tile ({current_tile_x}, {current_tile_y})")
        
        # Check adjacent tiles for walls
        adjacent_walls = 0
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
            check_x = current_tile_x + dx
            check_y = current_tile_y + dy
            
            # Check bounds
            if (0 <= check_x < self.map_manager.get_width() and 
                0 <= check_y < self.map_manager.get_height()):
                tile_type = self.map_manager.get_tile_type(check_x, check_y)
                if tile_type != 0:  # Wall or brick
                    adjacent_walls += 1
                    print(f"  Wall found at ({check_x}, {check_y})")
                else:
                    print(f"  Walkable at ({check_x}, {check_y})")
        
        print(f"Total adjacent walls: {adjacent_walls}")
        result = adjacent_walls >= 2
        print(f"Is corner situation: {result}")
        return result
    
    def start_centering(self):
        """Start the centering process with directional awareness"""
        # Calculate the center of the current tile
        current_tile_x = int(self.x // TILE_SIZE)
        current_tile_y = int(self.y // TILE_SIZE)
        tile_center_x = current_tile_x * TILE_SIZE + TILE_SIZE // 2
        tile_center_y = current_tile_y * TILE_SIZE + TILE_SIZE // 2
        
        # Get the pending direction to determine which side to center toward
        if self.pending_direction:
            pending_dx, pending_dy = self.pending_direction
            
            # Calculate target center based on the intended direction
            # This centers toward the side where the player wants to go
            if pending_dx < 0:  # Moving left
                self.centering_target_x = tile_center_x - TILE_SIZE // 4  # Center toward left side
            elif pending_dx > 0:  # Moving right
                self.centering_target_x = tile_center_x + TILE_SIZE // 4  # Center toward right side
            else:
                self.centering_target_x = tile_center_x  # No horizontal movement, use center
                
            if pending_dy < 0:  # Moving up
                self.centering_target_y = tile_center_y - TILE_SIZE // 4  # Center toward top side
            elif pending_dy > 0:  # Moving down
                self.centering_target_y = tile_center_y + TILE_SIZE // 4  # Center toward bottom side
            else:
                self.centering_target_y = tile_center_y  # No vertical movement, use center
        else:
            # Fallback to tile center if no pending direction
            self.centering_target_x = tile_center_x
            self.centering_target_y = tile_center_y
        
        # Only start centering if we're not already close to the target
        distance_x = abs(self.x - self.centering_target_x)
        distance_y = abs(self.y - self.centering_target_y)
        
        if distance_x > 2 or distance_y > 2:
            self.is_centering = True
            self.dx = 0
            self.dy = 0
        else:
            # We're already close to the target, move in the pending direction
            self.move_in_pending_direction()
    
    def handle_centering(self):
        """Handle the centering movement"""
        print("=== HANDLE CENTERING DEBUG ===")
        # Calculate direction to center
        dx_to_center = self.centering_target_x - self.x
        dy_to_center = self.centering_target_y - self.y
        
        print(f"Current position: ({self.x}, {self.y})")
        print(f"Target center: ({self.centering_target_x}, {self.centering_target_y})")
        print(f"Distance to center: dx={dx_to_center}, dy={dy_to_center}")
        
        # Move toward center
        if abs(dx_to_center) > 2:
            self.dx = self.speed if dx_to_center > 0 else -self.speed
            print(f"Moving X: {self.dx}")
        else:
            self.dx = 0
            print("X movement stopped")
            
        if abs(dy_to_center) > 2:
            self.dy = self.speed if dy_to_center > 0 else -self.speed
            print(f"Moving Y: {self.dy}")
        else:
            self.dy = 0
            print("Y movement stopped")
        
        # Actually update the player position here
        new_x = self.x + self.dx
        new_y = self.y + self.dy
        
        # Check if we can move to the new position
        can_move_x = self.can_move_to(new_x, self.y)
        can_move_y = self.can_move_to(self.x, new_y)
        
        print(f"Can move X: {can_move_x}, Can move Y: {can_move_y}")
        
        # Update position based on what's allowed
        if can_move_x:
            self.x = new_x
        if can_move_y:
            self.y = new_y
        
        print(f"New position after movement: ({self.x}, {self.y})")
        
        # Check if we've reached the center
        if abs(self.x - self.centering_target_x) <= 2 and abs(self.y - self.centering_target_y) <= 2:
            print("Reached target, snapping to exact position")
            # Snap to exact center
            self.x = self.centering_target_x
            self.y = self.centering_target_y
            # Stop centering and move in pending direction
            self.is_centering = False
            print("Stopping centering, moving in pending direction")
            self.move_in_pending_direction()
        print("=== END HANDLE CENTERING DEBUG ===")
    
    def move_in_pending_direction(self):
        """Move in the direction that was pending during centering"""
        if self.pending_direction:
            pending_dx, pending_dy = self.pending_direction
            self.dx = pending_dx
            self.dy = pending_dy
            self.pending_direction = None
    
    def can_move_diagonally(self, x, y):
        """More permissive collision check for diagonal movement with corner detection"""
        # For diagonal movement, we want to be very permissive to allow smooth cornering
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
        
        # Detect if we're in a corner situation
        # Check if there are walls on two adjacent sides
        current_tile_x = int(self.x // TILE_SIZE)
        current_tile_y = int(self.y // TILE_SIZE)
        
        # Check adjacent tiles for walls
        adjacent_walls = 0
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
            check_x = current_tile_x + dx
            check_y = current_tile_y + dy
            if (0 <= check_x < self.map_manager.get_width() and 
                0 <= check_y < self.map_manager.get_height()):
                tile_type = self.map_manager.get_tile_type(check_x, check_y)
                if tile_type != 0:  # Wall
                    adjacent_walls += 1
        
        # If we have 2 or more adjacent walls, we're in a corner situation
        # Use a much smaller collision box to allow cornering
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
        
        # Be very permissive for diagonal movement - only require center and 1 other point
        # This allows cornering even when the player is close to walls
        return walkable_points >= 2  # Center + at least 1 other point
    
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
        for i, (corner_x, corner_y) in enumerate(corners):
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
        
        # Debug collision visualization
        DEBUG_COLLISION = True  # Set to True to see collision boxes
        if DEBUG_COLLISION:
            # Draw player collision box
            pygame.draw.rect(screen, (255, 255, 0), (render_x, render_y, self.size, self.size), 2)
            
            # Draw player center point
            center_x = int(self.x)
            center_y = int(self.y)
            pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), 3)
            
            # Draw collision check points for can_move_to (normal movement)
            half_size = self.size // 2 - 1
            corners = [
                (self.x - half_size, self.y - half_size),  # Top-left
                (self.x + half_size, self.y - half_size),  # Top-right
                (self.x - half_size, self.y + half_size),  # Bottom-left
                (self.x + half_size, self.y + half_size)   # Bottom-right
            ]
            
            for i, (corner_x, corner_y) in enumerate(corners):
                # Convert to tile coordinates
                tile_x = int(corner_x // TILE_SIZE)
                tile_y = int(corner_y // TILE_SIZE)
                
                # Check if tile is walkable
                if (0 <= tile_x < self.map_manager.get_width() and 
                    0 <= tile_y < self.map_manager.get_height()):
                    tile_type = self.map_manager.get_tile_type(tile_x, tile_y)
                    is_walkable = tile_type == 0
                    
                    # Draw corner point with color based on walkability
                    color = (0, 255, 0) if is_walkable else (255, 0, 0)  # Green if walkable, red if not
                    pygame.draw.circle(screen, color, (int(corner_x), int(corner_y)), 2)
                    
                    # Draw tile grid for reference
                    tile_pixel_x = tile_x * TILE_SIZE
                    tile_pixel_y = tile_y * TILE_SIZE
                    pygame.draw.rect(screen, (100, 100, 100), (tile_pixel_x, tile_pixel_y, TILE_SIZE, TILE_SIZE), 1)
            
            # Draw diagonal movement check points with corner detection
            current_tile_x = int(self.x // TILE_SIZE)
            current_tile_y = int(self.y // TILE_SIZE)
            
            # Check adjacent tiles for walls to determine corner situation
            adjacent_walls = 0
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
                check_x = current_tile_x + dx
                check_y = current_tile_y + dy
                if (0 <= check_x < self.map_manager.get_width() and 
                    0 <= check_y < self.map_manager.get_height()):
                    tile_type = self.map_manager.get_tile_type(check_x, check_y)
                    if tile_type != 0:  # Wall
                        adjacent_walls += 1
            
            # Use different collision box size based on corner situation
            if adjacent_walls >= 2:
                half_size_diag = self.size // 2 - 6  # Very small for cornering
                corner_color = (255, 128, 0)  # Orange for corner situation
            else:
                half_size_diag = self.size // 2 - 4  # Normal small
                corner_color = (0, 255, 255)  # Cyan for normal
            
            diag_points = [
                (self.x, self.y),  # Center
                (self.x - half_size_diag, self.y - half_size_diag),  # Top-left
                (self.x + half_size_diag, self.y - half_size_diag),  # Top-right
                (self.x - half_size_diag, self.y + half_size_diag),  # Bottom-left
                (self.x + half_size_diag, self.y + half_size_diag)   # Bottom-right
            ]
            
            for i, (point_x, point_y) in enumerate(diag_points):
                # Convert to tile coordinates
                tile_x = int(point_x // TILE_SIZE)
                tile_y = int(point_y // TILE_SIZE)
                
                # Check if tile is walkable
                if (0 <= tile_x < self.map_manager.get_width() and 
                    0 <= tile_y < self.map_manager.get_height()):
                    tile_type = self.map_manager.get_tile_type(tile_x, tile_y)
                    is_walkable = tile_type == 0
                    
                    # Draw diagonal check point with color based on walkability and corner situation
                    if is_walkable:
                        color = corner_color
                    else:
                        color = (255, 0, 255)  # Magenta if not walkable
                    
                    size = 4 if i == 0 else 3  # Center point is larger
                    pygame.draw.circle(screen, color, (int(point_x), int(point_y)), size)
            
            # Draw adjacent wall indicator
            if adjacent_walls >= 2:
                # Draw a small indicator that we're in a corner situation
                pygame.draw.circle(screen, (255, 0, 0), (center_x + 20, center_y - 20), 8)
                pygame.draw.circle(screen, (255, 255, 255), (center_x + 20, center_y - 20), 8, 2)
            
            # Draw smart centering indicators
            if self.is_centering:
                # Draw centering target
                pygame.draw.circle(screen, (0, 255, 0), (int(self.centering_target_x), int(self.centering_target_y)), 6)
                pygame.draw.circle(screen, (0, 0, 0), (int(self.centering_target_x), int(self.centering_target_y)), 6, 2)
                
                # Draw line from player to centering target
                pygame.draw.line(screen, (0, 255, 0), (center_x, center_y), 
                               (int(self.centering_target_x), int(self.centering_target_y)), 2)
                
                # Draw "CENTERING" text
                font = pygame.font.Font(None, 24)
                text = font.render("CENTERING", True, (0, 255, 0))
                screen.blit(text, (center_x - 40, center_y - 40))
                
                # Draw directional indicator
                if self.pending_direction:
                    pending_dx, pending_dy = self.pending_direction
                    if pending_dx != 0 or pending_dy != 0:
                        # Draw arrow showing the direction we're centering toward
                        arrow_start = (center_x, center_y)
                        arrow_end = (center_x + pending_dx * 2, center_y + pending_dy * 2)
                        pygame.draw.line(screen, (255, 255, 0), arrow_start, arrow_end, 3)
                        pygame.draw.circle(screen, (255, 255, 0), (int(arrow_end[0]), int(arrow_end[1])), 4)
                        
                        # Draw "TOWARD" text
                        font = pygame.font.Font(None, 20)
                        text = font.render("TOWARD", True, (255, 255, 0))
                        screen.blit(text, (center_x - 30, center_y + 20))
            
            # Draw pending direction indicator
            if self.pending_direction:
                pending_dx, pending_dy = self.pending_direction
                if pending_dx != 0 or pending_dy != 0:
                    # Draw arrow showing pending direction
                    arrow_start = (center_x, center_y)
                    arrow_end = (center_x + pending_dx * 3, center_y + pending_dy * 3)
                    pygame.draw.line(screen, (255, 255, 0), arrow_start, arrow_end, 4)
                    pygame.draw.circle(screen, (255, 255, 0), (int(arrow_end[0]), int(arrow_end[1])), 6)
                    
                    # Draw "PENDING" text
                    font = pygame.font.Font(None, 20)
                    text = font.render("PENDING", True, (255, 255, 0))
                    screen.blit(text, (center_x - 30, center_y + 30))
            
            # Draw movement direction indicator
            if self.dx != 0 or self.dy != 0:
                # Draw arrow showing current movement direction
                arrow_start = (center_x, center_y)
                arrow_end = (center_x + self.dx * 2, center_y + self.dy * 2)
                pygame.draw.line(screen, (0, 255, 255), arrow_start, arrow_end, 3)
                pygame.draw.circle(screen, (0, 255, 255), (int(arrow_end[0]), int(arrow_end[1])), 4)
            
            # Draw target tile center for diagonal movement
            if self.dx != 0 and self.dy != 0:
                # Calculate target tile center
                target_x = self.x + self.dx
                target_y = self.y + self.dy
                target_tile_x = int(target_x // TILE_SIZE)
                target_tile_y = int(target_y // TILE_SIZE)
                target_center_x = target_tile_x * TILE_SIZE + TILE_SIZE // 2
                target_center_y = target_tile_y * TILE_SIZE + TILE_SIZE // 2
                
                # Draw target center with a different color
                pygame.draw.circle(screen, (255, 255, 255), (int(target_center_x), int(target_center_y)), 5)
                pygame.draw.circle(screen, (0, 0, 0), (int(target_center_x), int(target_center_y)), 5, 2) 