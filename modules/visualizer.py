import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

from .algorithms import heuristic, astar_step, dijkstra_step
from .agent import PathAgent
from .grid import create_grid

class Maze3DVisualizer:
    def __init__(self):
        pygame.init()
        pygame.font.init()  # Fixed font initialization
        self.width = 1600
        self.height = 900
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Pathfinding Visualization")  # Fixed method name

        # UI elements
        self.font = pygame.font.Font(None, 36)
        self.ui_buttons = {
            'start': pygame.Rect(20, self.height - 60, 100, 40),
            'reset': pygame.Rect(140, self.height - 60, 100, 40)
        }
        self.button_colors = {
            'normal': (100, 100, 100),
            'hover': (150, 150, 150),
            'text': (255, 255, 255)
        }
        self.rotation_angle = 30  # Initial rotation angle

        # OpenGL initialization with improved lighting
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (50.0, 50.0, 50.0, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
        
        self.camera_distance = 45
        self.camera_height = 35
        self.camera_angle = 30
        
        # Set up the isometric camera
        self.setup_camera()
        
        # Initialize game state
        self.grid, self.heights = create_grid()
        self.start = (0, 0)
        self.goal = (14, 14)
        
        # Initialize pathfinding states
        self.reset_algorithm_states()
        
        # Animation control
        self.is_running = False
        self.exploration_speed = 100
        self.agent_speed = 100
        
        # Create agents
        self.agent_astar = PathAgent(self.start)
        self.agent_dijkstra = PathAgent(self.start)

        # Create separate surface for UI
        self.ui_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)

        # Create UI background surface
        self.ui_background = pygame.Surface((400, 200), pygame.SRCALPHA)
        self.ui_background.fill((0, 0, 0, 180))  # Semi-transparent black background

        # Add time tracking
        self.astar_time = 0.0
        self.dijkstra_time = 0.0
        self.start_time = None

        # Initialize GLUT for text rendering
        glutInit()
        
        # Add text rendering surface
        self.text_surface = pygame.Surface((256, 64), pygame.SRCALPHA)
        self.text_font = pygame.font.Font(None, 24)

    def setup_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.width/self.height), 0.1, 200.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Top-down view: center roughly between both maps (x=2, z=7) and high above (y=50)
        gluLookAt(2, 50, 7, 2, 0, 7, 0, 0, -1)

    def draw_cube(self, position, color, scale=1.0):
        x, y, z = position
        r, g, b = color
        
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(scale, scale, scale)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (r, g, b, 1.0))
        
        # Updated vertices and faces for a fully rendered cube
        vertices = [
            (-1, -1, -1),  # 0
            ( 1, -1, -1),  # 1
            ( 1,  1, -1),  # 2
            (-1,  1, -1),  # 3
            (-1, -1,  1),  # 4
            ( 1, -1,  1),  # 5
            ( 1,  1,  1),  # 6
            (-1,  1,  1)   # 7
        ]
        faces = [
            (0, 1, 5, 4),  # Bottom
            (3, 2, 6, 7),  # Top
            (4, 5, 6, 7),  # Front
            (0, 1, 2, 3),  # Back
            (0, 4, 7, 3),  # Left
            (1, 5, 6, 2)   # Right
        ]
        
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()
        
        glPopMatrix()

    def draw_maze3d(self, offset_x, grid, visited, path, agent_pos):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x = j + offset_x
                z = i
                base_height = self.heights[i][j]
                
                # Draw base tiles (terrain) at lowest level
                if grid[i][j] == 1:  # Wall
                    self.draw_cube((x, base_height/2, z), (0.2, 0.2, 0.2), 0.5)
                elif grid[i][j] == 2:  # Slow terrain
                    self.draw_cube((x, base_height/2, z), (0.6, 0.3, 0.1), 0.5)
                else:  # Normal terrain
                    self.draw_cube((x, base_height/2, z), (0.8, 0.8, 0.8), 0.5)

        # Draw visited cells above terrain
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x = j + offset_x
                z = i
                if (i, j) in visited:
                    # Draw visited cells higher than walls and terrain
                    self.draw_cube((x, 1.5, z), (0.3, 0.5, 0.8), 0.3)  # Darker blue

        # Draw path above visited cells
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x = j + offset_x
                z = i
                if path and (i, j) in path:
                    # Draw path even higher
                    self.draw_cube((x, 2.0, z), (1.0, 1.0, 0.0), 0.3)

        # Draw start, goal and agent at the highest level
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x = j + offset_x
                z = i
                # Draw agent and markers at the highest level
                if agent_pos and (i, j) == agent_pos:
                    self.draw_cube((x, 2.5, z), (0.0, 0.0, 1.0), 0.4)
                if (i, j) == self.start:
                    self.draw_cube((x, 2.5, z), (0.0, 1.0, 0.0), 0.4)
                elif (i, j) == self.goal:
                    self.draw_cube((x, 2.5, z), (1.0, 0.0, 0.0), 0.4)

    def reset_algorithm_states(self):
        # A* state
        self.astar_open = [(heuristic(self.start, self.goal), self.start)]
        self.astar_closed = set()
        self.astar_came_from = {}
        self.astar_g_score = {self.start: 0}
        self.astar_done = False
        self.astar_path = None
        
        # Dijkstra state
        self.dijkstra_open = [(0, self.start)]
        self.dijkstra_closed = set()
        self.dijkstra_came_from = {}
        self.dijkstra_g_score = {self.start: 0}
        self.dijkstra_done = False
        self.dijkstra_path = None
        
        # Reset agents
        self.agent_astar = PathAgent(self.start)
        self.agent_dijkstra = PathAgent(self.start)

        # Reset time tracking
        self.start_time = None
        self.astar_time = 0.0
        self.dijkstra_time = 0.0

    def update(self):
        if not self.is_running:
            return

        if self.start_time is None:
            self.start_time = time.time()

        # Update A*
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

        # Move agents along final paths
        if self.astar_done:
            self.agent_astar.move_step()
        if self.dijkstra_done:
            self.agent_dijkstra.move_step()

    def draw_ui(self):
        # Clear UI surface
        self.ui_surface.fill((0, 0, 0, 0))
        
        # Draw semi-transparent background for UI text
        self.ui_surface.blit(self.ui_background, (10, self.height - 220))
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for text, rect in self.ui_buttons.items():
            color = self.button_colors['hover'] if rect.collidepoint(mouse_pos) else self.button_colors['normal']
            pygame.draw.rect(self.ui_surface, color, rect)
            text_surface = self.font.render(text.title(), True, self.button_colors['text'])
            text_rect = text_surface.get_rect(center=rect.center)
            self.ui_surface.blit(text_surface, text_rect)
        
        # Draw color legend
        legend_items = [
            ("Black", (51, 51, 51), "Walls"),
            ("Brown", (153, 76, 0), "Slow Terrain (2x cost)"),
            ("Light Blue", (128, 179, 255), "Visited Cells"),
            ("Yellow", (255, 255, 0), "Final Path"),
            ("Magenta", (255, 0, 255), "Current Best Path"),
            ("Blue", (0, 0, 255), "Agent Position"),
            ("Green", (0, 255, 0), "Start Point"),
            ("Red", (255, 0, 0), "Goal Point")
        ]

        legend_y = 100
        for name, color, desc in legend_items:
            pygame.draw.rect(self.ui_surface, color, pygame.Rect(20, legend_y, 20, 20))
            text_surface = self.font.render(f"{name}: {desc}", True, (255, 255, 255))
            self.ui_surface.blit(text_surface, (50, legend_y))
            legend_y += 30

        # Draw instructions in control area
        instructions = [
            "Controls:",
            "SPACE - Start/Pause",
            "R - Reset"
        ]

        instruction_y = self.height - 200
        for instruction in instructions:
            text_surface = self.font.render(instruction, True, (255, 255, 255))
            self.ui_surface.blit(text_surface, (20, instruction_y))
            instruction_y += 25

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # Use top-down camera view instead of rotating view:
        gluLookAt(2, 50, 7, 2, 0, 7, 0, 0, -1)

        # Draw both maps without additional rotation
        self.draw_maze3d(-20, self.grid, self.astar_closed, 
                        self.astar_path, self.agent_astar.pos)
        self.draw_maze3d(10, self.grid, self.dijkstra_closed, 
                        self.dijkstra_path, self.agent_dijkstra.pos)
        
        # Add labels for the maps above each maze
        self.draw_text_3d(-14, 3, 0, ["A* Algorithm"])
        self.draw_text_3d(13, 3, 0, ["Dijkstra's Algorithm"])
        
        # Calculate and display real-time elapsed times if start_time is set
        if self.start_time is not None:
            curr_time = time.time() - self.start_time
            astar_display_time = self.astar_time if self.astar_done else curr_time
            dijkstra_display_time = self.dijkstra_time if self.dijkstra_done else curr_time

            self.draw_text_3d(-12, 10, 0, [f"Time: {astar_display_time:.3f}s"])
            self.draw_text_3d(12, 10, 0, [f"Time: {dijkstra_display_time:.3f}s"])
            diff = abs(astar_display_time - dijkstra_display_time)
            self.draw_text_3d(-1, 10, 0, [f"Time Diff: {diff:.3f}s"])
        
        # Draw current best candidate exploration paths (magenta) if still exploring
        if self.agent_astar.exploring and self.agent_astar.path:
            for cell in self.agent_astar.path:
                i, j = cell
                x = j - 20
                z = i
                self.draw_cube((x, 2.2, z), (1.0, 0.0, 1.0), 0.2)
        if self.agent_dijkstra.exploring and self.agent_dijkstra.path:
            for cell in self.agent_dijkstra.path:
                i, j = cell
                x = j + 10
                z = i
                self.draw_cube((x, 2.2, z), (1.0, 0.0, 1.0), 0.2)

        # Draw UI with proper blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Switch to 2D mode for UI
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Disable lighting and depth test for UI
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        
        # Draw UI
        self.draw_ui()
        pygame_surface = pygame.image.tostring(self.ui_surface, 'RGBA', True)
        glRasterPos2d(0, self.height)
        glDrawPixels(self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE, pygame_surface)
        
        # Draw algorithm stats in 3D space
        if self.astar_path:
            stats_text = [
                f"A* Path Length: {len(self.astar_path)}",
                f"Time: {self.astar_time:.3f}s"
            ]
            self.draw_text_3d(-25, 2, 0, stats_text)
        
        if self.dijkstra_path:
            stats_text = [
                f"Dijkstra Path Length: {len(self.dijkstra_path)}",
                f"Time: {self.dijkstra_time:.3f}s"
            ]
            self.draw_text_3d(5, 2, 0, stats_text)

        # Restore 3D state
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glDisable(GL_BLEND)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        
        pygame.display.flip()

    def draw_text_3d(self, x, y, z, text_lines):
        """Draw text using pygame surface converted to texture"""
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(-self.rotation_angle, 0, 1, 0)
        
        # Create text surface
        self.text_surface.fill((0, 0, 0, 0))
        y_offset = 0
        for text in text_lines:
            text_render = self.text_font.render(text, True, (255, 255, 255))
            self.text_surface.blit(text_render, (0, y_offset))
            y_offset += 20
        
        # Convert pygame surface to OpenGL texture
        text_data = pygame.image.tostring(self.text_surface, 'RGBA', True)
        
        # Enable blending for transparent background
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Render the text texture as a billboard
        glRasterPos3f(0, 0, 0)
        glDrawPixels(self.text_surface.get_width(), self.text_surface.get_height(), 
                    GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
        glDisable(GL_BLEND)
        glPopMatrix()

    def handle_mouse_click(self, pos):
        for button, rect in self.ui_buttons.items():
            if rect.collidepoint(pos):
                if button == 'start':
                    self.is_running = True
                elif button == 'reset':
                    self.reset_algorithm_states()
                    self.is_running = False

    def run(self):
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
                        self.is_running = not self.is_running
                    elif event.key == pygame.K_r:
                        self.reset_algorithm_states()
                        self.is_running = False
            
            self.update()
            self.render()
            clock.tick(60)
