import pygame
from typing import Tuple, Optional
from dataclasses import dataclass
from .agent import PathAgent

Position = Tuple[int, int]
Color = Tuple[int, int, int]

@dataclass
class GhostConfig:
    color: Color
    scatter_target: Position

GHOST_CONFIGS = {
    'blinky': GhostConfig((255, 0, 0), (1, 23)),     # Red, Upper-right
    'pinky': GhostConfig((255, 182, 255), (1, 1)),   # Pink, Upper-left
    'inky': GhostConfig((0, 255, 255), (23, 23)),    # Cyan, Lower-right
    'clyde': GhostConfig((255, 182, 85), (23, 1))    # Orange, Lower-left
}

class Ghost(PathAgent):
    """Represents a ghost enemy in the game with specific behavior patterns."""
    
    def __init__(self, pos: Position, ghost_type: str):
        """Initialize ghost with position and type-specific attributes."""
        super().__init__(pos)
        if ghost_type not in GHOST_CONFIGS:
            raise ValueError(f"Invalid ghost type: {ghost_type}")
            
        self.ghost_type = ghost_type
        config = GHOST_CONFIGS[ghost_type]
        self.color = config.color
        self.scatter_target = config.scatter_target
        self.scatter_mode = False
        self.active = False

    def get_chase_target(self, player_pos: Position, player_direction: Position, 
                        blinky_pos: Optional[Position] = None) -> Position:
        """Calculate target position based on ghost type and game state."""
        if self.scatter_mode:
            return self.scatter_target

        if self.ghost_type == 'blinky':
            return player_pos

        if self.ghost_type == 'pinky':
            return self._get_pinky_target(player_pos, player_direction)

        if self.ghost_type == 'inky' and blinky_pos:
            return self._get_inky_target(player_pos, player_direction, blinky_pos)

        if self.ghost_type == 'clyde':
            return self._get_clyde_target(player_pos)

        return player_pos

    def _get_pinky_target(self, player_pos: Position, player_direction: Position) -> Position:
        """Calculate Pinky's target (4 tiles ahead of player)."""
        target_x = player_pos[0] + (4 * player_direction[0])
        target_y = player_pos[1] + (4 * player_direction[1])
        # Reproduce the original game's bug when Pac-Man faces up
        if player_direction == (-1, 0):
            target_y -= 4
        return (target_x, target_y)

    def _get_inky_target(self, player_pos: Position, player_direction: Position, 
                        blinky_pos: Position) -> Position:
        """Calculate Inky's target (based on Blinky's position)."""
        intermediate_x = player_pos[0] + (2 * player_direction[0])
        intermediate_y = player_pos[1] + (2 * player_direction[1])
        vector_x = intermediate_x - blinky_pos[0]
        vector_y = intermediate_y - blinky_pos[1]
        return (intermediate_x + vector_x, intermediate_y + vector_y)

    def _get_clyde_target(self, player_pos: Position) -> Position:
        """Calculate Clyde's target (switches between chase and scatter)."""
        distance = ((player_pos[0] - self.pos[0])**2 + 
                   (player_pos[1] - self.pos[1])**2)**0.5
        return self.scatter_target if distance < 8 else player_pos

    def draw(self, screen, cell_size: int) -> None:
        """Draw the ghost with direction-indicating eyes."""
        # Draw ghost body
        ghost_rect = pygame.Rect(
            self.pos[1] * cell_size,
            self.pos[0] * cell_size,
            cell_size, cell_size
        )
        pygame.draw.ellipse(screen, self.color, ghost_rect)
        
        # Calculate eye positions
        eye_radius = cell_size // 5
        left_eye_pos = (
            self.pos[1] * cell_size + cell_size // 3,
            self.pos[0] * cell_size + cell_size // 3
        )
        right_eye_pos = (
            self.pos[1] * cell_size + cell_size * 2 // 3,
            self.pos[0] * cell_size + cell_size // 3
        )
        
        # Draw eyes (white circles)
        pygame.draw.circle(screen, (255, 255, 255), left_eye_pos, eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), right_eye_pos, eye_radius)
        
        # Determine pupil positions based on current direction
        direction = (0, 0)
        if self.path and len(self.path) > self.path_index + 1:
            next_pos = self.path[self.path_index + 1]
            direction = (next_pos[0] - self.pos[0], next_pos[1] - self.pos[1])
        
        # Calculate pupil offset based on direction
        pupil_offset_x = 0
        pupil_offset_y = 0
        
        if direction[0] < 0:  # Moving up
            pupil_offset_y = -eye_radius // 2
        elif direction[0] > 0:  # Moving down
            pupil_offset_y = eye_radius // 2
        elif direction[1] < 0:  # Moving left
            pupil_offset_x = -eye_radius // 2
        elif direction[1] > 0:  # Moving right
            pupil_offset_x = eye_radius // 2
        
        # Draw pupils (blue circles)
        pupil_radius = eye_radius // 2
        pygame.draw.circle(screen, (0, 0, 255), 
                         (left_eye_pos[0] + pupil_offset_x, 
                          left_eye_pos[1] + pupil_offset_y), 
                         pupil_radius)
        pygame.draw.circle(screen, (0, 0, 255), 
                         (right_eye_pos[0] + pupil_offset_x, 
                          right_eye_pos[1] + pupil_offset_y), 
                         pupil_radius)
