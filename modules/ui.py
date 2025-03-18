import pygame
from typing import List, Tuple

class UI:
    """Handles all UI and rendering functionality for the game."""
    
    def __init__(self, screen: pygame.Surface, cell_size: int):
        """Initialize the UI with the pygame screen and cell size."""
        self.screen = screen
        self.cell_size = cell_size
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render_game(self, grid: List[List[int]], player, ghosts: List, debug_mode: bool = False) -> None:
        """Main rendering method that draws everything in the game."""
        self.screen.fill((0, 0, 0))  # Clear screen
        self._draw_grid(grid)
        self._draw_entities(player, ghosts)
        self._draw_score(player.score)
        if debug_mode:
            self._draw_debug_info(ghosts)
        pygame.display.flip()
    
    def _draw_grid(self, grid: List[List[int]]) -> None:
        """Draw the game grid with walls and dots."""
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x = j * self.cell_size
                y = i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                if grid[i][j] == 1:  # Wall
                    pygame.draw.rect(self.screen, (51, 51, 51), rect)
                elif grid[i][j] == 2:  # Point
                    dot_size = self.cell_size // 4
                    dot_pos = (x + self.cell_size//2, y + self.cell_size//2)
                    pygame.draw.circle(self.screen, (255, 255, 0), dot_pos, dot_size)
    
    def _draw_entities(self, player, ghosts: List) -> None:
        """Draw player and ghosts using their draw methods."""
        # Draw player 
        player.draw(self.screen, self.cell_size)
        
        # Draw ghosts
        for ghost in ghosts:
            ghost.draw(self.screen, self.cell_size)
    
    def _draw_score(self, score: int) -> None:
        """Display the current score on screen."""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
    
    def _draw_debug_info(self, ghosts: List) -> None:
        """Draw debug information like ghost paths."""
        for ghost in ghosts:
            if ghost.path:
                points = [(p[1] * self.cell_size + self.cell_size//2,
                         p[0] * self.cell_size + self.cell_size//2)
                        for p in ghost.path[ghost.path_index:]]
                if len(points) > 1:
                    pygame.draw.lines(self.screen, ghost.color, False, points, 2)
        
        font = pygame.font.Font(None, 36)
        debug_text = font.render(f"Debug Mode: ON (F3)", True, (255, 255, 255))
        self.screen.blit(debug_text, (10, self.height - 30))
