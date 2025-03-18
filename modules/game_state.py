from dataclasses import dataclass
from typing import List, Tuple, Optional
from .ghost import Ghost
from .grid import create_grid

@dataclass
class GameState:
    """Manages the game's state and logic."""
    grid: List[List[int]]
    player_pos: List[int]
    player_direction: Tuple[int, int]
    ghosts: List[Ghost]
    score: int = 0
    ghost_release_times: List[int] = None
    game_timer: int = 0
    scatter_timer: int = 0
    debug_mode: bool = False
    game_over: bool = False  # Flag for game over state
    lives: int = 3  # Number of player lives
    
    def __post_init__(self):
        if self.ghost_release_times is None:
            self.ghost_release_times = [0, 300, 600, 900]
    
    @classmethod
    def create_new_game(cls) -> 'GameState':
        """Create a new game state with initial positions."""
        grid, _ = create_grid()
        player_pos = [18, 11]  # Starting position
        player_direction = (0, 0)
        
        # Initialize ghosts
        ghosts = [
            Ghost((11, 9), 'blinky'),
            Ghost((11, 10), 'inky'),
            Ghost((11, 12), 'pinky'),
            Ghost((11, 13), 'clyde'),
        ]
        
        return cls(
            grid=grid,
            player_pos=player_pos,
            player_direction=player_direction,
            ghosts=ghosts
        )
    
    def update(self) -> None:
        """Update game state for one frame."""
        if self.game_over:
            return
            
        self.game_timer += 1
        self.scatter_timer = (self.scatter_timer + 1) % 400
        
        # Update ghost states
        scatter_mode = self.scatter_timer >= 200
        for i, release_time in enumerate(self.ghost_release_times):
            if self.game_timer >= release_time and not self.ghosts[i].active:
                self.ghosts[i].active = True
                
        for ghost in self.ghosts:
            if ghost.active:
                ghost.scatter_mode = scatter_mode
                
        # Check for collision with ghosts
        self._check_ghost_collisions()
    
    def _check_ghost_collisions(self) -> None:
        """Check if player has collided with any ghost."""
        player_pos = tuple(self.player_pos)
        for ghost in self.ghosts:
            if ghost.active and ghost.pos == player_pos:
                self._handle_ghost_collision()
                break
    
    def _handle_ghost_collision(self) -> None:
        """Handle what happens when player collides with ghost."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            self._reset_positions()
    
    def _reset_positions(self) -> None:
        """Reset player and ghost positions after losing a life."""
        # Reset player position
        self.player_pos = [18, 11]  # Starting position
        self.player_direction = (0, 0)
        
        # Reset ghosts
        for ghost in self.ghosts:
            ghost.reset_to_start()
            ghost.active = False
            
        # Reset timers
        self.game_timer = 0
