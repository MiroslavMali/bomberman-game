import pygame
from settings import *

class PauseMenu:
    def __init__(self, display_surface, game_state_manager):
        self.display_surface = display_surface
        self.game_state_manager = game_state_manager
        
        # Font setup
        self.font = pygame.font.Font(None, FONT_SIZE * 2)
        self.small_font = pygame.font.Font(None, FONT_SIZE)
        
        # Menu options
        self.options = ['Resume', 'Quit to Menu']
        self.selected_option = 0
        
        # Colors
        self.title_color = WHITE
        self.option_color = WHITE
        self.selected_color = GREEN

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()
                elif event.key == pygame.K_ESCAPE:
                    self.game_state_manager.set_state('level')

    def select_option(self):
        if self.selected_option == 0:  # Resume
            self.game_state_manager.set_state('level')
        elif self.selected_option == 1:  # Quit to Menu
            self.game_state_manager.set_state('main_menu')

    def run(self, events):
        self.handle_input(events)
        self.draw()

    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.display_surface.blit(overlay, (0, 0))
        
        # Draw title
        title_text = self.font.render('PAUSED', True, self.title_color)
        title_rect = title_text.get_rect(center=(DISPLAY_CENTER[0], DISPLAY_CENTER[1] - 100))
        self.display_surface.blit(title_text, title_rect)
        
        # Draw options
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.option_color
            text = self.small_font.render(option, True, color)
            rect = text.get_rect(center=(DISPLAY_CENTER[0], DISPLAY_CENTER[1] + i * 50))
            self.display_surface.blit(text, rect)
        
        # Draw instructions
        instructions = [
            'Use UP/DOWN arrows to navigate',
            'Press ENTER to select',
            'Press ESC to resume'
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            rect = text.get_rect(center=(DISPLAY_CENTER[0], DISPLAY_CENTER[1] + 200 + i * 30))
            self.display_surface.blit(text, rect) 