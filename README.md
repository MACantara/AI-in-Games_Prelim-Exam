# AI in Games Prelim Exam - Pathfinding Visualization

## Overview
This project demonstrates a side-by-side pathfinding visualization tool using A* and Dijkstra algorithms. It is designed for educational purposes to illustrate how different pathfinding techniques work in complex terrain environments. The visualization uses Pygame to create an interactive and engaging display with Pacman-style agents.

## Why This Project?
- **Educational Value:** Illustrates core pathfinding algorithms and heuristic search methods.
- **Visualization:** Provides an intuitive 2D view with animated agents and clear visual feedback.
- **Comparison:** Enables direct side-by-side performance comparisons between A* and Dijkstra.

## How It Works
- **Grid and Terrain Generation:** The grid is generated with obstacles and slow terrain cells while ensuring the start and goal remain clear.
- **Algorithm Steps:** Both A* and Dijkstra algorithms perform incremental steps with their current best candidate paths visualized.
- **Visual Feedback:** Pacman-style agents move through the discovered paths, with mouth animations and proper directional facing.
- **Performance Metrics:** Real-time display of execution time, path length, and nodes explored for both algorithms.

## Setting Up the Local Development Environment
### Prerequisites
- Python 3.x
- pip
- Visual Studio Code (recommended)

### Installation Steps
1. Clone or download the repository
2. Create and activate a virtual environment:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
3. Install the required packages:
    ```
    pip install -r requirements.txt
    ```
4. Run the application:
    ```
    python app.py
    ```

## Features
- Side-by-side visualization of A* and Dijkstra pathfinding
- Animated Pacman agents that follow discovered paths
- Real-time performance metrics and comparison
- Interactive controls (Start/Pause/Reset)
- Color-coded visualization of:
  - Walls and obstacles
  - Slow terrain
  - Visited nodes
  - Final paths
  - Start and goal positions

## Controls
- **Space:** Start/Pause the simulation
- **R:** Reset both algorithms
- UI buttons for easy interaction

## Project Structure
- **/modules/**
  - **algorithms.py:** Implementation of A* and Dijkstra algorithms
  - **agent.py:** Pacman agent logic and movement
  - **grid.py:** Maze generation and terrain setup
  - **visualizer.py:** Main visualization and UI components
- **app.py:** Application entry point
- **requirements.txt:** Python dependencies

## Implementation Details
### Visualization
- Uses Pygame for rendering
- Animations for pathfinding agents
- Color-coded grid cells for different terrain types
- Clear visual distinction between algorithms' progress

### Pathfinding Algorithms
- **A* Search:** Uses Manhattan distance heuristic
- **Dijkstra:** Implements uniform cost search
- Both algorithms provide:
  - Step-by-step visualization
  - Node exploration tracking
  - Path reconstruction
  - Performance metrics

## Common Issues and Solutions
### Display Issues
- **Problem:** Window not appearing or incorrect sizing
- **Solution:** Check monitor resolution settings and Pygame installation

### Performance
- **Problem:** Slow animation or response
- **Solution:** Adjust animation speed in visualizer settings

## Acknowledgments
This project demonstrates pathfinding concepts using Pygame for visualization. The Pacman-style agents add a gaming element while maintaining educational value.
