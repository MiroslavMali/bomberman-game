"""
Bomb - Handles bomb placement, timing, and explosion logic
"""

import pygame
import time
from config import TILE_SIZE, BOMB_TIMER, EXPLOSION_DURATION, EXPLOSION_RANGE

class Bomb:
    def __init__(self, tile_x, tile_y, map_manager):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.map_manager = map_manager
        self.place_time = time.time()
        self.exploded = False
        self.explosion_start = None
        self.explosion_positions = []
        self.finished = False  # New state to track when bomb should be removed
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.frame_duration = 200  # milliseconds
        
    def update(self, dt):
        """Update bomb state"""
        current_time = time.time()
        
        if not self.exploded:
            # Check if bomb should explode
            if current_time - self.place_time >= BOMB_TIMER / 1000.0:
                self.explode()
            else:
                # Update animation
                self.animation_timer += dt
                if self.animation_timer >= self.frame_duration:
                    self.animation_timer = 0
                    self.animation_frame = (self.animation_frame + 1) % 3
        else:
            # Check if explosion should end
            if current_time - self.explosion_start >= EXPLOSION_DURATION / 1000.0:
                self.finished = True  # Signal to remove bomb
    
    def explode(self):
        """Trigger bomb explosion"""
        self.exploded = True
        self.explosion_start = time.time()
        
        # Calculate explosion positions
        self.explosion_positions = []
        
        # Center explosion
        self.explosion_positions.append((self.tile_x, self.tile_y))
        
        # Explosion in all 4 directions
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, Down, Left, Right
        
        for dx, dy in directions:
            for distance in range(1, EXPLOSION_RANGE + 1):
                x = self.tile_x + dx * distance
                y = self.tile_y + dy * distance
                
                # Check if position is valid
                if not (0 <= x < self.map_manager.map_data[0].__len__() and 
                       0 <= y < self.map_manager.map_data.__len__()):
                    break
                
                tile_type = self.map_manager.get_tile_type(x, y)
                
                if tile_type == 1:  # Wall - stop explosion
                    break
                elif tile_type == 2:  # Breakable brick - destroy and stop
                    self.map_manager.destroy_brick(x, y)
                    self.explosion_positions.append((x, y))
                    break
                else:  # Grass - continue explosion
                    self.explosion_positions.append((x, y))
    
    def render(self, screen, sprite_manager):
        """Render the bomb or explosion"""
        if not self.exploded:
            # Render bomb with animation
            bomb_sprite = sprite_manager.get_bomb_frame(self.animation_frame)
            if bomb_sprite:
                screen.blit(bomb_sprite, (self.tile_x * TILE_SIZE, self.tile_y * TILE_SIZE))
            else:
                # Fallback circle
                center = (self.tile_x * TILE_SIZE + TILE_SIZE // 2, 
                         self.tile_y * TILE_SIZE + TILE_SIZE // 2)
                pygame.draw.circle(screen, (0, 0, 0), center, TILE_SIZE // 3)
        else:
            # Render explosion
            current_time = time.time()
            if self.explosion_start and current_time - self.explosion_start < EXPLOSION_DURATION / 1000.0:
                # Calculate explosion animation frame
                elapsed = current_time - self.explosion_start
                frame_index = int((elapsed / (EXPLOSION_DURATION / 1000.0)) * 3)
                frame_index = min(frame_index, 2)  # Clamp to valid range
                
                explosion_sprite = sprite_manager.get_explosion_frame(frame_index)
                
                for x, y in self.explosion_positions:
                    if explosion_sprite:
                        # Scale explosion sprite to 140% (40% bigger)
                        scaled_size = int(TILE_SIZE * 1.4)
                        scaled_sprite = pygame.transform.scale(explosion_sprite, (scaled_size, scaled_size))
                        
                        # Center the scaled sprite on the tile
                        offset_x = (TILE_SIZE - scaled_size) // 2
                        offset_y = (TILE_SIZE - scaled_size) // 2
                        render_x = x * TILE_SIZE + offset_x
                        render_y = y * TILE_SIZE + offset_y
                        
                        screen.blit(scaled_sprite, (render_x, render_y))
                    else:
                        # Fallback explosion - centered circle
                        center_x = x * TILE_SIZE + TILE_SIZE // 2
                        center_y = y * TILE_SIZE + TILE_SIZE // 2
                        radius = int(TILE_SIZE * 0.7)  # 70% of tile size
                        pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), radius) 