def create_grid():
    """Create a 15x15 grid with enhanced 3D terrain.
    
    Ensures that the start (0,0) and goal (14,14) cells remain clear.
    """
    grid = [[0] * 15 for _ in range(15)]
    heights = [[0.0] * 15 for _ in range(15)]
    
    # Define obstacles and terrain patterns
    obstacles = [
        # Top-left corner maze pattern
        (0, 1), (1, 1), (2, 1), (2, 2), (1, 2),
        (0, 3), (1, 3), (1, 4),
        
        # Top-right corner pattern
        (1, 13), (0, 13), (1, 14), (2, 12),
        (2, 13), (2, 14), (3, 13), (4, 13), (4, 14),
        
        # Bottom-left corner pattern
        (13, 0), (13, 1), (14, 1), (12, 1),
        (12, 2), (13, 2), (14, 3), (13, 3), (13, 4),
        
        # Bottom-right corner pattern
        (13, 13), (13, 14), (12, 12),
        (12, 13), (11, 13), (11, 14),
        
        # Central maze patterns
        (6, 6), (6, 7), (6, 8), (6, 9),
        (7, 6), (8, 6), (8, 7), (8, 8),
        (7, 8), (7, 9), (7, 10),
        
        # Additional obstacles for complexity
        (3, 3), (3, 4), (4, 4), (4, 5),
        (5, 5), (5, 6), (6, 4),
        (10, 2), (11, 2), (12, 2),
        (10, 3), (10, 4), (11, 4),
        (11, 11), (11, 12),
        (9, 1), (9, 2), (9, 3),
        (13, 7), (13, 8), (13, 9),
        (4, 8), (8, 4), (10, 8), (8, 10),
        (5, 13), (13, 5), (7, 12), (12, 7)
    ]
    
    slow_terrain = [
        # Corner alternatives
        (0, 2), (2, 0), (1, 12), (2, 11),
        (12, 0), (11, 1), (12, 14), (14, 12),
        
        # Central patterns
        (5, 7), (5, 8), (5, 9),
        (7, 5), (8, 5), (9, 5),
        (9, 6), (9, 7), (9, 8),
        
        # Alternative paths
        (3, 5), (3, 6), (3, 7),
        (11, 5), (11, 6), (11, 7),
        
        # Strategic spots
        (4, 13), (6, 11), (8, 13),
        (10, 6), (12, 8), (13, 10),
        
        # Additional slow terrain
        (4, 2), (4, 3), (7, 7), (8, 9),
        (10, 10), (11, 9), (2, 4), (2, 5),
        (5, 2), (6, 2), (10, 12), (10, 13),
        (12, 10), (12, 11)
    ]
    
    # Place obstacles and terrain
    for pos in obstacles:
        grid[pos[0]][pos[1]] = 1
        heights[pos[0]][pos[1]] = 1.0
    
    for pos in slow_terrain:
        grid[pos[0]][pos[1]] = 2
        heights[pos[0]][pos[1]] = 0.3
    
    # Ensure start and goal are clear
    grid[0][0] = 0
    grid[14][14] = 0
    heights[0][0] = 0.0
    heights[14][14] = 0.0
    
    return grid, heights
