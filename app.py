import pygame
from typing import Tuple, Optional
from modules.game_state import GameState
from modules.algorithms import astar_path

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
        
    def handle_input(self) -> bool:
        """Handle user input. Returns False if game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)
        return True
        
    def _handle_keypress(self, key: int) -> None:
        """Handle keyboard input for player movement and debug mode."""
        if key == pygame.K_F3:
            self.state.debug_mode = not self.state.debug_mode
            return
            
        new_pos = self.state.player_pos.copy()
        new_direction = self.state.player_direction
        
        if key in (pygame.K_UP, pygame.K_w):
            new_pos[0] -= 1
            new_direction = (-1, 0)
        elif key in (pygame.K_DOWN, pygame.K_s):
            new_pos[0] += 1
            new_direction = (1, 0)
        elif key in (pygame.K_LEFT, pygame.K_a):
            new_pos[1] -= 1
            new_direction = (0, -1)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            new_pos[1] += 1
            new_direction = (0, 1)
            
        if self._can_move_to(tuple(new_pos)):
            self.state.player_pos = new_pos
            self.state.player_direction = new_direction
            
    def _can_move_to(self, pos: Tuple[int, int]) -> bool:
        """Check if movement to position is valid, handling tunnel wraparound."""
        i, j = pos
        if i == 11:  # Tunnel row
            if j < 0:
                self.state.player_pos[1] = len(self.state.grid[0]) - 2
                return True
            if j >= len(self.state.grid[0]):
                self.state.player_pos[1] = 0
                return True
        return (0 <= i < len(self.state.grid) and 
                0 <= j < len(self.state.grid[0]) and 
                self.state.grid[i][j] != 1)
                
    def update(self) -> None:
        """Update game state."""
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
                
            blinky_pos = self.state.ghosts[0].pos if ghost.ghost_type != 'blinky' else None
            target = ghost.get_chase_target(
                tuple(self.state.player_pos),
                self.state.player_direction,
                blinky_pos
            )
            
            if not ghost.path or ghost.path_index >= len(ghost.path) - 1:
                path = astar_path(self.state.grid, ghost.pos, target)
                if path and len(path) > 1:
                    ghost.set_path(path)
            
            ghost.move_step()
            
    def render(self) -> None:
        """Render the game state to the screen."""
        self.screen.fill((0, 0, 0))
        self._draw_grid()
        self._draw_entities()
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
        # Draw player
        player_rect = pygame.Rect(
            self.state.player_pos[1] * self.cell_size,
            self.state.player_pos[0] * self.cell_size,
            self.cell_size, self.cell_size
        )
        pygame.draw.ellipse(self.screen, (255, 255, 0), player_rect)
        
        # Draw ghosts
        for ghost in self.state.ghosts:
            ghost_rect = pygame.Rect(
                ghost.pos[1] * self.cell_size,
                ghost.pos[0] * self.cell_size,
                self.cell_size, self.cell_size
            )
            pygame.draw.ellipse(self.screen, ghost.color, ghost_rect)
            
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
