from typing import List, Tuple, Dict, Optional
from .algorithms import reconstruct_path

Position = Tuple[int, int]

class PathAgent:
    """Base class for game entities that follow paths."""
    
    def __init__(self, start_pos: Position):
        self.pos: Position = start_pos
        self.path: List[Position] = []
        self.path_index: int = 0
        self.moving: bool = False
        self.direction: int = 0  # 0: right, 90: down, 180: left, 270: up

    def set_path(self, path: List[Position]) -> None:
        """Set a new path for the agent to follow."""
        if not path:
            return
        
        # Keep current position if already moving
        if self.moving and self.path:
            # Only update path if it's significantly different
            if len(path) > 1 and path[1] != self.path[min(self.path_index + 1, len(self.path) - 1)]:
                self.path = path
                self.path_index = 0
        else:
            self.path = path
            self.path_index = 0
            
        self.moving = True

    def move_step(self) -> bool:
        """Move one step along the current path. Returns True if moved."""
        if not self.moving or self.path_index >= len(self.path) - 1:
            self.moving = False
            return False

        old_pos = self.pos
        self.path_index += 1
        self.pos = self.path[self.path_index]
        
        # Update direction based on movement
        dx = self.pos[1] - old_pos[1]
        dy = self.pos[0] - old_pos[0]
        
        if dx > 0:      self.direction = 0
        elif dx < 0:    self.direction = 180
        elif dy > 0:    self.direction = 90
        elif dy < 0:    self.direction = 270
        
        return True
