import pygame
from typing import List, Tuple
from modules.grid import create_grid
from modules.algorithms import heuristic, astar_step
from modules.ghost import Ghost  # Change this import

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
    if not path or path[-1] != goal:
        return None
    return path

def can_move_to(grid: List[List[int]], pos: Tuple[int,int]) -> bool:
    i, j = pos
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
        return False
    return grid[i][j] != 1

def main():
    pygame.init()
    cell_size = 30
    width, height = 23 * cell_size, 25 * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pacman with AI Enemies")
    clock = pygame.time.Clock()
    
    # Add ghost movement delay counter
    ghost_move_delay = 0
    GHOST_MOVE_INTERVAL = 6  # Ghosts move every 3 frames

    grid, _ = create_grid()
    
    # Find initial positions from the grid layout
    player_pos = None
    enemy_positions = []
    
    # Scan the map_data to find C and M positions
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x = j * cell_size
            y = i * cell_size
            if (i, j) == (18, 12):  # Position of 'C' in the map
                player_pos = [i, j]
            elif (i, j) in [(11, 8), (11, 9), (11, 15), (11, 16)]:  # Positions of 'M' in the map
                enemy_positions.append((i, j))

    player_color = (255, 255, 0)  # Yellow for player

    # Create ghosts with proper types instead of generic PathAgents
    ghosts = [
        Ghost((11, 8), 'blinky'),   # Red ghost
        Ghost((11, 9), 'pinky'),    # Pink ghost
        Ghost((11, 15), 'inky'),    # Cyan ghost
        Ghost((11, 16), 'clyde'),   # Orange ghost
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_pos = player_pos.copy()
                # Support arrow keys and WASD keys.
                if event.key in [pygame.K_UP, pygame.K_w]:
                    new_pos[0] -= 1
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    new_pos[0] += 1
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    new_pos[1] -= 1
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    new_pos[1] += 1
                if can_move_to(grid, tuple(new_pos)):
                    player_pos = new_pos

        # Update enemy paths and move them with delay
        ghost_move_delay = (ghost_move_delay + 1) % GHOST_MOVE_INTERVAL
        if ghost_move_delay == 0:  # Only move ghosts every GHOST_MOVE_INTERVAL frames
            for ghost in ghosts:
                path = compute_astar_path(grid, ghost.pos, tuple(player_pos))
                if path and len(path) > 1:
                    ghost.set_final_path(path)
                    ghost.move_step()
                    
        # Render scene.
        screen.fill((0, 0, 0))
        # Draw grid.
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x = j * cell_size
                y = i * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)
                if grid[i][j] == 1:  # Wall
                    color = (51,51,51)
                    pygame.draw.rect(screen, color, rect)
                else:  # Empty space or point
                    color = (0, 0, 0)  # Black background
                    pygame.draw.rect(screen, color, rect)
                    if grid[i][j] == 2:  # Point
                        # Draw small yellow dot
                        dot_size = cell_size // 4
                        dot_pos = (x + cell_size//2, y + cell_size//2)
                        pygame.draw.circle(screen, (255, 255, 0), dot_pos, dot_size)
        # Draw player.
        player_rect = pygame.Rect(player_pos[1]*cell_size, player_pos[0]*cell_size, cell_size, cell_size)
        pygame.draw.ellipse(screen, player_color, player_rect)
        # Draw ghosts with their unique colors
        for ghost in ghosts:
            ghost_rect = pygame.Rect(ghost.pos[1]*cell_size, ghost.pos[0]*cell_size, cell_size, cell_size)
            pygame.draw.ellipse(screen, ghost.color, ghost_rect)
        pygame.display.flip()
        clock.tick(30)  # Increased from 10 to 30 for smoother player movement
    pygame.quit()

if __name__ == '__main__':
    main()
