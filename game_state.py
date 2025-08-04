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
        
        # Store current game mode and level before reset (if they exist)
        current_game_mode = getattr(self, 'game_mode', "random")
        current_level = getattr(self, 'current_level', 1)
        
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
        
        # Game mode and level info (preserve existing values)
        self.game_mode = current_game_mode
        self.current_level = current_level
        
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
        
        # Use fixed positions for level mode, random for random mode
        if self.game_mode == "level":
            from maze import get_level_positions
            self.key_pos, self.exit_pos = get_level_positions(self.current_level)
        else:
            self.key_pos, self.exit_pos = get_non_overlapping_positions()
            
        self.key = Key(key_images, self.key_pos)
        self.key_group.add(self.key)
        self.game_exit_rect = pygame.Rect(self.exit_pos[0], self.exit_pos[1], constants.TILE_SIZE, constants.TILE_SIZE)
        
        # No immediate enemy spawning for any level - let game_logic.py handle it after INVISIBLE_DURATION
    
    def spawn_boss_enemies(self):
        """Spawn 2 enemies for boss level (Level 5)"""
        from game_objects import Enemy
        
        # Spawn first enemy at a safe distance from player (not at starting position)
        enemy1 = Enemy((5 * constants.TILE_SIZE, 5 * constants.TILE_SIZE))  # Away from player spawn
        enemy1.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy1)
        
        # Spawn second enemy at opposite corner
        enemy2 = Enemy((39 * constants.TILE_SIZE, 39 * constants.TILE_SIZE))  # Boss level is 41x41
        enemy2.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy2)
        
        print("Boss level: 2 enemies spawned!")
    
    def spawn_final_boss_enemies(self):
        """Spawn 3 enemies for final boss level (Level 10)"""
        from game_objects import Enemy
        
        # Spawn first enemy at a safe distance from player (not at starting position)
        enemy1 = Enemy((7 * constants.TILE_SIZE, 7 * constants.TILE_SIZE))  # Away from player spawn
        enemy1.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy1)
        
        # Spawn second enemy at opposite corner
        enemy2 = Enemy((43 * constants.TILE_SIZE, 43 * constants.TILE_SIZE))  # Final boss level is 51x51
        enemy2.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy2)
        
        # Spawn third enemy at another corner
        enemy3 = Enemy((7 * constants.TILE_SIZE, 43 * constants.TILE_SIZE))  # Third enemy position
        enemy3.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy3)
        
        print("Final Boss level: 3 enemies spawned!")
    
    def spawn_ultimate_boss_enemies(self):
        """Spawn 4 enemies for ultimate boss level (Level 15)"""
        from game_objects import Enemy
        
        # Spawn first enemy at a safe distance from player (not at starting position)
        enemy1 = Enemy((9 * constants.TILE_SIZE, 9 * constants.TILE_SIZE))  # Away from player spawn
        enemy1.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy1)
        
        # Spawn second enemy at opposite corner
        enemy2 = Enemy((51 * constants.TILE_SIZE, 51 * constants.TILE_SIZE))  # Ultimate boss level is 61x61
        enemy2.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy2)
        
        # Spawn third enemy at another corner
        enemy3 = Enemy((9 * constants.TILE_SIZE, 51 * constants.TILE_SIZE))  # Third enemy position
        enemy3.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy3)
        
        # Spawn fourth enemy at the remaining corner
        enemy4 = Enemy((51 * constants.TILE_SIZE, 9 * constants.TILE_SIZE))  # Fourth enemy position
        enemy4.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy4)
        
        print("Ultimate Boss level: 4 enemies spawned!")
    
    def spawn_single_enemy(self):
        """Spawn single enemy for levels 6-9"""
        from game_objects import Enemy
        
        # Spawn enemy at a safe distance from player starting position (1,1)
        # Choose a position far from the starting point
        enemy_pos = (35 * constants.TILE_SIZE, 35 * constants.TILE_SIZE)  # Far corner for 41x41 maps
        enemy = Enemy(enemy_pos)
        enemy.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy)
        
        print(f"Level {self.current_level}: 1 enemy spawned!")
    
    def spawn_level_11_14_enemies(self):
        """Spawn 2 enemies for levels 11-14 (51x51 maps)"""
        from game_objects import Enemy
        
        # Spawn first enemy at a safe distance from player (not at starting position)
        enemy1 = Enemy((7 * constants.TILE_SIZE, 7 * constants.TILE_SIZE))  # Away from player spawn
        enemy1.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy1)
        
        # Spawn second enemy at opposite corner
        enemy2 = Enemy((43 * constants.TILE_SIZE, 43 * constants.TILE_SIZE))  # For 51x51 maps
        enemy2.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        self.enemy_group.add(enemy2)
        
        print(f"Level {self.current_level}: 2 enemies spawned!")
    
    def spawn_items(self):
        """Spawn items on the map"""
        Player, Item, Key = get_game_objects()
        item_images, key_images = get_assets()
        
        for _ in range(constants.SPAWN_ITEMS_TIMES):
            for item_type in ['red', 'yellow', 'blue']:
                pos = random_walkable_position(self.current_level)
                self.item_group.add(Item(item_images[item_type], pos, item_type))
    
    def kill_all_sprites(self):
        """Clear all sprite groups"""
        self.player_group.empty()
        self.enemy_group.empty()
        self.item_group.empty()
        self.key_group.empty()

game_state = GameState()

def initialize_game_state(regenerate_maze_flag=True, game_mode="random", level_number=1):
    """Initialize all game state variables - updated version"""
    if game_mode == "level":
        # Level mode - load specific level maze
        from maze import load_level_maze, update_walls
        load_level_maze(level_number)
        update_walls()
    elif regenerate_maze_flag:
        # Random mode - generate new maze
        from maze import regenerate_maze, update_walls
        regenerate_maze()
        update_walls()
    else:
        # If maze is already loaded, just update walls
        from maze import update_walls
        update_walls()
    
    # Set game mode and level info
    game_state.game_mode = game_mode
    game_state.current_level = level_number
    
    game_state.reset()
    game_state.initialize_level()

def kill_all_sprite():
    """Legacy function for compatibility"""
    game_state.kill_all_sprites()