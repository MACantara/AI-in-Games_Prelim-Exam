import pygame
from typing import List, Tuple
import time

from .algorithms import heuristic, astar_step, dijkstra_step
from .agent import PathAgent
from .grid import create_grid, START, GOAL

class Maze2DVisualizer:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        # Adjust window size and layout
        self.width = 1800
        self.height = 900
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("2D Pathfinding Visualization")
        self.font = pygame.font.Font(None, 36)
        self.font_bold = pygame.font.Font(None, 42)  # Slightly larger font for time difference
        self.cell_size = 35  # Slightly smaller cells
        
        # Move buttons to bottom center of screen
        button_y = self.height - 60
        center_x = self.width // 2
        self.ui_buttons = {
            'start': pygame.Rect(center_x - 120, button_y, 100, 40),
            'reset': pygame.Rect(center_x + 20, button_y, 100, 40)
        }
        self.button_colors = {
            'normal': (100, 100, 100),
            'hover': (150, 150, 150),
            'text': (255, 255, 255)
        }
        
        self.grid, _ = create_grid()
        self.start = START
        self.goal = GOAL
        
        self.reset_algorithm_states()
        self.is_running = False
        
        self.agent_astar = PathAgent(self.start)
        self.agent_dijkstra = PathAgent(self.start)
        
        # Create base Pacman sprites (facing right)
        pacman_size = 30
        self.pacman_open = pygame.Surface((pacman_size, pacman_size), pygame.SRCALPHA)
        self.pacman_closed = pygame.Surface((pacman_size, pacman_size), pygame.SRCALPHA)
        
        # Draw yellow circle for both states
        pygame.draw.circle(self.pacman_open, (255, 255, 0), (pacman_size//2, pacman_size//2), pacman_size//2)
        pygame.draw.circle(self.pacman_closed, (255, 255, 0), (pacman_size//2, pacman_size//2), pacman_size//2)
        
        # Draw mouth points (right-facing wedge)
        center = (pacman_size//2, pacman_size//2)
        mouth_points = [
            center,  # Center point
            (pacman_size, center[1] - pacman_size//4),  # Top right
            (pacman_size, center[1] + pacman_size//4)   # Bottom right
        ]
        pygame.draw.polygon(self.pacman_open, (0, 0, 0), mouth_points)
        
        # Store original sprites for rotation
        self.pacman_open_original = self.pacman_open.copy()
        self.pacman_closed_original = self.pacman_closed.copy()
        
        self.animation_speed = 50  # milliseconds per frame for mouth animation
        self.movement_delay = 100   # milliseconds between moves
        self.last_animation = pygame.time.get_ticks()
        self.last_movement = pygame.time.get_ticks()

        # Initialize UI surfaces
        self.ui_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.ui_background = pygame.Surface((400, 200), pygame.SRCALPHA)
        self.ui_background.fill((0, 0, 0, 180))

    def draw_grid(self, offset_x: int, grid: List[List[int]], visited: set,
                 path: List[Tuple[int, int]], agent: PathAgent) -> None:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x = j * self.cell_size + offset_x
                y = i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                # Draw base cell
                if grid[i][j] == 1:  # Wall
                    pygame.draw.rect(self.screen, (51, 51, 51), rect)
                elif grid[i][j] == 2:  # Slow terrain
                    pygame.draw.rect(self.screen, (153, 76, 0), rect)
                else:  # Normal terrain
                    pygame.draw.rect(self.screen, (200, 200, 200), rect)
                
                # Draw visited cells
                if (i, j) in visited:
                    s = pygame.Surface((self.cell_size, self.cell_size))
                    s.set_alpha(128)
                    s.fill((128, 179, 255))
                    self.screen.blit(s, (x, y))
                
                # Draw path
                if not agent.exploring and path and (i, j) in path:
                    # Final path in yellow (existing)
                    s = pygame.Surface((self.cell_size, self.cell_size))
                    s.set_alpha(128)
                    s.fill((255, 255, 0))
                    self.screen.blit(s, (x, y))
                elif agent.exploring and path and (i, j) in path:
                    # Current best path in magenta during exploration
                    s = pygame.Surface((self.cell_size, self.cell_size))
                    s.set_alpha(128)
                    s.fill((255, 0, 255))  # Magenta
                    self.screen.blit(s, (x, y))
                
                # Draw grid lines
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
                
                # Draw start and goal
                if (i, j) == self.start:
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
                elif (i, j) == self.goal:
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)
                
                # Draw agent with animation and rotation
                if (i, j) == agent.pos:
                    if agent.moving:
                        base_sprite = self.pacman_open_original if agent.mouth_open else self.pacman_closed_original
                        
                        # Calculate next position if available
                        next_pos = None
                        if agent.path_index + 1 < len(agent.path):
                            next_pos = agent.path[agent.path_index + 1]
                            
                        # Determine direction based on next position
                        if next_pos:
                            dx = next_pos[1] - agent.pos[1]  # Column difference
                            dy = next_pos[0] - agent.pos[0]  # Row difference
                            
                            if dx > 0:      # Moving right
                                rotation = 0    # No rotation needed, sprite faces right by default
                            elif dx < 0:     # Moving left
                                rotation = 90  # Rotate 180° to face left
                            elif dy > 0:     # Moving down
                                rotation = 270   # Rotate 90° to face down
                            else:            # Moving up
                                rotation = 270  # Rotate 270° to face up
                        else:
                            rotation = agent.direction
                    else:
                        base_sprite = self.pacman_open_original
                        rotation = agent.direction
                    
                    # Rotate sprite
                    sprite = pygame.transform.rotate(base_sprite, rotation)
                    sprite_rect = sprite.get_rect(center=(x + self.cell_size//2, y + self.cell_size//2))
                    self.screen.blit(sprite, sprite_rect)

    def render(self) -> None:
        self.screen.fill((255, 255, 255))
        
        # Draw legend on the left side
        self.draw_legend(20, 500)
        
        # Center the grids and add more spacing between them
        grid_offset = (self.width - (2 * 15 * self.cell_size + 200)) // 2
        
        # Draw A* grid and info
        astar_x = grid_offset
        self.draw_grid(astar_x, self.grid, self.astar_closed,
                      self.astar_path, self.agent_astar)
        
        # Draw Dijkstra grid and info
        dijkstra_x = astar_x + (15 * self.cell_size) + 200
        self.draw_grid(dijkstra_x, self.grid, self.dijkstra_closed,
                      self.dijkstra_path, self.agent_dijkstra)

        # Draw statistics and labels at the bottom
        stats_y = self.height - 120
        title_y = stats_y - 40  # Position titles just above stats

        # Draw A* label and stats
        astar_title = self.font.render("A* Algorithm", True, (0, 0, 0))
        self.screen.blit(astar_title, (astar_x + (15 * self.cell_size)//2 - astar_title.get_width()//2, title_y))
        
        if self.astar_done:
            astar_stats = [
                f"Time: {self.astar_time:.3f}s",
                f"Path Length: {len(self.astar_path) if self.astar_path else 0}",
                f"Nodes Explored: {len(self.astar_closed)}"
            ]
            y = stats_y
            for stat in astar_stats:
                text = self.font.render(stat, True, (0, 0, 0))
                self.screen.blit(text, (astar_x + (15 * self.cell_size)//2 - text.get_width()//2, y))
                y += 25

        # Draw Dijkstra label and stats
        dijkstra_title = self.font.render("Dijkstra's Algorithm", True, (0, 0, 0))
        self.screen.blit(dijkstra_title, (dijkstra_x + (15 * self.cell_size)//2 - dijkstra_title.get_width()//2, title_y))
        
        if self.dijkstra_done:
            dijkstra_stats = [
                f"Time: {self.dijkstra_time:.3f}s",
                f"Path Length: {len(self.dijkstra_path) if self.dijkstra_path else 0}",
                f"Nodes Explored: {len(self.dijkstra_closed)}"
            ]
            y = stats_y
            for stat in dijkstra_stats:
                text = self.font.render(stat, True, (0, 0, 0))
                self.screen.blit(text, (dijkstra_x + (15 * self.cell_size)//2 - text.get_width()//2, y))
                y += 25

        # Draw time difference in the center between grids
        if self.astar_done and self.dijkstra_done:
            center_x = self.width // 2
            time_diff = abs(self.astar_time - self.dijkstra_time)
            faster_algo = "A*" if self.astar_time < self.dijkstra_time else "Dijkstra"
            
            diff_text = [
                f"Time Difference:",
                f"{time_diff:.3f}s",
                f"{faster_algo} is faster!"
            ]
            
            y = self.height - 180
            for text in diff_text:
                surface = self.font_bold.render(text, True, (0, 0, 100))
                self.screen.blit(surface, 
                               (center_x - surface.get_width()//2, y))
                y += 30

        # Draw instructions and UI
        self.draw_instructions(20, self.height - 145)
        self.draw_ui()
        
        pygame.display.flip()

    # Keep other methods the same, just remove OpenGL-specific code
    def reset_algorithm_states(self) -> None:
        self.astar_open = [(heuristic(self.start, self.goal), self.start)]
        self.astar_closed = set()
        self.astar_came_from = {}
        self.astar_g_score = {self.start: 0}
        self.astar_done = False
        self.astar_path = None
        self.dijkstra_open = [(0, self.start)]
        self.dijkstra_closed = set()
        self.dijkstra_came_from = {}
        self.dijkstra_g_score = {self.start: 0}
        self.dijkstra_done = False
        self.dijkstra_path = None
        self.agent_astar = PathAgent(self.start)
        self.agent_dijkstra = PathAgent(self.start)
        self.start_time = None
        self.accumulated_time = 0.0
        self.astar_time = 0.0
        self.dijkstra_time = 0.0

    def update(self) -> None:
        if not self.is_running:
            return
            
        current_time = pygame.time.get_ticks()
        
        # Handle mouth animation
        if current_time - self.last_animation > self.animation_speed:
            self.last_animation = current_time
            if self.astar_done and self.agent_astar.moving:
                self.agent_astar.mouth_open = not self.agent_astar.mouth_open
            if self.dijkstra_done and self.agent_dijkstra.moving:
                self.agent_dijkstra.mouth_open = not self.agent_dijkstra.mouth_open

        # Handle movement with delay
        if current_time - self.last_movement > self.movement_delay:
            self.last_movement = current_time
            # Move agents along final paths
            if self.astar_done:
                self.agent_astar.move_step()
            if self.dijkstra_done:
                self.agent_dijkstra.move_step()

        # Handle pathfinding updates
        if self.start_time is None:
            self.start_time = time.time()
            
        # A* and Dijkstra step updates
        if not self.astar_done:
            current, is_complete, path, came_from = astar_step(
                self.grid, self.start, self.goal,
                self.astar_open, self.astar_closed,
                self.astar_came_from, self.astar_g_score
            )
            self.agent_astar.set_exploration_path(current, came_from)
            
            if is_complete:
                self.astar_done = True
                self.astar_path = path
                self.astar_time = time.time() - self.start_time
                self.agent_astar.set_final_path(path)

        # Update Dijkstra
        if not self.dijkstra_done:
            current, is_complete, path, came_from = dijkstra_step(
                self.grid, self.start, self.goal,
                self.dijkstra_open, self.dijkstra_closed,
                self.dijkstra_came_from, self.dijkstra_g_score
            )
            self.agent_dijkstra.set_exploration_path(current, came_from)
            
            if is_complete:
                self.dijkstra_done = True
                self.dijkstra_path = path
                self.dijkstra_time = time.time() - self.start_time
                self.agent_dijkstra.set_final_path(path)

    def draw_legend(self, x: int, y: int) -> None:
        legend_items = [
            (None, None, "Color Legend"),
            ("Black", (51, 51, 51), "Walls"),
            ("Brown", (153, 76, 0), "Slow Terrain (2x cost)"),
            ("Light Blue", (128, 179, 255), "Visited Cells"),
            ("Magenta", (255, 0, 255), "Current Best Path"),
            ("Yellow", (255, 255, 0), "Final Path"),
            ("Green", (0, 255, 0), "Start Point"),
            ("Red", (255, 0, 0), "Goal Point")
        ]
        
        for name, color, desc in legend_items:
            if color is not None:  # Only draw colored rectangle if color is specified
                pygame.draw.rect(self.screen, color, pygame.Rect(x, y, 20, 20))
                text = self.font.render(f"{name}: {desc}", True, (0, 0, 0))
            else:  # For the header, just render the text
                text = self.font.render(desc, True, (0, 0, 0))
            self.screen.blit(text, (x + 30, y))
            y += 30

    def draw_instructions(self, x: int, y: int) -> None:
        instructions = [
            "Controls:",
            "SPACE - Start/Pause",
            "R - Reset",
            "",
            "Press Start to begin"
        ]
        
        for instruction in instructions:
            text = self.font.render(instruction, True, (0, 0, 0))
            self.screen.blit(text, (x, y))
            y += 25

    def draw_ui(self) -> None:
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for text, rect in self.ui_buttons.items():
            color = self.button_colors['hover'] if rect.collidepoint(mouse_pos) else self.button_colors['normal']
            pygame.draw.rect(self.screen, color, rect)
            text_surface = self.font.render(text.title(), True, self.button_colors['text'])
            self.screen.blit(text_surface, text_surface.get_rect(center=rect.center))

    def handle_mouse_click(self, pos: Tuple[int, int]) -> None:
        for button, rect in self.ui_buttons.items():
            if rect.collidepoint(pos):
                if button == 'start':
                    self.is_running = True
                elif button == 'reset':
                    self.reset_algorithm_states()
                    self.is_running = False

    def run(self) -> None:
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.is_running:
                            # Pause the simulation: accumulate elapsed time and pause agents.
                            if self.start_time is not None:
                                self.accumulated_time += time.time() - self.start_time
                            self.start_time = None
                            self.is_running = False
                        else:
                            # Resume the simulation.
                            self.start_time = time.time()
                            self.is_running = True
                    elif event.key == pygame.K_r:
                        self.reset_algorithm_states()
                        self.is_running = False
            self.update()
            self.render()
            clock.tick(60)