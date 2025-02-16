import pygame
import time
from typing import List, Tuple
from modules.grid import create_grid
from modules.algorithms import heuristic, astar_step
from modules.agent import PathAgent

def compute_astar_path(grid: List[List[int]], start: Tuple[int,int], goal: Tuple[int,int]) -> List[Tuple[int,int]]:
    open_list = [(heuristic(start, goal), start)]
    closed_set = set()
    came_from = {}
    g_score = {start: 0}
    path = None
    while True:
        current, is_complete, res_path, came_from = astar_step(grid, start, goal, open_list, closed_set, came_from, g_score)
        if res_path:
            path = res_path
        if is_complete:
            break
    # Check that the computed path actually ends at the goal.
    if not path or path[-1] != goal:
        return None
    return path

class ControlledVisualizer:
    def __init__(self) -> None:
        pygame.init()
        self.width = 800
        self.height = 800
        self.cell_size = 40
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Controlled Pathfinding")
        
        self.grid, _ = create_grid()
        # Set agent's starting point to the center of a 15x15 grid
        self.agent = PathAgent((7, 7))
        self.goal = (7, 7)  # initial goal same as start
        self.path = []
        self.font = pygame.font.Font(None, 24)
        self.running = True
        self.message = ""  # Added to display error messages

    def draw_grid(self) -> None:
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                x = j * self.cell_size
                y = i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if self.grid[i][j] == 1:
                    color = (51, 51, 51)
                elif self.grid[i][j] == 2:
                    color = (153, 76, 0)
                else:
                    color = (200, 200, 200)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100,100,100), rect, 1)
                if (i, j) == self.goal:
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)

        if self.path:
            for (i, j) in self.path:
                x = j * self.cell_size
                y = i * self.cell_size
                s = pygame.Surface((self.cell_size, self.cell_size))
                s.set_alpha(150)
                s.fill((255, 255, 0))
                self.screen.blit(s, (x, y))

    def draw_agent(self) -> None:
        i, j = self.agent.pos
        x = j * self.cell_size
        y = i * self.cell_size
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (0, 255, 0), rect)
                
    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        mouse_x, mouse_y = event.pos
                        j = mouse_x // self.cell_size
                        i = mouse_y // self.cell_size
                        # Check for out-of-bound indices.
                        if i < 0 or i >= len(self.grid) or j < 0 or j >= len(self.grid[0]):
                            self.message = "You can't go there"
                        elif self.grid[i][j] == 1:
                            self.message = "You can't go there"
                        else:
                            path = compute_astar_path(self.grid, self.agent.pos, (i, j))
                            if not path:
                                self.message = "You can't go there"
                            else:
                                self.goal = (i, j)
                                self.path = path
                                self.agent.set_final_path(path)
                                self.message = ""
        
            if self.agent.path and self.agent.path_index < len(self.agent.path) - 1:
                self.agent.move_step()

            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_agent()
            instructions = self.font.render("Right-click to set goal; agent moves automatically.", True, (0, 0, 0))
            self.screen.blit(instructions, (10, self.height - 30))
            # Display error message if any.
            if self.message:
                error_surface = self.font.render(self.message, True, (255, 0, 0))
                self.screen.blit(error_surface, (10, self.height - 60))
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    app = ControlledVisualizer()
    app.run()
