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

### Installation Steps
1. Clone or download the repository into `/c:/Programming_Projects/AI-in-Games_Prelim-Exam`.
2. Open a terminal and navigate to the project directory:
    ```
    cd /c:/Programming_Projects/AI-in-Games_Prelim-Exam
    ```
3. (Optional) Create and activate a virtual environment:
    ```
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```
4. Install the required packages using pip:
    ```
    pip install -r requirements.txt
    ```
5. Run the application:
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

## Conclusion
This project is intended to serve as a hands-on tool for understanding pathfinding in a 3D environment. It combines visual feedback with algorithmic exploration, making it a useful resource for both learning and demonstration purposes. For additional questions or support, refer to this README or contact the project maintainer.
