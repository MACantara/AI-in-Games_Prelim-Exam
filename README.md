# AI in Games Prelim Exam - 3D Pathfinding Visualization

## Overview
This project demonstrates a 3D pathfinding visualization tool using A* and Dijkstra algorithms. It is designed for educational purposes to illustrate how different pathfinding techniques work in complex terrain environments. The visualization uses Pygame and PyOpenGL for rendering and interactive controls.

## Why This Project?
- **Educational Value:** Illustrates core pathfinding algorithms and heuristic search methods.
- **Visualization:** Provides a 3D interactive view of maze generation and algorithm exploration.
- **Comparison:** Enables direct side-by-side performance comparisons between A* and Dijkstra.

## How It Works
- **Grid and Terrain Generation:** The grid is generated with obstacles and slow terrain cells while ensuring the start and goal remain clear.
- **Algorithm Steps:** Both A* and Dijkstra algorithms perform incremental steps with their current best candidate paths visualized in 3D.
- **User Interaction:** Users can start/pause the algorithms, reset the maze, and save an image of the current map directly from the UI.

## Setting Up the Local Development Environment
### Prerequisites
- Python 3.x
- pip
- Visual Studio Code installed
- Command Prompt (cmd) on Windows

### Installation Steps
1. Clone or download the repository into `/c:/Programming_Projects/AI-in-Games_Prelim-Exam`.
2. Open Visual Studio Code and open the folder `c:/Programming_Projects/AI-in-Games_Prelim-Exam`.
3. Open the integrated terminal in VS Code by pressing ``Ctrl+` `` (To the left of number 1 key on the top of the keyboard):
   - Click the dropdown icon next to the plus (+) icon at the top-right of the Terminal panel.
   - When prompted, select "Command Prompt" to open a new terminal using cmd.
4. In the integrated terminal, navigate to the project directory:
    ```
    cd c:/Programming_Projects/AI-in-Games_Prelim-Exam
    ```
5. Create and activate a virtual environment:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
6. Install the required packages using pip:
    ```
    pip install -r requirements.txt
    ```
7. Run the application:
    ```
    python app.py
    ```

## Common Issues and Solutions
### OpenGL or Rendering Issues
- **Problem:** Errors related to OpenGL or GLU.
- **Solution:** Ensure your graphics drivers are updated and that your hardware supports OpenGL.

### Missing Dependencies
- **Problem:** Import errors or missing modules.
- **Solution:** Verify that all dependencies are installed using `pip install -r requirements.txt`.

### Performance and Responsiveness
- **Problem:** Application lag or freezing.
- **Solution:** Reduce grid size or check the system resource usage; ensure your machine meets the graphical requirements.

### File Saving Issues
- **Problem:** Image not saved or I/O errors.
- **Solution:** Check that the application has write permissions for the project directory and monitor console output for error messages.

## Project Structure
- **/modules:** Contains core functionality including maze generation, pathfinding algorithms, agent control, and visualization.
- **app.py:** Entry point to run the visualization.
- **requirements.txt:** Lists all Python package dependencies.
- **README.md:** This file with comprehensive documentation.

## Pathfinding Report

### Map Analysis
- **Grid and Terrain:** The map (see [modules/grid.py](#file:grid.py)) is a 15x15 grid that includes obstacles (walls) and slow terrain cells. Obstacles are purposefully placed to create challenging paths, while slow terrain imposes a higher traversal cost.
- **Key Locations:** The start and goal positions are explicitly marked and kept clear to ensure a valid path exists. These provide fixed reference points for both algorithms.

### A* Search Solution
- **Module:** Refer to [modules/algorithms.py](#file:algorithms.py).
- **Heuristic:** The Manhattan distance is used to estimate the cost from any cell to the goal.
- **Process:** 
  - The algorithm maintains an open list (priority queue) and a closed set.
  - For each selected node, it calculates the tentative cost (g_cost) and adds the heuristic to form the f_cost.
  - Once the goal is reached, the final path is reconstructed using a "came_from" map.
- **Visual Aids:** Use screenshots from the visualizer ([modules/visualizer.py](#file:visualizer.py)) that showcase the progress of node exploration and the final highlighted path.

### Dijkstra's Solution
- **Module:** Also implemented in [modules/algorithms.py](#file:algorithms.py).
- **Cost Calculation:** Uses only cumulative costs without adding a heuristic, ensuring each node's cost is determined solely by the traversal path.
- **Process:**
  - Maintains a similar open and closed system as A*.
  - Updates costs based purely on traversal, leading to potentially more nodes being explored.
  - The final path is similarly reconstructed through the "came_from" mapping.
- **Visual Aids:** Compare the progression and final paths with those generated by A*, highlighting differences in node exploration and path choices.

### Comparison and Analysis
- **Performance:** Compare metrics such as the number of nodes explored and path length between A* and Dijkstra's. The visualization displays "A* Nodes Processed" and "Dijkstra Nodes Processed" in real time, providing insight into the computational work done by each algorithm.
- **Efficiency:** Discuss how the heuristic in A* reduces the number of nodes processed compared to Dijkstra's exhaustive search.
- **Observations:** Note that the lower count of processed nodes in A* typically correlates with a faster search, especially in complex grids.

## Conclusion
This project is intended to serve as a hands-on tool for understanding pathfinding in a 3D environment. It combines visual feedback with algorithmic exploration, making it a useful resource for both learning and demonstration purposes. For additional questions or support, refer to this README or contact the project maintainer.
