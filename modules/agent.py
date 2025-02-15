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
        self.height: float = 0.0
        self.target_height: float = 0.0
        self.height_speed: float = 0.1
        
    def set_exploration_path(self, current: Point, came_from: Dict[Point, Point]) -> None:
        if not current:
            return
        # Update using the best candidate path.
        self.path = reconstruct_path(came_from, current)
        self.path_index = len(self.path) - 1
        self.pos = current
        self.target_height = 0.3
        
    def set_final_path(self, path: List[Point]) -> None:
        self.path = path
        self.path_index = 0
        self.moving = True
        self.exploring = False
        self.target_height = 0.5
        
    def move_step(self) -> bool:
        if self.height < self.target_height:
            self.height = min(self.height + self.height_speed, self.target_height)
        elif self.height > self.target_height:
            self.height = max(self.height - self.height_speed, self.target_height)
            
        if self.moving and self.path_index < len(self.path) - 1:
            self.path_index += 1
            self.pos = self.path[self.path_index]
            return True
        self.moving = False
        return False

    def get_3d_position(self) -> Tuple[int, float, int]:
        x, y = self.pos
        return (x, self.height, y)
