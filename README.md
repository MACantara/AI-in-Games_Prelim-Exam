# AI in Games: Pac-Man with AI-Controlled Ghosts

## Project Overview
This project implements a Pac-Man clone with AI-controlled ghosts, demonstrating artificial intelligence concepts in game development. The ghosts use pathfinding algorithms with different personalities to chase the player or flee when vulnerable, creating engaging gameplay that showcases how AI can enhance gaming experiences.

## Table of Contents
- [AI in Games: Pac-Man with AI-Controlled Ghosts](#ai-in-games-pac-man-with-ai-controlled-ghosts)
  - [Project Overview](#project-overview)
  - [Table of Contents](#table-of-contents)
  - [Installation and Setup](#installation-and-setup)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [Gameplay](#gameplay)
  - [Controls](#controls)
  - [AI Implementation](#ai-implementation)
    - [Design Philosophy](#design-philosophy)
    - [Pathfinding Algorithms](#pathfinding-algorithms)
    - [Ghost Behavior](#ghost-behavior)
    - [Decision Making](#decision-making)
    - [AI Optimization Techniques](#ai-optimization-techniques)
  - [Technical Architecture](#technical-architecture)
    - [Module Breakdown](#module-breakdown)
  - [Challenges Faced during Development](#challenges-faced-during-development)
    - [1. Ghost Rendering Challenges](#1-ghost-rendering-challenges)
    - [2. Pathfinding Issues](#2-pathfinding-issues)
    - [3. Ghost Behavior Implementation](#3-ghost-behavior-implementation)
    - [4. Game State Management](#4-game-state-management)
  - [Acknowledgments](#acknowledgments)

## Installation and Setup
### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation Steps
1. Clone or download the repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```

## Gameplay
- **Pac-Man:** The player controls Pac-Man, navigating through a maze, eating pellets, and avoiding ghosts.
- **Ghosts:** AI-controlled ghosts with different behaviors chase Pac-Man. When Pac-Man eats a power pellet, ghosts become vulnerable and can be eaten.

## Controls
- **WASD Keys** or **Arrow Keys:** Move Pac-Man
- **Esc:** Pause/Resume the game
- **R:** Reset the game

## AI Implementation

### Design Philosophy
- **Authentic Recreation:** Implementation closely follows the original Pac-Man ghost behaviors while improving pathfinding reliability.
- **Modular Design:** Each ghost's behavior is encapsulated within its own targeting method, allowing for easy adjustment and extension.
- **Memory Efficiency:** Path calculations are optimized to minimize memory usage while maintaining gameplay responsiveness.
- **Emergent Challenge:** The ghost behaviors are designed to create dynamic gameplay scenarios without explicit coordination.

### Pathfinding Algorithms
- **A\* Search:** Used by ghosts to find the shortest path to Pac-Man, balancing computational efficiency with optimal pathfinding. This algorithm was chosen over alternatives like Dijkstra's because it provides better performance in grid-based environments while maintaining path optimality.
- **Manhattan Distance Heuristic:** Implemented for A* to maintain grid-based movement patterns authentic to the original game. This heuristic was selected to match the four-directional movement constraints of the game world.
- **Path Recalculation Logic:** Ghosts recalculate paths at controlled intervals (every 15 frames) to balance responsiveness with performance. This timing was carefully tuned through playtesting to ensure ghosts react appropriately without causing CPU spikes.
- **Flee Behavior Vector Calculation:** When vulnerable, ghosts use a vector-based flee algorithm with randomization to avoid predictable patterns. The randomization factor (0.2) was specifically chosen to create unpredictable but still believable movement.

### Ghost Behavior
- **Blinky:** Chases Pac-Man directly by targeting the player's current position, becoming more aggressive as the game progresses. This direct approach creates pressure on players and serves as the baseline aggressor.
- **Pinky:** Tries to ambush Pac-Man by targeting 4 tiles ahead of the player's current direction, implementing the classic "look-ahead" strategy. The 4-tile offset was selected through testing to create effective ambush scenarios without making the ghost too predictable.
- **Inky:** Uses a combination of Blinky's position and Pac-Man's position to determine its target. Calculates a pivot point 2 tiles ahead of Pac-Man, then doubles the vector from Blinky to this point. This complex targeting creates unpredictable flanking movements.
- **Clyde:** Alternates between chasing Pac-Man and retreating to a scatter corner based on proximity (switches to scatter mode when within 8 tiles of Pac-Man). The 8-tile threshold was chosen to create a "shy" personality that provides strategic breathing room for players.

### Decision Making
- **State Machine Architecture:** Ghosts operate using a finite state machine with distinct states (chase, scatter, frightened, eaten). This architecture was selected for its clarity, maintainability, and faithful recreation of the original game's behavior.
- **Dynamic Target Selection:** Each ghost type implements custom targeting algorithms that determine movement goals based on current game state. These algorithms are designed to create complementary hunting patterns that challenge the player from multiple angles.
- **Scatter Mode Timing:** Periodic switches to scatter mode force ghosts to temporarily target their home corners, giving players strategic breaks from pursuit. The timing system follows a 27/27/23/23/19/19/15/15 second pattern similar to the original game.
- **Vulnerability Response:** When Pac-Man consumes a power pellet, ghosts enter frightened state with modified pathfinding goals to flee from the player. The flee algorithm incorporates a small random component to prevent predictable escape routes.
- **Path Consistency Management:** To prevent erratic movement, ghosts maintain path consistency counters and delay timers that prevent rapid direction changes. This creates smoother, more believable movement patterns that resemble intelligent entities rather than random agents.

### AI Optimization Techniques
- **Path Caching:** Critical paths are cached to reduce computational overhead during intense gameplay moments. Common paths (like returning to spawn) are prioritized for caching to maximize performance benefits.
- **Selective Recalculation:** Path updates occur only when significant player movement is detected or timers expire. This adaptive approach reduces unnecessary calculations while maintaining responsive ghost behavior.
- **Difficulty Scaling:** Ghost speeds and decision-making accuracy increase as the game progresses, creating an adaptive difficulty curve. Speed increases are implemented in stages (80%, 90%, 100%) based on remaining dots.
- **Coordinated Behavior:** Ghost movement patterns are designed to create emergent cooperative behaviors without explicit communication between agents. This results in natural-feeling encirclement and trapping strategies.

## Technical Architecture
### Module Breakdown
- **/modules/**
  - **agent.py:** Base path-following agent class used by ghosts, implementing path management and movement logic.
  - **algorithms.py:** Implementation of A* pathfinding, heuristic functions, and flee behavior algorithms.
  - **game_state.py:** Core game state management, handling collisions, scoring, and game lifecycle events.
  - **ghost.py:** Ghost AI with distinct behavior patterns (Blinky, Pinky, Inky, Clyde) and rendering.
  - **grid.py:** Maze generation, terrain setup, and spawn point configuration.
  - **player.py:** Pac-Man character controls, animation states, and collision detection.
  - **ui.py:** Visualization system handling rendering, animations, and game UI elements.
- **app.py:** Application entry point and game loop controller.
- **requirements.txt:** Python dependencies.

## Challenges Faced during Development

### 1. Ghost Rendering Challenges
- **Wavy Bottom Animation:** Implementing the classic wavy bottom for ghosts required careful mathematics using sine waves with dynamic offsets. Getting smooth animation that worked at different resolutions was particularly challenging.
- **State-Based Rendering:** Creating different visual states (normal, vulnerable, eaten) required complex rendering logic and careful timing of animation transitions.

### 2. Pathfinding Issues
- **Path Calculation Failures:** Ghosts would sometimes stop moving because no valid path could be calculated, especially in complex maze sections. This required implementing fallback behaviors and path consistency counters.
- **Back-and-Forth Movement:** Ghosts would occasionally get stuck in repetitive back-and-forth patterns due to rapid path recalculations. Solved by adding delay timers and path consistency checks to prevent frequent path changes.

### 3. Ghost Behavior Implementation
- **Return to Spawn Mechanics:** After being eaten, ghosts wouldn't properly return to their spawn points using the A* algorithm. This was fixed by implementing a direct pathfinding mode specifically for the respawn journey.
- **Personality Balancing:** Tuning the different ghost personalities (Blinky, Pinky, Inky, Clyde) to make the game challenging but fair required extensive playtesting and parameter adjustments.

### 4. Game State Management
- **Synchronizing Multiple States:** Managing various game states (normal play, power mode, death sequences, ghost vulnerability) simultaneously required careful timing and state transition management.
- **Performance Optimization:** Frequent path recalculations for multiple ghosts created performance issues, which were addressed by implementing timers to limit recalculation frequency.

## Acknowledgments
This project demonstrates pathfinding concepts using Pygame for visualization. The Pacman-style agents add a gaming element while maintaining educational value.
