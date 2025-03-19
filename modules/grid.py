from typing import List, Tuple

GRID_SIZE: int = 25

def create_grid() -> Tuple[List[List[int]], List[List[float]], Tuple[int, int], List[Tuple[int, int]]]:
    grid: List[List[int]] = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    heights: List[List[float]] = [[0.0] * GRID_SIZE for _ in range(GRID_SIZE)]
    player_spawn: Tuple[int, int] = (0, 0)  # Default value, will be overwritten
    ghost_spawns: List[Tuple[int, int]] = []  # List to store ghost spawn points

    # Define the map based on the provided image
    # '#' represents a wall (1), ' ' or other characters represent open space (0)
    # '*' represents dots (2), '@' represents power pellets/fruits (3)

    map_data = [
        "#######################",
        "#**********#**********#",
        "#@###*####*#*####*###@#",
        "#*###*####*#*####*###*#",
        "#*********************#",
        "#*###*# ####### #*###*#",
        "#*****# ####### #*****#",
        "#####*#         #*#####",
        "#####*#### # ####*#####",
        "#####*#         #*#####",
        "#####*# ### ### #*#####",
        "#    *  #MM MM#  *    #",
        "#####*# ####### #*#####",
        "#####*#         #*#####",
        "#####*# ####### #*#####",
        "#####*# ####### #*#####",
        "#**********#**********#",
        "#*###*####*#*####*###*#",
        "#@**#******C******#**@#",
        "###*#*#*#######*#*#*###",
        "#*****#****#****#*****#",
        "#*########*#*########*#",
        "#*########*#*########*#",
        "#*********************#",
        "#######################"
    ]

    for row_index, row_data in enumerate(map_data):
        if row_index >= GRID_SIZE:
            break  # Stop if we exceed grid size
        for col_index, cell_data in enumerate(row_data):
            if col_index >= GRID_SIZE:
                break # Stop if we exceed grid size
            if cell_data == '#':
                grid[row_index][col_index] = 1
                heights[row_index][col_index] = 1.0
            elif cell_data == '*':
                grid[row_index][col_index] = 2  # 2 represents points
                heights[row_index][col_index] = 0.0
            elif cell_data == '@':
                grid[row_index][col_index] = 3  # 3 represents power pellets/fruits
                heights[row_index][col_index] = 0.0
            elif cell_data == 'C':
                # 'C' represents the player spawn point
                player_spawn = (row_index, col_index)
                grid[row_index][col_index] = 0  # Treat as empty space
                heights[row_index][col_index] = 0.0
            elif cell_data == 'M':
                # 'M' represents ghost spawn points
                ghost_spawns.append((row_index, col_index))
                grid[row_index][col_index] = 0  # Treat as empty space
                heights[row_index][col_index] = 0.0
            else:
                grid[row_index][col_index] = 0 # Explicitly setting open spaces to 0
                heights[row_index][col_index] = 0.0

    return grid, heights, player_spawn, ghost_spawns

# Return all grid-related data
pacman_grid, pacman_heights, pacman_spawn, ghost_spawns = create_grid()

# Print the grid (optional)
for row in pacman_grid:
    print("".join(['#' if cell == 1 else ' ' for cell in row]))