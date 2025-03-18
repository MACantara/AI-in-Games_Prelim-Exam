import pygame
import math
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
        
        # Simplified animation properties - just alternating between open and closed
        self.mouth_open = True  # Start with open mouth
        self.animation_counter = 0
        self.animation_speed = 5  # Lower = faster animation
        
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
        # Update mouth animation every frame for smoother animation
        self._update_animation()
        
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
    
    def _update_animation(self) -> None:
        """Update the mouth animation state - simple open/close toggle."""
        self.animation_counter = (self.animation_counter + 1) % self.animation_speed
        
        # Only change state when counter resets
        if self.animation_counter == 0:
            self.mouth_open = not self.mouth_open
    
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
        """Draw the player (Pacman) with animated mouth."""
        # Calculate center point and radius
        center_x = self.pos[1] * cell_size + cell_size // 2
        center_y = self.pos[0] * cell_size + cell_size // 2
        radius = cell_size // 2 - 1  # Slightly smaller for better visibility
        
        # Calculate mouth angles based on direction
        # Default to right if not moving
        facing_direction = self.direction if self.direction != (0, 0) else (0, 1)
        
        angle_offset = 0
        if facing_direction == (0, -1):  # Left
            angle_offset = 180
        elif facing_direction == (-1, 0):  # Up
            angle_offset = 270
        elif facing_direction == (1, 0):  # Down
            angle_offset = 90
        # Right is default (offset = 0)
        
        # Set fixed mouth angles based on animation state
        if self.mouth_open:
            # Open mouth - draw partial circle (45 degree angle)
            start_angle = angle_offset - 45
            end_angle = angle_offset + 45
            
            # Draw the pac-man using pygame's arc function for precision
            # Fill a full circle with black first
            pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)
            
            # Draw yellow arc (Pac-Man body)
            # Convert angles to radians for pygame
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Create a rectangle that bounds the circle
            rect = pygame.Rect(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2
            )
            
            # Draw the arc as a semi-circle with the mouth cutout
            # We need to draw the arc and then connect it to center for the pie shape
            points = [(center_x, center_y)]  # Start at center
            
            # Add points around the arc
            num_points = 20  # Number of points for a smooth circle
            for i in range(num_points + 1):
                angle_rad = end_rad + (start_rad - end_rad + 2*math.pi) % (2*math.pi) * i / num_points
                x = center_x + radius * math.cos(angle_rad)
                y = center_y + radius * math.sin(angle_rad)
                points.append((x, y))
            
            # Close the shape
            points.append((center_x, center_y))
            
            # Draw the full shape
            pygame.draw.polygon(screen, (255, 255, 0), points)
        else:
            # Closed mouth - just a full yellow circle
            pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), radius)
