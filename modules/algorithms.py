"""
This module implements A* and Dijkstra search steps with helper functions.
"""
import heapq
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

def astar_path(grid: Grid, start: Position, goal: Position) -> List[Position]:
    """Find path using A* algorithm."""
    # First, ensure the goal is valid and within bounds
    if not (0 <= goal[0] < len(grid) and 0 <= goal[1] < len(grid[0])):
        # If target is out of bounds, find closest valid position
        return [start]
        
    # Don't try to path to walls
    if grid[goal[0]][goal[1]] == 1:
        return [start]
        
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
        
        if current == goal:
            return reconstruct_path(came_from, current)
            
        closed_set.add(current)
        
        for neighbor, cost in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue
                
            tentative_g = g_score[current] + cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
    
    # If we reached here, no path was found or max iterations reached
    # Return at least a path to a nearby valid position if possible
    if came_from:
        # Find the position closest to the goal that we did reach
        best_pos = min(came_from.keys(), key=lambda pos: heuristic(pos, goal))
        return reconstruct_path(came_from, best_pos)
        
    return [start]  # Return single-point path if no path found
