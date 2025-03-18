import pygame
from typing import Tuple, Optional
from modules.game_state import GameState
from modules.algorithms import astar_path
from modules.player import Player

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
        
    def handle_input(self) -> bool:
        """Handle user input. Returns False if game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self.state.debug_mode = not self.state.debug_mode
                else:
                    self.player.handle_key_input(event.key)
        return True
        
    def update(self) -> None:
        """Update game state."""
        # Update player position and collect dots
        self.player.update_position(self.state.grid)
        
        # Update game state with current player position and direction
        self.state.player_pos = self.player.pos
        self.state.player_direction = self.player.direction
        
        self.state.update()
        self._update_ghosts()
        
    def _update_ghosts(self) -> None:
        """Update ghost movement and pathfinding."""
        self.ghost_move_delay = (self.ghost_move_delay + 1) % 6
        if self.ghost_move_delay != 0:
            return
            
        for ghost in self.state.ghosts:
            if not ghost.active:
                continue
                
            # Always get new target and calculate new path
            blinky_pos = self.state.ghosts[0].pos if ghost.ghost_type != 'blinky' else None
            target = ghost.get_chase_target(
                tuple(self.state.player_pos),
                self.state.player_direction,
                blinky_pos
            )
            
            # Calculate new path every frame
            path = astar_path(self.state.grid, ghost.pos, target)
            if path and len(path) > 1:
                ghost.set_path(path)
            
            ghost.move_step()
            
    def render(self) -> None:
        """Render the game state to the screen."""
        self.screen.fill((0, 0, 0))
        self._draw_grid()
        self._draw_entities()
        self._draw_score()
        self._draw_debug_info()
        pygame.display.flip()
        
    def _draw_grid(self) -> None:
        """Draw the game grid."""
        for i in range(len(self.state.grid)):
            for j in range(len(self.state.grid[0])):
                x = j * self.cell_size
                y = i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                if self.state.grid[i][j] == 1:  # Wall
                    pygame.draw.rect(self.screen, (51, 51, 51), rect)
                elif self.state.grid[i][j] == 2:  # Point
                    dot_size = self.cell_size // 4
                    dot_pos = (x + self.cell_size//2, y + self.cell_size//2)
                    pygame.draw.circle(self.screen, (255, 255, 0), dot_pos, dot_size)
                    
    def _draw_entities(self) -> None:
        """Draw player and ghosts."""
        # Draw player using its own draw method
        self.player.draw(self.screen, self.cell_size)
        
        # Draw ghosts
        for ghost in self.state.ghosts:
            ghost.draw(self.screen, self.cell_size)
            
    def _draw_score(self) -> None:
        """Display the current score on screen."""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
    def _draw_debug_info(self) -> None:
        """Draw debug information if debug mode is enabled."""
        if not self.state.debug_mode:
            return
            
        for ghost in self.state.ghosts:
            if ghost.path:
                points = [(p[1] * self.cell_size + self.cell_size//2,
                          p[0] * self.cell_size + self.cell_size//2)
                         for p in ghost.path[ghost.path_index:]]
                if len(points) > 1:
                    pygame.draw.lines(self.screen, ghost.color, False, points, 2)
                    
        font = pygame.font.Font(None, 36)
        debug_text = font.render(f"Debug Mode: ON (F3)", True, (255, 255, 255))
        self.screen.blit(debug_text, (10, self.height - 30))
        
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
