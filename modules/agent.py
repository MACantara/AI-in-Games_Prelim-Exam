from typing import List, Tuple, Dict
from .algorithms import reconstruct_path

Point = Tuple[int, int]

class PathAgent:
    def __init__(self, start_pos: Point) -> None:
        self.pos: Point = start_pos
        self.path: List[Point] = []
        self.path_index: int = 0
        self.moving: bool = False
        self.exploring: bool = True
        self.mouth_open = True
        self.animation_time = 0
        self.direction = 0  # 0: right, 90: down, 180: left, 270: up
        
    def set_exploration_path(self, current: Point, came_from: Dict[Point, Point]) -> None:
        if not current:
            return
        self.path = reconstruct_path(came_from, current)
        self.path_index = len(self.path) - 1
        self.pos = current
        
    def set_final_path(self, path: List[Point]) -> None:
        self.path = path
        self.path_index = 0
        self.moving = True
        self.exploring = False
        self.direction = 0  # Reset direction when new path is set
        
    def move_step(self) -> bool:
        if self.moving and self.path_index < len(self.path) - 1:
            old_pos = self.pos
            self.path_index += 1
            self.pos = self.path[self.path_index]
            
            # Calculate direction based on movement
            dx = self.pos[1] - old_pos[1]  # Column difference (x-axis)
            dy = self.pos[0] - old_pos[0]  # Row difference (y-axis)
            
            if dx > 0:  # Moving right
                self.direction = 0
            elif dx < 0:  # Moving left
                self.direction = 180
            elif dy > 0:  # Moving down
                self.direction = 90
            elif dy < 0:  # Moving up
                self.direction = 270
                
            self.mouth_open = not self.mouth_open
            return True
        self.moving = False
        return False
