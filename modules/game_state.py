from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable
from .ghost import Ghost
from .grid import create_grid

@dataclass
class GameState:
    """Manages the game's state and logic."""
    grid: List[List[int]]
    player_pos: List[int]
    player_direction: Tuple[int, int]
    ghosts: List[Ghost]
    player_spawn_pos: Tuple[int, int]  # Store the spawn position
    score: int = 0
    ghost_release_times: List[int] = None
    game_timer: int = 0
    scatter_timer: int = 0
    debug_mode: bool = False
    game_over: bool = False  # Flag for game over state
    lives: int = 3  # Number of player lives
    dying: bool = False  # Flag for death animation
    death_timer: int = 0  # Timer for death animation
    death_animation_length: int = 90  # Length of death animation in frames (3 seconds at 30fps)
    death_callback: Optional[Callable] = field(default=None, repr=False)
    respawn_callback: Optional[Callable] = field(default=None, repr=False)
    power_active: bool = False
    power_timer: int = 0
    power_duration: int = 300  # 10 seconds at 30fps
    ghost_points: int = 200  # Base points for eating a ghost
    ghost_points_multiplier: int = 1  # Multiplier increases with each ghost eaten
    fruit_eaten_callback: Optional[Callable] = field(default=None, repr=False)
    ghost_eaten_callback: Optional[Callable] = field(default=None, repr=False)
    power_just_ended: bool = False  # Add this flag to track when power mode just ended
    
    def __post_init__(self):
        if self.ghost_release_times is None:
            self.ghost_release_times = [0, 300, 600, 900]
    
    @classmethod
    def create_new_game(cls) -> 'GameState':
        """Create a new game state with initial positions."""
        grid, _, player_spawn, ghost_spawns = create_grid()
        player_pos = list(player_spawn)  # Use spawn position from grid
        player_direction = (0, 0)
        
        # Use ghost spawn points from grid, or fallback to defaults if not enough spawn points
        # Default ghost positions as fallback
        default_ghost_positions = [(11, 9), (11, 10), (11, 12), (11, 13)]
        
        # Map ghost positions to the available spawn points
        ghost_positions = []
        for i in range(4):  # We need 4 ghosts
            if i < len(ghost_spawns):
                ghost_positions.append(ghost_spawns[i])
            else:
                ghost_positions.append(default_ghost_positions[i])
        
        # Initialize ghosts at their spawn positions
        ghosts = [
            Ghost(ghost_positions[0], 'blinky'),
            Ghost(ghost_positions[1], 'inky'),
            Ghost(ghost_positions[2], 'pinky'),
            Ghost(ghost_positions[3], 'clyde'),
        ]
        
        return cls(
            grid=grid,
            player_pos=player_pos,
            player_direction=player_direction,
            ghosts=ghosts,
            player_spawn_pos=player_spawn
        )
    
    def update(self) -> None:
        """Update game state for one frame."""
        # Reset the power_just_ended flag at the start of each frame
        self.power_just_ended = False
        
        # Handle death animation even in game over state
        if self.dying:
            self.death_timer += 1
            if self.death_timer >= self.death_animation_length:
                self.dying = False
                self.death_timer = 0
                
                # Only reset positions if we still have lives
                if not self.game_over:
                    self._reset_positions()
                    # Call respawn callback after reset
                    if self.respawn_callback:
                        self.respawn_callback()
            return
            
        # Skip other updates if game over
        if self.game_over:
            return
        
        self.game_timer += 1
        self.scatter_timer = (self.scatter_timer + 1) % 400
        
        # Update power mode timer
        if self.power_active:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_active = False
                self.power_just_ended = True  # Set flag when power mode just ended
                self.ghost_points_multiplier = 1
                # Reset ghost vulnerability
                for ghost in self.ghosts:
                    ghost.vulnerable = False
                    ghost.vulnerable_flash = False
        
        # Update ghost states
        for ghost in self.ghosts:
            if ghost.active and not ghost.eaten:
                ghost.update(self.power_active)
        
        # Update ghost states
        scatter_mode = self.scatter_timer >= 200
        for i, release_time in enumerate(self.ghost_release_times):
            if self.game_timer >= release_time and not self.ghosts[i].active:
                self.ghosts[i].active = True
                
        # Update ghost states - Modified to handle all active ghosts, including eaten ones
        for ghost in self.ghosts:
            if ghost.active:  # Remove the condition checking if not eaten
                # Update the ghost state, and get a bool indicating if it just respawned
                just_respawned = ghost.update(self.power_active)
                
                # If a ghost just respawned, we need to force a path recalculation immediately
                if just_respawned:
                    # Force recalculation of its path in the next update cycle
                    ghost.path = []
                
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
                if self.power_active and ghost.vulnerable and not ghost.eaten:
                    # Eat the ghost
                    self._handle_ghost_eaten(ghost)
                elif not ghost.eaten:
                    # Player gets eaten
                    self._handle_ghost_collision()
                break
    
    def set_death_callback(self, callback: Callable) -> None:
        """Set callback function to be called when player dies."""
        self.death_callback = callback
        
    def set_respawn_callback(self, callback: Callable) -> None:
        """Set callback function to be called when player respawns after death."""
        self.respawn_callback = callback
    
    def set_fruit_eaten_callback(self, callback: Callable) -> None:
        """Set callback function to be called when player eats a power fruit."""
        self.fruit_eaten_callback = callback
        
    def set_ghost_eaten_callback(self, callback: Callable) -> None:
        """Set callback function to be called when player eats a ghost."""
        self.ghost_eaten_callback = callback
    
    def _handle_ghost_collision(self) -> None:
        """Handle what happens when player collides with ghost."""
        self.lives -= 1
        
        # Call death callback if set
        if self.death_callback:
            self.death_callback()
            
        # Start death animation in either case
        self.dying = True
        self.death_timer = 0
        # Freeze ghosts during animation
        for ghost in self.ghosts:
            ghost.active = False
            
        # Set game over flag if needed
        if self.lives <= 0:
            self.game_over = True
    
    def _handle_ghost_eaten(self, ghost: 'Ghost') -> None:
        """Handle the player eating a vulnerable ghost."""
        # Calculate points (200, 400, 800, 1600)
        points = self.ghost_points * self.ghost_points_multiplier
        self.score += points
        self.ghost_points_multiplier *= 2
        
        # Mark ghost as eaten - the movement back to spawn will be handled in update_all_ghosts
        ghost.get_eaten()
        
        # Call callback if set
        if self.ghost_eaten_callback:
            self.ghost_eaten_callback()
    
    def _move_and_collect_item(self, new_pos: List[int]) -> None:
        """Move player to new position and collect items there."""
        row, col = new_pos
        
        # Check for dot
        if self.grid[row][col] == 2:
            self.grid[row][col] = 0
            self.score += self.dot_points
            
        # Check for power pellet/fruit
        elif self.grid[row][col] == 3:
            self.grid[row][col] = 0
            self.score += self.power_pellet_points
            self._activate_power_mode()
            # Call fruit eaten callback
            if self.fruit_eaten_callback:
                self.fruit_eaten_callback()
                
        # Update position
        self.player_pos = new_pos
    
    def _activate_power_mode(self) -> None:
        """Activate the power mode where ghosts are vulnerable."""
        self.power_active = True
        self.power_timer = self.power_duration
        self.ghost_points_multiplier = 1
        
        # Make all active ghosts vulnerable
        for ghost in self.ghosts:
            if ghost.active and not ghost.eaten:
                ghost.make_vulnerable(self.power_duration)
    
    def _reset_positions(self) -> None:
        """Reset player and ghost positions after losing a life."""
        # Reset player position to spawn point
        self.player_pos = list(self.player_spawn_pos)
        self.player_direction = (0, 0)
        
        # Reset ghosts
        for ghost in self.ghosts:
            ghost.reset_to_start()
            ghost.active = False
            
        # Reset timers
        self.game_timer = 0
