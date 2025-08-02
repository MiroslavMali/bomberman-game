# Game Configuration
WIDTH = 800
HEIGHT = 600
FPS = 60

# Debug Configuration
DEBUG_COLLISION = False  # Set to True to see collision boxes

# Tile Configuration
TILE_SIZE = 32
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

# Player Configuration
PLAYER_SIZE = 28
PLAYER_SPEED = 3

# Bomb Configuration
BOMB_TIMER = 3000  # milliseconds
EXPLOSION_DURATION = 500  # milliseconds
EXPLOSION_RANGE = 2  # tiles

# Network Configuration
PORT = 65432
HOST = None  # Will be set dynamically

# Colors
BACKGROUND_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game Window
WINDOW_TITLE = "Bomberman Game" 