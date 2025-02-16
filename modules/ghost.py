from typing import Tuple, List
from .agent import PathAgent
import math

class Ghost(PathAgent):
    def __init__(self, pos: Tuple[int, int], ghost_type: str):
        super().__init__(pos)
        self.ghost_type = ghost_type
        self.scatter_mode = False
        self.color = self.get_ghost_color()
        self.scatter_target = self.get_scatter_target()
        
    def get_ghost_color(self) -> Tuple[int, int, int]:
        colors = {
            'blinky': (255, 0, 0),    # Red
            'pinky': (255, 182, 255),  # Pink
            'inky': (0, 255, 255),     # Cyan
            'clyde': (255, 182, 85)    # Orange
        }
        return colors.get(self.ghost_type, (255, 0, 0))
        
    def get_scatter_target(self) -> Tuple[int, int]:
        corners = {
            'blinky': (1, 23),      # Upper-right
            'pinky': (1, 1),        # Upper-left
            'inky': (23, 23),       # Lower-right
            'clyde': (23, 1)        # Lower-left
        }
        return corners.get(self.ghost_type, (1, 1))

    def get_chase_target(self, player_pos: Tuple[int, int], player_direction: Tuple[int, int], 
                        blinky_pos: Tuple[int, int] = None) -> Tuple[int, int]:
        if self.scatter_mode:
            return self.scatter_target
            
        if self.ghost_type == 'blinky':
            return player_pos
            
        elif self.ghost_type == 'pinky':
            # Target 2 tiles in front of Pac-Man
            target_x = player_pos[0] + (2 * player_direction[0])
            target_y = player_pos[1] + (2 * player_direction[1])
            # Reproduce the original game's bug when Pac-Man faces up
            if player_direction == (-1, 0):  # Facing up
                target_y -= 2
            return (target_x, target_y)
            
        elif self.ghost_type == 'inky' and blinky_pos:
            # Get position 2 tiles in front of Pac-Man
            intermediate_x = player_pos[0] + (2 * player_direction[0])
            intermediate_y = player_pos[1] + (2 * player_direction[1])
            # Double the vector from Blinky to that position
            vector_x = intermediate_x - blinky_pos[0]
            vector_y = intermediate_y - blinky_pos[1]
            return (intermediate_x + vector_x, intermediate_y + vector_y)
            
        elif self.ghost_type == 'clyde':
            # If within 8 tiles of Pac-Man, go to scatter mode
            distance = math.sqrt((player_pos[0] - self.pos[0])**2 + 
                               (player_pos[1] - self.pos[1])**2)
            if distance < 8:
                return self.scatter_target
            return player_pos
            
        return player_pos  # Default behavior
