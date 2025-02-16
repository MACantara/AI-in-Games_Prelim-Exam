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
    if not path:
        return [start]
    return path

def can_move_to(grid: List[List[int]], pos: Tuple[int,int]) -> Tuple[bool, Tuple[int,int]]:
    i, j = pos
    # Check for tunnel wrap-around at row 11 (where the tunnel is)
    if i == 11:  # Middle tunnel row
        if j < 0:  # Going through left tunnel
            return True, (i, len(grid[0])-2)  # Wrap to second-to-last position on right
        elif j > len(grid[0])-2:  # Going through right tunnel
            return True, (i, 0)  # Wrap to first position on left
    
    # Normal boundary and wall checks
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
        return False, None
    return (grid[i][j] != 1), None

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
            if (i, j) == (18, 11):  # Position of 'C' in the map
                player_pos = [i, j]
            elif (i, j) in [(11, 10), (11, 11), (11, 13), (11, 14)]:  # Positions of 'M' in the map
                enemy_positions.append((i, j))

    player_color = (255, 255, 0)  # Yellow for player

    # Create ghosts with proper types instead of generic PathAgents
    ghosts = [
        Ghost((11, 8), 'blinky'),   # Red ghost
        Ghost((11, 9), 'pinky'),    # Pink ghost
        Ghost((11, 15), 'inky'),    # Cyan ghost
        Ghost((11, 16), 'clyde'),   # Orange ghost
    ]

    # Add player direction tracking
    player_direction = (0, 0)
    
    # Add scatter mode timing
    scatter_timer = 0
    SCATTER_INTERVAL = 200  # Alternate between scatter and chase every 200 frames

    # Add debug mode flag
    debug_mode = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Add debug mode toggle with F3 key
                if event.key == pygame.K_F3:
                    debug_mode = not debug_mode
                new_pos = player_pos.copy()
                # Update player direction based on key press
                if event.key in [pygame.K_UP, pygame.K_w]:
                    new_pos[0] -= 1
                    player_direction = (-1, 0)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    new_pos[0] += 1
                    player_direction = (1, 0)
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    new_pos[1] -= 1
                    player_direction = (0, -1)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    new_pos[1] += 1
                    player_direction = (0, 1)
                
                can_move, new_position = can_move_to(grid, tuple(new_pos))
                if can_move:
                    player_pos = list(new_position if new_position else new_pos)

        # Update scatter mode
        scatter_timer = (scatter_timer + 1) % (2 * SCATTER_INTERVAL)
        scatter_mode = scatter_timer >= SCATTER_INTERVAL

        # Update enemy paths and move them with delay
        ghost_move_delay = (ghost_move_delay + 1) % GHOST_MOVE_INTERVAL
        if ghost_move_delay == 0:
            # Update each ghost's behavior
            for ghost in ghosts:
                ghost.scatter_mode = scatter_mode
                # Get Blinky's position for Inky's behavior
                blinky_pos = ghosts[0].pos if ghost.ghost_type != 'blinky' else None
                # Get target based on ghost's individual behavior
                target = ghost.get_chase_target(tuple(player_pos), player_direction, blinky_pos)
                
                # Only compute new path if ghost has reached end of current path or has no path
                if not ghost.path or ghost.path_index >= len(ghost.path) - 1:
                    path = compute_astar_path(grid, ghost.pos, target)
                    if path and len(path) > 1:
                        ghost.set_final_path(path)
                
                # Always try to move if we have a path
                if ghost.path and ghost.path_index < len(ghost.path) - 1:
                    next_pos = ghost.path[ghost.path_index + 1]
                    can_move, new_position = can_move_to(grid, next_pos)
                    if can_move:
                        if new_position:  # Instant wrap around
                            ghost.pos = new_position
                            # Update the rest of the path to account for the wrap
                            if ghost.path_index + 2 < len(ghost.path):
                                ghost.path = ghost.path[:ghost.path_index + 1] + [new_position] + ghost.path[ghost.path_index + 2:]
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
        
        # Draw debug paths if debug mode is on
        if debug_mode:
            for ghost in ghosts:
                if ghost.path:
                    # Fix coordinate order in points calculation
                    points = [(p[1] * cell_size + cell_size//2, p[0] * cell_size + cell_size//2) 
                             for p in ghost.path[ghost.path_index:]]
                    if len(points) > 1:
                        pygame.draw.lines(screen, ghost.color, False, points, 2)
                    # Fix coordinate order in target position
                    target = ghost.get_chase_target(tuple(player_pos), player_direction, 
                                                  ghosts[0].pos if ghost.ghost_type != 'blinky' else None)
                    target_pos = (target[1] * cell_size + cell_size//2, 
                                target[0] * cell_size + cell_size//2)
                    pygame.draw.circle(screen, ghost.color, target_pos, 5)

        # Draw player using consistent coordinate order (y before x)
        player_rect = pygame.Rect(player_pos[1]*cell_size, player_pos[0]*cell_size, cell_size, cell_size)
        pygame.draw.ellipse(screen, player_color, player_rect)
        
        # Draw ghosts using consistent coordinate order
        for ghost in ghosts:
            ghost_rect = pygame.Rect(ghost.pos[1]*cell_size, ghost.pos[0]*cell_size, cell_size, cell_size)
            pygame.draw.ellipse(screen, ghost.color, ghost_rect)

        # Draw debug mode status
        font = pygame.font.Font(None, 36)
        debug_text = font.render("Debug Mode: " + ("ON" if debug_mode else "OFF") + " (F3)", True, (255, 255, 255))
        screen.blit(debug_text, (10, height - 30))

        pygame.display.flip()
        clock.tick(30)  # Increased from 10 to 30 for smoother player movement
    pygame.quit()

if __name__ == '__main__':
    main()
