import pygame
import os
from typing import Tuple, Optional
from modules.game_state import GameState
from modules.algorithms import astar_path
from modules.player import Player
from modules.ghost import Ghost
from modules.ui import UI

class PacmanGame:
    def __init__(self, cell_size: int = 30):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer for audio
        self.cell_size = cell_size
        self.width = 23 * cell_size
        self.height = 25 * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pacman with AI Enemies")
        self.clock = pygame.time.Clock()
        
        # Game states
        self.in_startup = True
        self.state = None
        self.ghost_move_delay = 0
        self.player = None
        self.ui = UI(self.screen, self.cell_size)
        
        # Load and play startup music
        self.startup_music_path = os.path.join(os.path.dirname(__file__), "static/audio/start-up.mp3")
        if os.path.exists(self.startup_music_path):
            pygame.mixer.music.load(self.startup_music_path)
            pygame.mixer.music.play()
        else:
            print(f"Warning: Could not find startup music at {self.startup_music_path}")
            self.in_startup = False  # Skip startup if music file doesn't exist
            self._init_game()
    
    def _init_game(self):
        """Initialize the game state and player."""
        self.state = GameState.create_new_game()
        self.player = Player(self.state.player_pos)
        self.ghost_move_delay = 0

    def handle_input(self) -> bool:
        """Handle user input. Returns False if game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.in_startup:
                # Only check if music has ended, ignore key presses during startup
                if not pygame.mixer.music.get_busy():
                    self.in_startup = False
                    self._init_game()
                # Ignore keypresses during startup
            else:
                # Regular game input handling
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        self.state.debug_mode = not self.state.debug_mode
                    elif event.key == pygame.K_r and self.state.game_over:
                        self._restart_game()
                    elif not self.state.game_over:
                        self.player.handle_key_input(event.key)
        return True
    
    def _restart_game(self) -> None:
        """Restart the game after game over."""
        self.state = GameState.create_new_game()
        self.player = Player(self.state.player_pos)
        self.ghost_move_delay = 0
        
    def update(self) -> None:
        """Update game state."""
        if self.in_startup:
            # Check if startup music has finished
            if not pygame.mixer.music.get_busy():
                self.in_startup = False
                self._init_game()
            return
        
        # Update player position and collect dots
        self.player.update_position(self.state.grid, self.state.dying)
        
        # Update game state with current player position and direction
        self.state.player_pos = self.player.pos
        self.state.player_direction = self.player.direction
        
        # Update ghost positions
        self.ghost_move_delay = (self.ghost_move_delay + 1) % 6
        if self.ghost_move_delay == 0:
            Ghost.update_all_ghosts(
                self.state.ghosts, 
                self.state.grid,
                tuple(self.state.player_pos),
                self.state.player_direction
            )
        
        self.state.update()
        
    def render(self) -> None:
        """Render the game state using the UI handler."""
        if self.in_startup:
            self._draw_startup_screen()
        else:
            self.ui.render_game(
                self.state.grid,
                self.player,
                self.state.ghosts,
                self.state.debug_mode,
                self.state.game_over,
                self.state.lives,
                self.state.dying,
                self.state.death_timer,
                self.state.death_animation_length
            )
    
    def _draw_startup_screen(self) -> None:
        """Draw the game grid and entities while startup music plays."""
        # If game state isn't initialized yet, create it temporarily for drawing
        if not self.state:
            temp_state = GameState.create_new_game()
            temp_player = Player(temp_state.player_pos)
            # Draw the game grid and entities
            self.ui.render_game(
                temp_state.grid,
                temp_player,
                temp_state.ghosts,
                debug_mode=False,
                game_over=False,
                lives=3,
                dying=False,
                death_timer=0,
                death_animation_length=90
            )
        else:
            # Use existing state if available
            self.ui.render_game(
                self.state.grid,
                self.player,
                self.state.ghosts,
                self.state.debug_mode,
                self.state.game_over,
                self.state.lives,
                self.state.dying,
                self.state.death_timer,
                self.state.death_animation_length
            )
        
    def run(self) -> None:
        """Main game loop."""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.render()
            self.clock.tick(30)
        pygame.quit()

if __name__ == '__main__':
    game = PacmanGame()
    game.run()
