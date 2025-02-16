from typing import List, Tuple

GRID_SIZE: int = 25  # Increased grid size
START: Tuple[int, int] = (1, 12)
GOAL: Tuple[int, int] = (23, 12)

def create_grid() -> Tuple[List[List[int]], List[List[float]]]:
    """
    Create a 25x25 grid resembling the Pacman maze.
    """
    grid: List[List[int]] = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    heights: List[List[float]] = [[0.0] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Define wall positions to resemble Pacman maze.
    walls = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24),
        (1, 0), (1, 4), (1, 7), (1, 12), (1, 17), (1, 20), (1, 24),
        (2, 0), (2, 2), (2, 3), (2, 4), (2, 6), (2, 7), (2, 8), (2, 12), (2, 16), (2, 17), (2, 18), (2, 20), (2, 21), (2, 22), (2, 24),
        (3, 0), (3, 2), (3, 4), (3, 12), (3, 20), (3, 22), (3, 24),
        (4, 0), (4, 1), (4, 2), (4, 4), (4, 5), (4, 6), (4, 8), (4, 9), (4, 10),  (4, 12), (4, 14), (4, 15), (4, 16), (4, 20), (4, 21), (4, 22), (4, 23), (4, 24),
        (5, 0), (5, 2), (5, 8), (5, 12), (5, 16), (5, 22), (5, 24),
        (6, 0), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 8), (6, 9), (6, 10), (6, 12),  (6, 14), (6, 15), (6, 16), (6, 18), (6, 19), (6, 20), (6, 22), (6, 24),
        (7, 0), (7, 12), (7, 24),
        (8, 0), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 8), (8, 9), (8, 10),  (8, 12), (8, 14), (8, 15), (8, 16), (8, 18), (8, 19), (8, 20), (8, 22), (8, 24),
        (9, 0), (9, 2), (9, 8), (9, 12), (9, 16), (9, 22), (9, 24),
        (10, 0), (10, 1), (10, 2), (10, 4), (10, 5), (10, 6), (10, 8), (10, 9), (10, 10), (10, 12), (10, 14), (10, 15), (10, 16), (10, 20), (10, 21), (10, 22), (10, 23), (10, 24),
        (11, 0), (11, 2), (11, 4), (11, 12), (11, 20), (11, 22), (11, 24),
        (12, 0), (12, 2), (12, 3), (12, 4), (12, 6), (12, 7), (12, 8), (12, 12), (12, 16), (12, 17), (12, 18), (12, 20), (12, 21), (12, 22), (12, 24),
        (13, 0), (13, 4), (13, 7), (13, 12), (13, 17), (13, 20), (13, 24),
        (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20), (14, 21), (14, 22), (14, 23), (14, 24),
        (15, 0), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 8), (15, 9), (15, 10), (15, 12), (15, 14), (15, 15), (15, 16), (15, 18), (15, 19), (15, 20), (15, 22), (15, 24),
        (16, 0), (16, 2), (16, 8), (16, 12), (16, 16), (16, 22), (16, 24),
        (17, 0), (17, 1), (17, 2), (17, 4), (17, 5), (17, 6), (17, 8), (17, 9), (17, 10), (17, 12), (17, 14), (17, 15), (17, 16), (17, 20), (17, 21), (17, 22), (17, 23), (17, 24),
        (18, 0), (18, 2), (18, 4), (18, 12), (18, 20), (18, 22), (18, 24),
        (19, 0), (19, 2), (19, 3), (19, 4), (19, 6), (19, 7), (19, 8), (19, 12), (19, 16), (19, 17), (19, 18), (19, 20), (19, 21), (19, 22), (19, 24),
        (20, 0), (20, 4), (20, 7), (20, 12), (20, 17), (20, 20), (20, 24),
        (21, 0), (21, 1), (21, 2), (21, 3), (21, 4), (21, 5), (21, 6), (21, 7), (21, 8), (21, 9), (21, 10), (21, 11), (21, 12), (21, 13), (21, 14), (21, 15), (21, 16), (21, 17), (21, 18), (21, 19), (21, 20), (21, 21), (21, 22), (21, 23), (21, 24),
        (22, 0), (22, 12), (22, 24),
        (23, 0), (23, 1), (23, 2), (23, 3), (23, 4), (23, 5), (23, 6),  (23, 7), (23, 8), (23, 9), (23, 10), (23, 11), (23, 12), (23, 13), (23, 14), (23, 15), (23, 16), (23, 17), (23, 18), (23, 19), (23, 20), (23, 21), (23, 22), (23, 23), (23, 24),
        (24, 0), (24, 1), (24, 2), (24, 3), (24, 4), (24, 5), (24, 6), (24, 7), (24, 8), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18), (24, 19), (24, 20), (24, 21), (24, 22), (24, 23), (24, 24)
    ]

    for pos in walls:
        grid[pos[0]][pos[1]] = 1
        heights[pos[0]][pos[1]] = 1.0

    # Ensure START and GOAL are clear.
    grid[START[0]][START[1]] = 0
    grid[GOAL[0]][GOAL[1]] = 0
    heights[START[0]][START[1]] = 0.0
    heights[GOAL[0]][GOAL[1]] = 0.0

    return grid, heights
