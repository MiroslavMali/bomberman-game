#!/usr/bin/env python3
"""
Bomberman Game - Main Entry Point
A classic multiplayer Bomberman game built with Python and Pygame
"""

from game.game_engine import GameEngine

def main():
    """Main game entry point"""
    game = GameEngine()
    game.run()

if __name__ == "__main__":
    main() 