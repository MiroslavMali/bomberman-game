import math

# Display settings
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 960
DISPLAY_CENTER = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
FONT_SIZE = 28

# Game settings
TILE_SIZE = 64
GRID_WIDTH = 20
GRID_HEIGHT = 15
PLAYER_SPEED = 5  # Back to original speed
PLAYER_SIZE = 56  # Slightly smaller than tile for visual clarity
BOMB_TIMER = 3000  # milliseconds
EXPLOSION_DURATION = 500  # milliseconds
EXPLOSION_RANGE = 2  # tiles

# Movement factors
DIAGONAL_SPEED_FACTOR = math.sqrt(2) / 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) 