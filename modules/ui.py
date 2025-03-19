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
    
    def render_game(self, grid: List[List[int]], player, ghosts: List, debug_mode: bool = False, 
                    game_over: bool = False, lives: int = 3, dying: bool = False, death_timer: int = 0,
                    death_animation_length: int = 90) -> None:
        """Main rendering method that draws everything in the game."""
        self.screen.fill((0, 0, 0))  # Clear screen
        self._draw_grid(grid)
        
        # Draw ghosts below player if player is dying
        if dying:
            for ghost in ghosts:
                ghost.draw(self.screen, self.cell_size)
            # Calculate death animation progress (0 to 1)
            death_progress = death_timer / death_animation_length
            player.draw(self.screen, self.cell_size, dying=True, death_progress=death_progress)
        else:
            self._draw_entities(player, ghosts)
            
        self._draw_score(player.score)
        self._draw_lives(lives)
        
        if debug_mode:
            self._draw_debug_info(ghosts)
            
        # Only show game over overlay after death animation is finished
        if game_over and not dying:
            self._draw_game_over()
            
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
    
    def _draw_lives(self, lives: int) -> None:
        """Display the number of remaining lives."""
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (self.width - 150, 10))
    
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
    
    def _draw_game_over(self) -> None:
        """Display game over message."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        
        # Instructions text
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
