import pygame
from typing import List, Tuple
import math

class UI:
    """Handles all UI and rendering functionality for the game."""
    
    def __init__(self, screen: pygame.Surface, cell_size: int):
        """Initialize the UI with the pygame screen and cell size."""
        self.screen = screen
        self.cell_size = cell_size
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def render_game(self, grid: List[List[int]], player, ghosts: List, debug_mode: bool = False, 
                    game_over: bool = False, lives: int = 3, dying: bool = False, death_timer: int = 0,
                    death_animation_length: int = 90, high_score: int = 0, victory: bool = False,
                    victory_timer: int = 0, victory_animation_length: int = 180,
                    collectibles_remaining: int = 0, total_collectibles: int = 0) -> None:
        """Main rendering method that draws everything in the game."""
        self.screen.fill((0, 0, 0))  # Clear screen
        self._draw_grid(grid)
        
        # Draw ghosts
        for ghost in ghosts:
            ghost.draw(self.screen, self.cell_size)
        
        # Draw player based on game state
        if dying:
            # Death animation
            death_progress = death_timer / death_animation_length
            player.draw(self.screen, self.cell_size, dying=True, death_progress=death_progress)
        elif victory:
            # Victory animation - draw player with different visualization
            victory_progress = min(1.0, victory_timer / victory_animation_length)
            self._draw_victory_player(player, victory_progress)
        elif not game_over:
            # Normal gameplay
            player.draw(self.screen, self.cell_size)
            
        self._draw_score(player.score, high_score)
        self._draw_lives(lives)
        
        # Show collectibles count if in debug mode
        if debug_mode:
            self._draw_debug_info(ghosts)
            self._draw_collectibles_info(collectibles_remaining, total_collectibles)
        
        # Show specific overlays based on game state
        if victory:
            # Always show victory screen if in victory state, animation capped at 100%
            victory_progress = min(1.0, victory_timer / victory_animation_length)
            self._draw_victory_screen(victory_progress)
        elif game_over and not dying:
            self._draw_game_over()
            
        pygame.display.flip()
    
    def _draw_grid(self, grid: List[List[int]]) -> None:
        """Draw the game grid with walls and dots."""
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x = j * self.cell_size
                y = i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                if grid[i][j] == 1:  # Wall
                    pygame.draw.rect(self.screen, (51, 51, 51), rect)
                elif grid[i][j] == 2:  # Regular dot
                    dot_size = self.cell_size // 4
                    dot_pos = (x + self.cell_size//2, y + self.cell_size//2)
                    pygame.draw.circle(self.screen, (255, 255, 0), dot_pos, dot_size)
                elif grid[i][j] == 3:  # Power pellet/fruit
                    dot_size = self.cell_size // 3  # Bigger than regular dots
                    dot_pos = (x + self.cell_size//2, y + self.cell_size//2)
                    
                    # Draw fruit as a larger, pulsing circle
                    pulse_factor = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.1 + 0.9  # 0.9 to 1.1
                    pygame.draw.circle(self.screen, (255, 50, 50), dot_pos, int(dot_size * pulse_factor))
                    
                    # Add small white highlight to make it look more like a cherry
                    highlight_pos = (dot_pos[0] - dot_size//3, dot_pos[1] - dot_size//3)
                    pygame.draw.circle(self.screen, (255, 255, 255), highlight_pos, dot_size//4)
    
    def _draw_entities(self, player, ghosts: List) -> None:
        """Draw player and ghosts using their draw methods."""
        # Draw player 
        player.draw(self.screen, self.cell_size)
        
        # Draw ghosts
        for ghost in ghosts:
            ghost.draw(self.screen, self.cell_size)
    
    def _draw_score(self, score: int, high_score: int) -> None:
        """Display the current score and high score on screen."""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Update high score display in real time if current score is higher
        displayed_high = max(score, high_score)
        high_score_color = (255, 215, 0) if score > high_score else (255, 255, 0)  # Gold color if new high score
        
        # Display high score
        high_score_text = font.render(f"High: {displayed_high}", True, high_score_color)
        self.screen.blit(high_score_text, (10, 50))
        
        # If current score is higher than high score, show a NEW! indicator
        if score > high_score:
            new_text = font.render("NEW!", True, (255, 0, 0))
            self.screen.blit(new_text, (150, 50))
    
    def _draw_lives(self, lives: int) -> None:
        """Display the number of remaining lives."""
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (self.width - 150, 10))
    
    def _draw_debug_info(self, ghosts: List) -> None:
        """Draw debug information like ghost paths."""
        for ghost in ghosts:
            if ghost.path:
                points = [(p[1] * self.cell_size + self.cell_size//2,
                         p[0] * self.cell_size + self.cell_size//2)
                        for p in ghost.path[ghost.path_index:]]
                if len(points) > 1:
                    pygame.draw.lines(self.screen, ghost.color, False, points, 2)
        
        font = pygame.font.Font(None, 36)
        debug_text = font.render(f"Debug Mode: ON (F3)", True, (255, 255, 255))
        self.screen.blit(debug_text, (10, self.height - 30))
    
    def _draw_game_over(self) -> None:
        """Display game over message."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        
        # Instructions text
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def _draw_victory_screen(self, progress: float) -> None:
        """Display victory message with animation."""
        # Semi-transparent overlay that becomes more opaque over time
        overlay_alpha = min(200, int(progress * 255))  # Max 200 alpha (partial transparency)
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 100, overlay_alpha))  # Blue-tinted overlay
        self.screen.blit(overlay, (0, 0))
        
        # Calculate text size based on animation progress
        size_factor = 1.0 + math.sin(progress * 5) * 0.05  # Pulsing effect
        
        # Victory text
        font_size = int(72 * size_factor)
        font = pygame.font.Font(None, font_size)
        text = font.render("VICTORY!", True, (255, 255, 0))  # Yellow text
        
        # Add glow/shadow effect
        glow_surf = pygame.Surface((text.get_width() + 10, text.get_height() + 10), pygame.SRCALPHA)
        glow_color = (255, 255, 0, 100)  # Semi-transparent yellow
        pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
        glow_surf = pygame.transform.scale(glow_surf, (int(glow_surf.get_width() * 1.2), int(glow_surf.get_height() * 1.2)))
        
        # Position and draw the glow and text
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 30))
        glow_rect = glow_surf.get_rect(center=text_rect.center)
        self.screen.blit(glow_surf, glow_rect)
        self.screen.blit(text, text_rect)
        
        # Congratulations text
        font_small = pygame.font.Font(None, 36)
        congrats_text = font_small.render("Congratulations! You've collected all the dots!", True, (255, 255, 255))
        congrats_rect = congrats_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
        self.screen.blit(congrats_text, congrats_rect)
        
        # Restart text that appears later in the animation
        if progress > 0.5:
            restart_opacity = min(255, int((progress - 0.5) * 2 * 255))
            restart_text = font_small.render("Press R to play again", True, (255, 255, 255, restart_opacity))
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 90))
            self.screen.blit(restart_text, restart_rect)
    
    def _draw_victory_player(self, player, progress: float) -> None:
        """Draw the player with special victory animation."""
        # Get player position
        center_x = player.pos[1] * self.cell_size + self.cell_size // 2
        center_y = player.pos[0] * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2
        
        # Animate the player - make it pulse/rotate during victory
        pulse_factor = 1.0 + 0.2 * math.sin(progress * 12)
        rotate_angle = progress * 360 * 2  # Rotate twice over the animation period
        
        # Create a surface for the rotating pacman
        size = int(radius * 2 * 1.5)  # Make surface a bit larger than pacman
        pacman_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw pacman on the surface - always with mouth open in victory
        pygame.draw.circle(pacman_surface, (255, 255, 0), (size//2, size//2), radius * pulse_factor)
        
        # Add a mouth cutout (45 degree angle)
        start_angle = -45
        end_angle = 45
        
        # Create a pie wedge for the mouth
        mouth_points = [(size//2, size//2)]  # Center point
        num_points = 10
        for i in range(num_points + 1):
            angle_rad = math.radians(start_angle + (end_angle - start_angle) * i / num_points)
            x = size//2 + radius * math.cos(angle_rad) * pulse_factor
            y = size//2 + radius * math.sin(angle_rad) * pulse_factor
            mouth_points.append((x, y))
        mouth_points.append((size//2, size//2))  # Back to center
        
        # Draw mouth cutout in black
        pygame.draw.polygon(pacman_surface, (0, 0, 0), mouth_points)
        
        # Rotate the surface
        rotated = pygame.transform.rotate(pacman_surface, rotate_angle)
        
        # Position the rotated surface on the screen
        rect = rotated.get_rect(center=(center_x, center_y))
        self.screen.blit(rotated, rect)
    
    def _draw_collectibles_info(self, remaining: int, total: int) -> None:
        """Display information about remaining collectibles."""
        font = pygame.font.Font(None, 24)
        text = font.render(f"Dots remaining: {remaining}/{total}", True, (255, 255, 255))
        self.screen.blit(text, (10, self.height - 60))
