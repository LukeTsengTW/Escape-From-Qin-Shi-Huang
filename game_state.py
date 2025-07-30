import pygame
import constants
from maze import random_walkable_position, get_non_overlapping_positions
from difficulty import difficulty_parameter_setting
from camera import Camera

def get_game_objects():
    from game_objects import Player, Item, Key
    return Player, Item, Key

def get_assets():
    from assets import item_images, key_images
    return item_images, key_images

class GameState:
    """Game state manager class"""
    def __init__(self):
        # Initialize the camera
        self.camera = Camera(constants.WIDTH, constants.HEIGHT)
        self.reset()
    
    def reset(self):
        """Reset all game state variables"""
        Player, Item, Key = get_game_objects()
        
        # Sprite groups
        self.player = Player((constants.TILE_SIZE, constants.TILE_SIZE))

        self.player.base_speed = constants.PLAYER_SPEED
        self.player.speed = constants.PLAYER_SPEED

        self.player_group = pygame.sprite.Group(self.player)
        self.enemy_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.key_group = pygame.sprite.Group()
        
        # Game objects
        self.key_pos = (0, 0)
        self.exit_pos = (0, 0)
        self.key = None
        self.game_exit_rect = pygame.Rect(0, 0, 0, 0)
        
        # Game state variables
        self.has_key = False
        self.start_time = pygame.time.get_ticks()
        self.boost_timer = 0
        self.running = True
        self.spawn_enemy_after_delay = False
        self.spawn_enemy_delay_start = 0
        self.paused = False
        
        # Pause time tracking
        self.total_pause_time = 0
        self.pause_start_time = 0
        
        # Reset hate value
        constants.HATE_VALUE = 0
        
        # Reset camera position
        if hasattr(self, 'camera'):
            self.camera.update(self.player)
    
    def update_camera(self):
        """Update camera position"""
        self.camera.update(self.player)
    
    def pause_game(self):
        """Pause the game and start tracking pause time"""
        if not self.paused:
            self.paused = True
            self.pause_start_time = pygame.time.get_ticks()
    
    def resume_game(self):
        """Resume the game and update total pause time"""
        if self.paused:
            self.paused = False
            pause_duration = pygame.time.get_ticks() - self.pause_start_time
            self.total_pause_time += pause_duration
    
    def get_adjusted_time(self):
        """Get current time adjusted for pause time"""
        current_time = pygame.time.get_ticks()
        if self.paused:
            # If currently paused, don't count the current pause session
            return current_time - self.total_pause_time
        else:
            return current_time - self.total_pause_time
    
    def get_elapsed_time(self):
        """Get elapsed time since game start (excluding pause time)"""
        return self.get_adjusted_time() - self.start_time
    
    def initialize_level(self):
        """Initialize level-specific objects"""
        # Set difficulty and spawn items

        from config import load_config
        config = load_config()
        difficulty_parameter_setting(config["DIFFICULTY"])
        self.spawn_items()
        
        # Create key and exit
        Player, Item, Key = get_game_objects()
        item_images, key_images = get_assets()
        
        self.key_pos, self.exit_pos = get_non_overlapping_positions()
        self.key = Key(key_images, self.key_pos)
        self.key_group.add(self.key)
        self.game_exit_rect = pygame.Rect(self.exit_pos[0], self.exit_pos[1], constants.TILE_SIZE, constants.TILE_SIZE)
    
    def spawn_items(self):
        """Spawn items on the map"""
        Player, Item, Key = get_game_objects()
        item_images, key_images = get_assets()
        
        for _ in range(constants.SPAWN_ITEMS_TIMES):
            for item_type in ['red', 'yellow', 'blue']:
                pos = random_walkable_position()
                self.item_group.add(Item(item_images[item_type], pos, item_type))
    
    def kill_all_sprites(self):
        """Clear all sprite groups"""
        self.player_group.empty()
        self.enemy_group.empty()
        self.item_group.empty()
        self.key_group.empty()

game_state = GameState()

def initialize_game_state():
    """Initialize all game state variables - updated version"""
    game_state.reset()
    game_state.initialize_level()

def kill_all_sprite():
    """Legacy function for compatibility"""
    game_state.kill_all_sprites()