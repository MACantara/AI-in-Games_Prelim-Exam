import pygame
import math
from typing import Tuple, Optional, List
from dataclasses import dataclass
from .agent import PathAgent
from .algorithms import astar_path

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
        # Animation counter for the wavy bottom
        self.wave_animation_counter = 0

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
        """Draw the ghost with direction-indicating eyes and wavy bottom."""
        # Update animation counter
        self.wave_animation_counter = (self.wave_animation_counter + 0.2) % (2 * math.pi)
        
        # Basic dimensions
        x = self.pos[1] * cell_size
        y = self.pos[0] * cell_size
        
        # Create a single polygon for the entire ghost body
        ghost_points = []
        
        # Add points for the semi-circular top
        num_arc_points = 10  # More points for smoother top arc
        for i in range(num_arc_points + 1):
            angle = math.pi * i / num_arc_points
            arc_x = x + cell_size/2 - (cell_size/2) * math.cos(angle)
            arc_y = y + cell_size/2 - (cell_size/2) * math.sin(angle)
            ghost_points.append((arc_x, arc_y))
            
        # Right edge down to where waves start
        ghost_points.append((x + cell_size, y + 3*cell_size//4))
        
        # Create smooth wavy bottom
        bottom_y = y + 3.5*cell_size//4
        num_waves = 5
        points_per_wave = 4  # More points per wave for smoothness
        
        # Generate the waves from right to left
        for i in range(num_waves * points_per_wave):
            t = i / (num_waves * points_per_wave)  # Position along bottom (0 to 1)
            wave_x = x + cell_size - t * cell_size
            
            # Use smoother sine function with offset for alternating waves
            wave_freq = 5  # Number of complete waves
            wave_height = cell_size // 24  # Less height for gentler waves
            
            # Calculate wave height with smooth animation
            offset = math.sin(self.wave_animation_counter) * (wave_height / 3)
            wave_y = bottom_y + math.sin(wave_freq * math.pi * t + self.wave_animation_counter) * wave_height + offset
            
            ghost_points.append((wave_x, wave_y))
            
        # Left edge back up to complete the shape
        ghost_points.append((x, y + 3*cell_size//4))
        ghost_points.append(ghost_points[0])  # Close the shape
        
        # Draw the ghost as a single polygon
        pygame.draw.polygon(screen, self.color, ghost_points)
        
        # Draw eyes as perfect circles
        eye_size = cell_size // 7
        
        # Left eye position - more centered horizontally
        left_eye_center = (
            self.pos[1] * cell_size + cell_size // 3,
            self.pos[0] * cell_size + cell_size // 3
        )
        
        # Right eye position - more centered horizontally
        right_eye_center = (
            self.pos[1] * cell_size + cell_size * 2 // 3,
            self.pos[0] * cell_size + cell_size // 3
        )
        
        # Draw white part of eyes
        pygame.draw.circle(screen, (255, 255, 255), left_eye_center, eye_size)
        pygame.draw.circle(screen, (255, 255, 255), right_eye_center, eye_size)
        
        # Determine pupil direction
        direction = (0, 0)
        if self.path and len(self.path) > self.path_index + 1:
            next_pos = self.path[self.path_index + 1]
            direction = (next_pos[0] - self.pos[0], next_pos[1] - self.pos[1])
        
        # Calculate pupil offset based on direction
        pupil_offset_x = 0
        pupil_offset_y = 0
        pupil_move_distance = eye_size // 2
        
        if direction[0] < 0:  # Moving up
            pupil_offset_y = -pupil_move_distance
        elif direction[0] > 0:  # Moving down
            pupil_offset_y = pupil_move_distance
        elif direction[1] < 0:  # Moving left
            pupil_offset_x = -pupil_move_distance
        elif direction[1] > 0:  # Moving right
            pupil_offset_x = pupil_move_distance
        
        # Draw pupils as smaller circles
        pupil_size = eye_size // 2
        pygame.draw.circle(screen, (0, 0, 255), 
                         (left_eye_center[0] + pupil_offset_x, 
                          left_eye_center[1] + pupil_offset_y), 
                         pupil_size)
        pygame.draw.circle(screen, (0, 0, 255), 
                         (right_eye_center[0] + pupil_offset_x, 
                          right_eye_center[1] + pupil_offset_y), 
                         pupil_size)

    @classmethod
    def update_all_ghosts(cls, ghosts: List['Ghost'], grid: List[List[int]], 
                          player_pos: Tuple[int, int], player_direction: Tuple[int, int]) -> None:
        """Update all ghosts movement and pathfinding."""
        for ghost in ghosts:
            if not ghost.active:
                continue
                
            # Always get new target and calculate new path
            blinky_pos = ghosts[0].pos if ghost.ghost_type != 'blinky' else None
            target = ghost.get_chase_target(
                player_pos,
                player_direction,
                blinky_pos
            )
            
            # Ensure target is within grid bounds
            target_row = max(0, min(target[0], len(grid) - 1))
            target_col = max(0, min(target[1], len(grid[0]) - 1))
            adjusted_target = (target_row, target_col)
            
            # Avoid targeting walls
            if grid[target_row][target_col] == 1:
                # Try to find a nearby non-wall position
                for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                    nr, nc = target_row + dr, target_col + dc
                    if (0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and 
                            grid[nr][nc] != 1):
                        adjusted_target = (nr, nc)
                        break
            
            # Calculate new path to the adjusted target
            path = astar_path(grid, ghost.pos, adjusted_target)
            
            # Don't update path if the resulting path is empty or just the current position
            if path and len(path) > 1:
                ghost.set_path(path)
            
            # Attempt to move the ghost
            if not ghost.move_step() and ghost.active:
                # If we couldn't move, try to recalculate a path
                new_path = astar_path(grid, ghost.pos, adjusted_target)
                if new_path and len(new_path) > 1:
                    ghost.path = new_path
                    ghost.path_index = 0
                    ghost.moving = True
                    ghost.move_step()
