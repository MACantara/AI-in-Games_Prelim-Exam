import pygame
from typing import Tuple, List

class Player:
    """Represents the player character (Pacman) in the game."""
    
    def __init__(self, pos: List[int]):
        """Initialize player with a position."""
        self.pos = pos  # [row, col]
        self.direction = (0, 0)  # (dx, dy)
        self.move_delay = 0
        self.move_speed = 5
        self.score = 0
        self.dot_points = 10
        self.power_pellet_points = 50
        
    def handle_key_input(self, key: int) -> None:
        """Handle keyboard input for player direction changes."""
        if key in (pygame.K_UP, pygame.K_w):
            self.direction = (-1, 0)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.direction = (1, 0)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.direction = (0, -1)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.direction = (0, 1)
    
    def update_position(self, grid: List[List[int]]) -> None:
        """Update player position based on current direction."""
        # Control movement speed
        self.move_delay = (self.move_delay + 1) % self.move_speed
        if self.move_delay != 0:
            return
            
        # Calculate new position based on current direction
        new_pos = self.pos.copy()
        dx, dy = self.direction
        new_pos[0] += dx
        new_pos[1] += dy
        
        # Try to move in the current direction
        if self._can_move_to(tuple(new_pos), grid):
            # Check if player is collecting a dot
            row, col = new_pos
            if grid[row][col] == 2:  # If it's a dot
                grid[row][col] = 0  # Remove the dot
                self.score += self.dot_points  # Increase score
                
            self.pos = new_pos
    
    def _can_move_to(self, pos: Tuple[int, int], grid: List[List[int]]) -> bool:
        """Check if movement to position is valid, handling tunnel wraparound."""
        i, j = pos
        if i == 11:  # Tunnel row
            if j < 0:
                self.pos[1] = len(grid[0]) - 2
                return True
            if j >= len(grid[0]):
                self.pos[1] = 0
                return True
        return (0 <= i < len(grid) and 
                0 <= j < len(grid[0]) and 
                grid[i][j] != 1)
    
    def draw(self, screen, cell_size: int) -> None:
        """Draw the player (Pacman)."""
        player_rect = pygame.Rect(
            self.pos[1] * cell_size,
            self.pos[0] * cell_size,
            cell_size, cell_size
        )
        pygame.draw.ellipse(screen, (255, 255, 0), player_rect)
