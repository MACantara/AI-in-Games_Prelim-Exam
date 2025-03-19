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
            'dying': os.path.join(os.path.dirname(__file__), "static/audio/pac-man-dying.mp3")
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
            if os.path.exists(self.audio_paths['dying']):
                self.sound_effects['dying'] = pygame.mixer.Sound(self.audio_paths['dying'])
                # Get the length of the death sound to sync with animation
                self.dying_sound_length = int(self.sound_effects['dying'].get_length() * 30)  # Convert seconds to frames at 30fps
            else:
                print(f"Warning: Could not find dying sound at {self.audio_paths['dying']}")
                self.dying_sound_length = 90  # Default length in frames
        except pygame.error as e:
            print(f"Error loading sound: {e}")
            self.dying_sound_length = 90  # Default length in frames
    
    def _init_game(self):
        """Initialize the game state and player."""
        self.state = GameState.create_new_game()
        # Set the death animation length based on the sound effect length
        self.state.death_animation_length = self.dying_sound_length
        self.state.set_death_callback(self._on_player_death)
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
                # Regular game input handling
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        self.state.debug_mode = not self.state.debug_mode
                    elif event.key == pygame.K_r and self.state.game_over:
                        self._restart_game()
                    elif not self.state.game_over:
                        self.player.handle_key_input(event.key)
        return True
    
    def _on_player_death(self):
        """Callback for when player dies - play death sound."""
        # Stop the eating sound
        pygame.mixer.music.stop()
        
        # Play death sound if available
        if 'dying' in self.sound_effects:
            self.sound_effects['dying'].play()
            
    def _restart_game(self) -> None:
        """Restart the game after game over."""
        self.state = GameState.create_new_game()
        # Set the death animation length based on the sound effect length
        self.state.death_animation_length = self.dying_sound_length 
        self.state.set_death_callback(self._on_player_death)
        self.player = Player(self.state.player_pos)
        self.ghost_move_delay = 0
        # Make sure eating sound is playing on restart
        if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
            self._play_eating_sound_loop()
        
    def update(self) -> None:
        """Update game state."""
        if self.in_startup:
            # Check if startup music has finished
            if not pygame.mixer.music.get_busy():
                self.in_startup = False
                self._init_game()
            return
        
        # Update player position and collect dots
        self.player.update_position(self.state.grid, self.state.dying)
        
        # Update game state with current player position and direction
        self.state.player_pos = self.player.pos
        self.state.player_direction = self.player.direction
        
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
