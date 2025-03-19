import pygame
from typing import Tuple, Optional
from modules.game_state import GameState
from modules.algorithms import astar_path
from modules.player import Player
from modules.ghost import Ghost
from modules.ui import UI

class PacmanGame:
    def __init__(self, cell_size: int = 30):
        pygame.init()
        self.cell_size = cell_size
        self.width = 23 * cell_size
        self.height = 25 * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pacman with AI Enemies")
        self.clock = pygame.time.Clock()
        self.state = GameState.create_new_game()
        self.ghost_move_delay = 0
        # Create player instance with initial position
        self.player = Player(self.state.player_pos)
        # Create UI handler
        self.ui = UI(self.screen, self.cell_size)
        
    def handle_input(self) -> bool:
        """Handle user input. Returns False if game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
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
