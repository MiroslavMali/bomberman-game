"""
Map Manager - Handles the game map layout and collision detection
"""

import pygame
from config import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT

class MapManager:
    def __init__(self, sprite_manager):
        self.sprite_manager = sprite_manager
        self.map_data = []
        self.create_map()
    
    def create_map(self):
        """Create the fixed map layout"""
        # Initialize empty map
        self.map_data = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Create outer walls
        for x in range(GRID_WIDTH):
            self.map_data[0][x] = 1  # Top wall
            self.map_data[GRID_HEIGHT-1][x] = 1  # Bottom wall
        
        for y in range(GRID_HEIGHT):
            self.map_data[y][0] = 1  # Left wall
            self.map_data[y][GRID_WIDTH-1] = 1  # Right wall
        
        # Create internal maze structure (fixed layout)
        # This creates a simple maze pattern
        maze_pattern = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Apply maze pattern to map (centered)
        start_y = (GRID_HEIGHT - len(maze_pattern)) // 2
        start_x = (GRID_WIDTH - len(maze_pattern[0])) // 2
        
        for y, row in enumerate(maze_pattern):
            for x, tile in enumerate(row):
                if (start_y + y < GRID_HEIGHT and start_x + x < GRID_WIDTH):
                    self.map_data[start_y + y][start_x + x] = tile
        
        # Add some breakable bricks randomly in open areas
        self.add_breakable_bricks()
    
    def add_breakable_bricks(self):
        """Add breakable bricks to open areas"""
        import random
        
        for y in range(1, GRID_HEIGHT - 1):
            for x in range(1, GRID_WIDTH - 1):
                # Only place bricks in grass areas (0)
                if self.map_data[y][x] == 0:
                    # 30% chance to place a breakable brick
                    if random.random() < 0.3:
                        # Don't place bricks in player starting areas
                        if not self.is_player_start_area(x, y):
                            self.map_data[y][x] = 2  # 2 = breakable brick
    
    def is_player_start_area(self, x, y):
        """Check if position is in a player starting area"""
        # Define player starting areas (corners)
        start_areas = [
            (1, 1), (2, 1), (1, 2), (2, 2),  # Top-left
            (GRID_WIDTH-3, 1), (GRID_WIDTH-2, 1), (GRID_WIDTH-3, 2), (GRID_WIDTH-2, 2),  # Top-right
            (1, GRID_HEIGHT-3), (2, GRID_HEIGHT-3), (1, GRID_HEIGHT-2), (2, GRID_HEIGHT-2),  # Bottom-left
            (GRID_WIDTH-3, GRID_HEIGHT-3), (GRID_WIDTH-2, GRID_HEIGHT-3), (GRID_WIDTH-3, GRID_HEIGHT-2), (GRID_WIDTH-2, GRID_HEIGHT-2)  # Bottom-right
        ]
        return (x, y) in start_areas
    
    def get_tile_type(self, x, y):
        """Get tile type at position"""
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.map_data[y][x]
        return 1  # Wall if out of bounds
    
    def is_walkable(self, x, y):
        """Check if position is walkable"""
        tile_type = self.get_tile_type(x, y)
        return tile_type == 0  # Only grass is walkable
    
    def destroy_brick(self, x, y):
        """Destroy a breakable brick"""
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            if self.map_data[y][x] == 2:  # Breakable brick
                self.map_data[y][x] = 0  # Convert to grass
                return True
        return False
    
    def render(self, screen):
        """Render the map"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                tile_type = self.map_data[y][x]
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                
                if tile_type == 0:  # Grass
                    screen.blit(self.sprite_manager.get_sprite('grass'), pos)
                elif tile_type == 1:  # Wall
                    screen.blit(self.sprite_manager.get_sprite('wall'), pos)
                elif tile_type == 2:  # Breakable brick
                    screen.blit(self.sprite_manager.get_sprite('brick'), pos) 