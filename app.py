import pygame
import os
from typing import Tuple, Optional
from modules.game_state import GameState
from modules.algorithms import astar_path
from modules.player import Player
from modules.ghost import Ghost
from modules.ui import UI

class PacmanGame:
    def __init__(self, cell_size: int = 30):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer for audio
        self.cell_size = cell_size
        self.width = 23 * cell_size
        self.height = 25 * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pacman with AI Enemies")
        self.clock = pygame.time.Clock()
        
        # Game states
        self.in_startup = True
        self.state = None
        self.ghost_move_delay = 0
        self.player = None
        self.ui = UI(self.screen, self.cell_size)
        
        # Audio setup
        self.audio_paths = {
            'startup': os.path.join(os.path.dirname(__file__), "static/audio/start-up.mp3"),
            'eating': os.path.join(os.path.dirname(__file__), "static/audio/pac-man-eatting.mp3"),
            'dying': os.path.join(os.path.dirname(__file__), "static/audio/pac-man-dying.mp3"),
            'fruit': os.path.join(os.path.dirname(__file__), "static/audio/pac-man-eatting-fruit.mp3"),
            'ghost_scared': os.path.join(os.path.dirname(__file__), "static/audio/ghost-scared.mp3"),
            'ghost_eaten': os.path.join(os.path.dirname(__file__), "static/audio/pac-man-eatting-ghost.mp3")
        }
        self.sound_effects = {}
        self._load_sound_effects()
        
        # Play startup music
        self._play_startup_music()
    
    def _play_startup_music(self):
        """Play the startup music and prepare for game start."""
        if os.path.exists(self.audio_paths['startup']):
            pygame.mixer.music.load(self.audio_paths['startup'])
            pygame.mixer.music.play()
        else:
            print(f"Warning: Could not find startup music at {self.audio_paths['startup']}")
            self.in_startup = False  # Skip startup if music file doesn't exist
            self._init_game()
    
    def _play_eating_sound_loop(self):
        """Play the eating sound on loop after startup finishes."""
        if os.path.exists(self.audio_paths['eating']):
            pygame.mixer.music.load(self.audio_paths['eating'])
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        else:
            print(f"Warning: Could not find eating sound at {self.audio_paths['eating']}")
    
    def _load_sound_effects(self):
        """Load sound effects that aren't played as music."""
        try:
            # Load death sound
            if os.path.exists(self.audio_paths['dying']):
                self.sound_effects['dying'] = pygame.mixer.Sound(self.audio_paths['dying'])
                # Get the length of the death sound to sync with animation
                self.dying_sound_length = int(self.sound_effects['dying'].get_length() * 30)  # Convert seconds to frames at 30fps
            else:
                print(f"Warning: Could not find dying sound at {self.audio_paths['dying']}")
                self.dying_sound_length = 90  # Default length in frames
                
            # Load fruit eating sound
            if os.path.exists(self.audio_paths['fruit']):
                self.sound_effects['fruit'] = pygame.mixer.Sound(self.audio_paths['fruit'])
            else:
                print(f"Warning: Could not find fruit eating sound at {self.audio_paths['fruit']}")
                
            # Load ghost scared (vulnerability) sound
            if os.path.exists(self.audio_paths['ghost_scared']):
                self.sound_effects['ghost_scared'] = pygame.mixer.Sound(self.audio_paths['ghost_scared'])
                # Calculate power duration as twice the length of ghost_scared sound (in frames)
                ghost_scared_length_secs = self.sound_effects['ghost_scared'].get_length()
                self.ghost_scared_frames = int(ghost_scared_length_secs * 30)  # Convert seconds to frames at 30fps
                self.power_duration = self.ghost_scared_frames * 2  # Two complete plays
            else:
                print(f"Warning: Could not find ghost scared sound at {self.audio_paths['ghost_scared']}")
                self.ghost_scared_frames = 300  # Default fallback (10 seconds at 30fps)
                self.power_duration = 600  # Default to 20 seconds if sound file missing
                
            # Load ghost eaten sound
            if os.path.exists(self.audio_paths['ghost_eaten']):
                self.sound_effects['ghost_eaten'] = pygame.mixer.Sound(self.audio_paths['ghost_eaten'])
            else:
                print(f"Warning: Could not find ghost eaten sound at {self.audio_paths['ghost_eaten']}")
                
        except pygame.error as e:
            print(f"Error loading sound: {e}")
            self.dying_sound_length = 90  # Default length in frames
            self.ghost_scared_frames = 300
            self.power_duration = 600
    
    def _init_game(self):
        """Initialize the game state and player."""
        self.state = GameState.create_new_game()
        # Set the death animation length based on the sound effect length
        self.state.death_animation_length = self.dying_sound_length
        # Set power duration based on ghost scared sound length
        self.state.power_duration = self.power_duration
        self.state.set_death_callback(self._on_player_death)
        self.state.set_respawn_callback(self._on_player_respawn)
        self.state.set_fruit_eaten_callback(self._on_fruit_eaten)
        self.state.set_ghost_eaten_callback(self._on_ghost_eaten)
        self.player = Player(self.state.player_pos)
        self.ghost_move_delay = 0
        # Start the eating sound loop when the game begins
        self._play_eating_sound_loop()

    def handle_input(self) -> bool:
        """Handle user input. Returns False if game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.in_startup:
                # Only check if music has ended, ignore key presses during startup
                if not pygame.mixer.music.get_busy():
                    self.in_startup = False
                    self._init_game()
                # Ignore keypresses during startup
            else:
                # Regular game input handling - ignore during dying animation
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        self.state.debug_mode = not self.state.debug_mode
                    elif event.key == pygame.K_r and self.state.game_over and not self.state.dying:
                        self._restart_game()
                    elif not self.state.game_over and not self.state.dying:
                        self.player.handle_key_input(event.key)
        return True
    
    def _on_player_death(self):
        """Callback for when player dies - play death sound."""
        # Stop the eating sound
        pygame.mixer.music.stop()
        
        # Play death sound if available
        if 'dying' in self.sound_effects:
            self.sound_effects['dying'].play()
    
    def _on_player_respawn(self):
        """Callback for when player respawns after death - restart eating sound and update player position."""
        # Update player position to match the state's reset position
        self.player.pos = self.state.player_pos.copy()
        
        # If power mode is active, play ghost scared sound
        if self.state.power_active:
            if 'ghost_scared' in self.sound_effects:
                pygame.mixer.music.load(self.audio_paths['ghost_scared'])
                pygame.mixer.music.play(-1)  # Loop
        else:
            # Otherwise play normal eating sound
            self._play_eating_sound_loop()
        
    def _on_fruit_eaten(self):
        """Callback for when player eats a power fruit."""
        # Stop the normal eating sound
        pygame.mixer.music.stop()
        
        # Play fruit eating sound effect
        if 'fruit' in self.sound_effects:
            self.sound_effects['fruit'].play()
            
        # Start the ghost scared sound in a loop
        if 'ghost_scared' in self.sound_effects:
            pygame.mixer.music.load(self.audio_paths['ghost_scared'])
            pygame.mixer.music.play(-1)  # Loop until power mode ends

    def _on_ghost_eaten(self):
        """Callback for when player eats a ghost."""
        # Play ghost eaten sound
        if 'ghost_eaten' in self.sound_effects:
            self.sound_effects['ghost_eaten'].play()
        
    def _restart_game(self) -> None:
        """Restart the game after game over."""
        # Reset to startup state
        self.in_startup = True
        self.state = None
        self.player = None
        
        # Stop any currently playing sounds
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        
        # Play startup music again
        self._play_startup_music()
        
        # Note: The game will be initialized after startup music finishes in the update method
        # This ensures the same startup flow as when the game first launches
        
    def update(self) -> None:
        """Update game state."""
        if self.in_startup:
            # Check if startup music has finished
            if not pygame.mixer.music.get_busy():
                self.in_startup = False
                self._init_game()
            return
        
        # Update player position and collect dots - but not if game is over
        if not self.state.game_over:
            # Store position before movement to check if we moved
            old_pos = self.player.pos.copy()
            
            # Update player position
            self.player.update_position(self.state.grid, self.state.dying)
            
            # Update game state with current player position and direction
            self.state.player_pos = self.player.pos
            self.state.player_direction = self.player.direction
            
            # Check if player ate a power pellet
            if old_pos != self.player.pos:  # Only check if player actually moved
                row, col = self.player.pos
                if old_pos != self.player.pos and self.player.just_ate_power_pellet:
                    self.player.just_ate_power_pellet = False
                    self.state._activate_power_mode()
                    # Call fruit eaten callback
                    if self.state.fruit_eaten_callback:
                        self.state.fruit_eaten_callback()
        
        # Update ghost positions
        self.ghost_move_delay = (self.ghost_move_delay + 1) % 6
        if self.ghost_move_delay == 0:
            Ghost.update_all_ghosts(
                self.state.ghosts, 
                self.state.grid,
                tuple(self.state.player_pos),
                self.state.player_direction
            )
        
        self.state.update()
        
        # Check if power mode just ended (to restart normal eating sound)
        if self.state.power_just_ended and not self.state.dying:
            # Explicitly stop any currently playing music
            pygame.mixer.music.stop()
            # Start the normal eating sound
            self._play_eating_sound_loop()
        
    def render(self) -> None:
        """Render the game state using the UI handler."""
        if self.in_startup:
            self._draw_startup_screen()
        else:
            self.ui.render_game(
                self.state.grid,
                self.player,
                self.state.ghosts,
                self.state.debug_mode,
                self.state.game_over,
                self.state.lives,
                self.state.dying,
                self.state.death_timer,
                self.state.death_animation_length
            )
    
    def _draw_startup_screen(self) -> None:
        """Draw the game grid and entities while startup music plays."""
        # If game state isn't initialized yet, create it temporarily for drawing
        if not self.state:
            temp_state = GameState.create_new_game()
            temp_player = Player(temp_state.player_pos)
            # Draw the game grid and entities
            self.ui.render_game(
                temp_state.grid,
                temp_player,
                temp_state.ghosts,
                debug_mode=False,
                game_over=False,
                lives=3,
                dying=False,
                death_timer=0,
                death_animation_length=90
            )
        else:
            # Use existing state if available
            self.ui.render_game(
                self.state.grid,
                self.player,
                self.state.ghosts,
                self.state.debug_mode,
                self.state.game_over,
                self.state.lives,
                self.state.dying,
                self.state.death_timer,
                self.state.death_animation_length
            )
        
    def run(self) -> None:
        """Main game loop."""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.render()
            self.clock.tick(30)
        pygame.quit()

if __name__ == '__main__':
    game = PacmanGame()
    game.run()
