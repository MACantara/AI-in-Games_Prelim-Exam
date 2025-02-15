"""
This module implements A* and Dijkstra search steps with helper functions.
"""
import heapq
from typing import Tuple, List, Dict, Generator, Any

# Type aliases for clarity.
Point = Tuple[int, int]
Grid = List[List[int]]
CameFrom = Dict[Point, Point]
GScore = Dict[Point, float]

def heuristic(a: Point, b: Point) -> int:
    """Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(pos: Point, grid: Grid) -> Generator[Tuple[Point, int], None, None]:
    """Yield valid neighbor cells and their cost."""
    x, y = pos
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 1:
            yield (nx, ny), (2 if grid[nx][ny] == 2 else 1)

def reconstruct_path(came_from: CameFrom, current: Point) -> List[Point]:
    """Reconstruct path from start to current."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def astar_step(grid: Grid, start: Point, goal: Point, open_set: List[Any],
               closed_set: set, came_from: CameFrom, g_score: GScore
              ) -> Tuple[Any, bool, Any, CameFrom]:
    """Perform one A* algorithm step and return current best candidate path."""
    if not open_set:
        return None, True, None, {}
    
    current_f, current = heapq.heappop(open_set)
    if current == goal:
        return current, True, reconstruct_path(came_from, current), came_from
    
    closed_set.add(current)
    
    for neighbor, cost in neighbors(current, grid):
        if neighbor in closed_set:
            continue
        tentative_g = g_score[current] + cost
        if neighbor not in g_score or tentative_g < g_score[neighbor]:
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g
            heapq.heappush(open_set, (tentative_g + heuristic(neighbor, goal), neighbor))
    
    best_path = reconstruct_path(came_from, current)
    return current, False, best_path, came_from

def dijkstra_step(grid: Grid, start: Point, goal: Point, open_set: List[Any],
                  closed_set: set, came_from: CameFrom, g_score: GScore
                 ) -> Tuple[Any, bool, Any, CameFrom]:
    """Perform one Dijkstra algorithm step and return current best candidate path."""
    if not open_set:
        return None, True, None, {}
    
    current_g, current = heapq.heappop(open_set)
    if current == goal:
        return current, True, reconstruct_path(came_from, current), came_from
    
    closed_set.add(current)
    
    for neighbor, cost in neighbors(current, grid):
        if neighbor in closed_set:
            continue
        tentative_g = g_score[current] + cost
        if neighbor not in g_score or tentative_g < g_score[neighbor]:
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g
            heapq.heappush(open_set, (tentative_g, neighbor))
    
    best_path = reconstruct_path(came_from, current)
    return current, False, best_path, came_from
