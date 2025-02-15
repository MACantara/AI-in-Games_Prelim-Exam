from .algorithms import reconstruct_path

class PathAgent:
    def __init__(self, start_pos):
        self.pos = start_pos
        self.path = []
        self.path_index = 0
        self.moving = False
        self.exploring = True
        self.height = 0.0
        self.target_height = 0.0
        self.height_speed = 0.1
        
    def set_exploration_path(self, current, came_from):
        if not current:
            return
        # Always update exploration path using current candidate's best route.
        path = reconstruct_path(came_from, current)
        self.path = path
        self.path_index = len(path) - 1
        self.pos = current
        self.target_height = 0.3
        
    def set_final_path(self, path):
        self.path = path
        self.path_index = 0
        self.moving = True
        self.exploring = False
        self.target_height = 0.5
        
    def move_step(self):
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

    def get_3d_position(self):
        x, y = self.pos
        return (x, self.height, y)
