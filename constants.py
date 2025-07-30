from config import load_config

config = load_config()

# Game window settings
WIDTH, HEIGHT = config["resolution_width"], config["resolution_height"]
TILE_SIZE = 40
MAZE_COLS, MAZE_ROWS = 31, 31

# Game mechanics
PLAYER_SPEED = 2
BOOST_SPEED = 4
ENEMY_SPEED = 3
HATE_VALUE = 0

# Durations (in milliseconds)
BOOST_DURATION = 5000
FREEZE_DURATION = 3000
RED_DURATION = 10000
BLUE_DURATION = 10000
INVISIBLE_DURATION = 10000

# Stamina System
SPRINT_SPEED_BONUS = 2
STAMINA_MAX = 2000
STAMINA_RECOVERY_RATE = 0.8
STAMINA_BAR_WIDTH = 60
STAMINA_BAR_HEIGHT = 8

# Game settings
SPAWN_ITEMS_TIMES = 3
DIFFICULTY = config["DIFFICULTY"]
FIRST_OPEN_GAME = config["first_open_game"]

master_volume, music_volume, sfx_volume = config["master_volume"], config["music_volume"], config["sfx_volume"]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Resolution options
RESOLUTION_OPTIONS = [
    (800, 600),   # 4:3
    (1024, 768),  # 4:3
    (1280, 720),  # 16:9 HD
    (1366, 768),  # 16:9
    (1600, 900),  # 16:9
    (1920, 1080), # 16:9 FHD
    (2560, 1440), # 16:9 QHD
]

# Version
current_version = "Beta v1.2"