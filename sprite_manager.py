"""
Sprite Manager - Handles loading and managing all game sprites
"""

import pygame
import os
from settings import TILE_SIZE

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.load_sprites()
    
    def load_sprites(self):
        """Load all sprites from the images folder"""
        images_path = "images"
        
        # Load tile sprites
        self.sprites['grass'] = self.load_sprite(os.path.join(images_path, "grass_tile.png"))
        self.sprites['wall'] = self.load_sprite(os.path.join(images_path, "wall_tile.png"))
        self.sprites['brick'] = self.load_sprite(os.path.join(images_path, "brick_tile.png"))
        
        # Load player sprite
        self.sprites['player'] = self.load_sprite(os.path.join(images_path, "player_sprite.png"))
        
        # Load bomb sprites (animation frames)
        self.sprites['bomb'] = [
            self.load_sprite(os.path.join(images_path, "bomb_sprite.png")),
            self.load_sprite(os.path.join(images_path, "bomb_sprite_1.png")),
            self.load_sprite(os.path.join(images_path, "bomb_sprite_2.png"))
        ]
        
        # Load explosion sprites (animation frames)
        self.sprites['explosion'] = [
            self.load_sprite(os.path.join(images_path, "explosion_1.png")),
            self.load_sprite(os.path.join(images_path, "explosion_2.png")),
            self.load_sprite(os.path.join(images_path, "explosion_3.png"))
        ]
    
    def load_sprite(self, path):
        """Load and scale a sprite"""
        try:
            sprite = pygame.image.load(path).convert_alpha()
            # Scale to tile size if it's a tile sprite
            if 'tile' in path or 'sprite' in path:
                sprite = pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            return sprite
        except pygame.error as e:
            print(f"Error loading sprite {path}: {e}")
            # Return a colored rectangle as fallback
            surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surface.fill((255, 0, 255))  # Magenta for missing sprites
            return surface
    
    def get_sprite(self, name):
        """Get a sprite by name"""
        return self.sprites.get(name)
    
    def get_bomb_frame(self, frame_index):
        """Get a specific bomb animation frame"""
        if 'bomb' in self.sprites and frame_index < len(self.sprites['bomb']):
            return self.sprites['bomb'][frame_index]
        return self.sprites.get('bomb', [None])[0]
    
    def get_explosion_frame(self, frame_index):
        """Get a specific explosion animation frame"""
        if 'explosion' in self.sprites and frame_index < len(self.sprites['explosion']):
            return self.sprites['explosion'][frame_index]
        return self.sprites.get('explosion', [None])[0] 