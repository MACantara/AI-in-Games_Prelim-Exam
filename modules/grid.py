from typing import List, Tuple

GRID_SIZE: int = 25

def create_grid() -> Tuple[List[List[int]], List[List[float]]]:
    grid: List[List[int]] = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    heights: List[List[float]] = [[0.0] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Define the map based on the provided image
    # '#' represents a wall (1), ' ' or other characters represent open space (0)

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
            else:
                grid[row_index][col_index] = 0 # Explicitly setting open spaces to 0
                heights[row_index][col_index] = 0.0

    return grid, heights

pacman_grid, pacman_heights = create_grid()

# Print the grid (optional)
for row in pacman_grid:
    print("".join(['#' if cell == 1 else ' ' for cell in row]))