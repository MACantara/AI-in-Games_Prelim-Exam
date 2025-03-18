import pygame
from typing import Tuple, List

class Player:
    """Represents the player character (Pacman) in the game."""
    
    def __init__(self, pos: List[int]):
        """Initialize player with a position."""
        self.pos = pos  # [row, col]
        self.direction = (0, 0)  # (dx, dy)
        self.requested_direction = (0, 0)  # Direction player wants to go
        self.move_delay = 0
        self.move_speed = 5
        self.score = 0
        self.dot_points = 10
        self.power_pellet_points = 50
        
    def handle_key_input(self, key: int) -> None:
        """Handle keyboard input for player direction changes."""
        # Store the requested direction but don't change actual direction yet
        if key in (pygame.K_UP, pygame.K_w):
            self.requested_direction = (-1, 0)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.requested_direction = (1, 0)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.requested_direction = (0, -1)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.requested_direction = (0, 1)
    
    def update_position(self, grid: List[List[int]]) -> None:
        """Update player position based on current direction."""
        # Control movement speed
        self.move_delay = (self.move_delay + 1) % self.move_speed
        if self.move_delay != 0:
            return
        
        # First, try to move in the requested direction if different from current
        if self.requested_direction != self.direction:
            requested_pos = [
                self.pos[0] + self.requested_direction[0],
                self.pos[1] + self.requested_direction[1]
            ]
            
            if self._can_move_to(tuple(requested_pos), grid):
                # Switch to the requested direction
                self.direction = self.requested_direction
                self._move_and_collect_dot(requested_pos, grid)
                return
        
        # If we can't move in the requested direction, try to continue in current direction
        current_pos = [
            self.pos[0] + self.direction[0],
            self.pos[1] + self.direction[1]
        ]
        
        if self._can_move_to(tuple(current_pos), grid):
            self._move_and_collect_dot(current_pos, grid)
    
    def _move_and_collect_dot(self, new_pos: List[int], grid: List[List[int]]) -> None:
        """Move to the new position and collect a dot if present."""
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
