# Bomberman Game

A classic Bomberman game built with Python and Pygame, featuring clean modular architecture.

## 🎮 Features

- **Clean State Management** - Menu, game, and pause states
- **Modular Architecture** - Separated concerns for easy maintenance
- **Player Movement** - WASD/Arrow keys with collision detection
- **Bomb System** - Place bombs with spacebar, animated explosions
- **Map System** - Procedurally generated maps with breakable bricks
- **Sprite Management** - All game assets properly loaded and scaled

## 🏗️ Project Structure

```
bomberman-game/
├── main.py                 # Main entry point with state management
├── settings.py             # Game configuration constants
├── game_state_manager.py   # State transitions (menu/game/pause)
├── main_menu.py           # Main menu with navigation
├── pause_menu.py          # Pause overlay menu
├── level.py               # Main game logic and rendering
├── game/                  # Game components
│   ├── player.py          # Player movement and bomb placement
│   ├── bomb.py            # Bomb logic and explosion system
│   ├── map_manager.py     # Map generation and collision
│   └── sprite_manager.py  # Asset loading and management
├── images/                # Game sprites and assets
└── requirements.txt       # Python dependencies
```

## 🚀 Installation & Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the game:**
   ```bash
   python main.py
   ```

## 🎯 Controls

- **WASD/Arrow Keys** - Move player
- **Spacebar** - Place bomb
- **ESC** - Pause game
- **Enter** - Select menu options

## 🎨 Architecture Benefits

- **Clean Separation** - UI, game logic, and state management separated
- **Easy to Extend** - Add new states, features, or multiplayer
- **Maintainable** - Each component has a single responsibility
- **Professional Structure** - Follows software engineering best practices

## 🔧 Development

The game uses a state-based architecture similar to professional game engines:
- **State Manager** handles transitions between menu/game/pause
- **Level Class** contains all game logic and rendering
- **Modular Components** for player, bombs, map, and sprites
- **Centralized Settings** for easy configuration

Perfect foundation for adding multiplayer networking, power-ups, and more features! 