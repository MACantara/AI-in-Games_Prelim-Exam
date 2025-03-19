"""
This module implements A* and Dijkstra search steps with helper functions.
"""
import heapq
import random
from typing import Tuple, List, Dict, Generator, Any

# Type aliases for clarity.
Position = Tuple[int, int]
Grid = List[List[int]]

def heuristic(a: Position, b: Position) -> float:
    """Calculate heuristic distance between two points."""
    if a[0] == 11 and b[0] == 11:  # Special case for tunnel
        direct_dist = abs(a[1] - b[1])
        tunnel_dist = min(a[1] + b[1], (23 - a[1]) + (23 - b[1]))
        return min(direct_dist, tunnel_dist)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos: Position, grid: Grid) -> Generator[Tuple[Position, int], None, None]:
    """Get valid neighboring positions and their movement costs."""
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 1:
            yield (nx, ny), 1

def reconstruct_path(came_from: Dict[Position, Position], current: Position) -> List[Position]:
    """Reconstruct path from start to current position."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def find_flee_target(ghost_pos: Position, player_pos: Position) -> Position:
    """Find a position to flee to (away from player)."""
    # Calculate vector from player to ghost
    dx = ghost_pos[0] - player_pos[0]
    dy = ghost_pos[1] - player_pos[1]
    
    # If the ghost is exactly on the player, choose a random direction
    if dx == 0 and dy == 0:
        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
    
    # Normalize and randomize direction slightly to avoid corners and predictable movement
    magnitude = max(1, abs(dx) + abs(dy))
    dx = dx / magnitude
    dy = dy / magnitude
    
    # Add some randomization to avoid predictable patterns and corner traps
    dx += random.uniform(-0.5, 0.5)
    dy += random.uniform(-0.5, 0.5)
    
    # Re-normalize
    magnitude = max(1, abs(dx) + abs(dy))
    dx = dx / magnitude
    dy = dy / magnitude
    
    # Scale the vector to get a point further away
    scale = 8.0 + random.uniform(0, 4)  # Variable distance (8-12 cells)
    target_x = ghost_pos[0] + int(dx * scale)
    target_y = ghost_pos[1] + int(dy * scale)
    
    # Add some randomness to prevent ghosts from clustering
    target_x += random.randint(-3, 3)
    target_y += random.randint(-3, 3)
    
    return (target_x, target_y)

def astar_path(grid: Grid, start: Position, goal: Position, flee_mode: bool = False) -> List[Position]:
    """Find path using A* algorithm, with option for flee behavior."""
    # Special case for direct path to spawn (when ghost is eaten)
    if grid is None:
        return [start, goal]
        
    # First, ensure the goal is valid and within bounds
    if not (0 <= goal[0] < len(grid) and 0 <= goal[1] < len(grid[0])):
        # If target is out of bounds, find closest valid position
        return [start]
        
    # Don't try to path to walls
    if grid[goal[0]][goal[1]] == 1:
        return [start]
    
    # In flee mode, avoid getting too close to the goal
    # We'll still path to the goal but with a modified heuristic
    
    open_set = [(0, start)]
    closed_set = set()
    came_from = {}
    g_score = {start: 0}
    
    # Limit the search to prevent infinite loops
    max_iterations = 1000
    iterations = 0
    
    while open_set and iterations < max_iterations:
        iterations += 1
        _, current = heapq.heappop(open_set)
        
        # In flee mode, we might want to stop earlier sometimes
        if current == goal or (flee_mode and iterations > max_iterations // 2 and random.random() < 0.1):
            path = reconstruct_path(came_from, current)
            
            # In flee mode, sometimes randomize the path to create less predictable movement
            if flee_mode and len(path) > 3:
                # Add some unpredictability: occasional random turns or shorter paths
                if random.random() < 0.4:  # 40% chance
                    turn_point = random.randint(1, min(5, len(path)-1))
                    return path[:turn_point]
                
            return path
            
        closed_set.add(current)
        
        for neighbor, cost in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue
                
            tentative_g = g_score[current] + cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                
                # Modified heuristic for flee mode
                if flee_mode:
                    # In flee mode, we want to minimize the function f = g + h
                    # But make the heuristic favor paths away from the goal
                    f_score = tentative_g - heuristic(neighbor, goal)
                else:
                    # Normal A* behavior
                    f_score = tentative_g + heuristic(neighbor, goal)
                    
                heapq.heappush(open_set, (f_score, neighbor))
    
    # If we reached here, no path was found or max iterations reached
    # Return at least a path to a nearby valid position if possible
    if came_from:
        if flee_mode:
            # In flee mode, find the position furthest from the goal
            best_pos = max(came_from.keys(), key=lambda pos: heuristic(pos, goal))
        else:
            # In chase mode, find the position closest to the goal
            best_pos = min(came_from.keys(), key=lambda pos: heuristic(pos, goal))
            
        return reconstruct_path(came_from, best_pos)
        
    return [start]  # Return single-point path if no path found
