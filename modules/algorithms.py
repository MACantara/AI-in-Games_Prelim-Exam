import heapq

def heuristic(a, b):
    """Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(pos, grid):
    """Return valid (non-obstacle) neighbor cells with their costs."""
    x, y = pos
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 1:
            cost = 2 if grid[nx][ny] == 2 else 1
            yield ((nx, ny), cost)

def reconstruct_path(came_from, current):
    """Reconstruct the path from start to goal."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def astar_step(grid, start, goal, open_set, closed_set, came_from, g_score):
    """Modified A* step to return current exploration path"""
    if not open_set:
        return None, True, None, {}
    
    current_f, current = heapq.heappop(open_set)
    if current == goal:
        path = reconstruct_path(came_from, current)
        return current, True, path, came_from
    
    closed_set.add(current)
    
    for neighbor, cost in neighbors(current, grid):
        if neighbor in closed_set:
            continue
        
        tentative_g = g_score[current] + cost
        if neighbor not in g_score or tentative_g < g_score[neighbor]:
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g
            f = tentative_g + heuristic(neighbor, goal)
            heapq.heappush(open_set, (f, neighbor))
    
    return current, False, None, came_from

def dijkstra_step(grid, start, goal, open_set, closed_set, came_from, g_score):
    """Modified Dijkstra step to return current exploration path"""
    if not open_set:
        return None, True, None, {}
    
    current_g, current = heapq.heappop(open_set)
    if current == goal:
        path = reconstruct_path(came_from, current)
        return current, True, path, came_from
    
    closed_set.add(current)
    
    for neighbor, cost in neighbors(current, grid):
        if neighbor in closed_set:
            continue
        
        tentative_g = g_score[current] + cost
        if neighbor not in g_score or tentative_g < g_score[neighbor]:
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g
            heapq.heappush(open_set, (tentative_g, neighbor))
    
    return current, False, None, came_from
