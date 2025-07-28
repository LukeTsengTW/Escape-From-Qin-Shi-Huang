"""
Game Name : Escape from Qin Shi Huang
Author : LukeTseng
Programming Language : Python
"""

from PIL import Image
import pygame
import sys
import random
import time
import heapq

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 40
MAZE_COLS, MAZE_ROWS = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
PLAYER_SPEED = 2
BOOST_SPEED = 4
ENEMY_SPEED = 3
HATE_VALUE = 0
BOOST_DURATION = 5000
FREEZE_DURATION = 3000
ENEMY_MOVE_INTERVAL = 200
INVISIBLE_DURATION = 5
RED_DURATION = 5000
BLUE_DURATION = 5000
SPAWN_ITEMS_TIMES = 2
DIFFICULTY = "normal"

master_volume, music_volume, sfx_volume = 1.0, 1.0, 1.0

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (200, 0, 200)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)

# === initial Pygame ===
pygame.init()
icon = pygame.image.load("icon.ico")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("逃離秦始皇 ( Escape from Qin Shi Huang )")
clock = pygame.time.Clock()

# initial mixer
pygame.mixer.init()

# loading bgm
menu_music_path = "sound/bgm/menu/menu_bgm.ogg"
playing_music_path = "sound/bgm/playing/c1.ogg"
victory_music_path = "sound/bgm/victory/victory.ogg"
gameover_music_path = "sound/bgm/gameover/gameover.ogg"

# loading sound effect
menu_click_sound = pygame.mixer.Sound("sound/sound_effect/menu/menu_selection_click.ogg")
door_open_sound = pygame.mixer.Sound("sound/sound_effect/door_open/door_open.ogg")
hit_sound = pygame.mixer.Sound("sound/sound_effect/hit/hit.ogg")

exit_image = pygame.image.load("img/exit/exit.png").convert_alpha()

item_images = {
    'red': pygame.image.load("img/items/sword/sword.png").convert_alpha(),
    'yellow': pygame.image.load("img/items/bolt/bolt.png").convert_alpha(),
    'blue': pygame.image.load("img/items/snowflake/snowflake.png").convert_alpha()
}

key_images = [
    pygame.image.load("img/items/keys/key_1.png").convert_alpha(),
    pygame.image.load("img/items/keys/key_2.png").convert_alpha(),
    pygame.image.load("img/items/keys/key_3.png").convert_alpha(),
    pygame.image.load("img/items/keys/key_4.png").convert_alpha()
]

# === Language Setting ===

current_language = "zh_tw"  # Default as traditional Chinese

font = pygame.font.Font("Cubic_11.ttf", 18)

translations = {
    "zh_tw": {
        "title": "逃離秦始皇",
        "play": "開始遊戲",
        "setting": "設定",
        "how_to_play" : "如何遊玩",
        "htp_line1" : "1. 你將扮演北極熊，在迷宮中逃離秦始皇的魔掌",
        "htp_line2" : "2. 透過 ↑ ↓ ← → 四個方向鍵移動",
        "htp_line3" : "3. 路途上有道具，用於干擾秦始皇",
        "exit" : "離開遊戲",
        "language": "語言",
        "sound": "音效",
        "back": "返回",
        "select_language": "選擇語言",
        "traditional_chinese": "繁體中文",
        "simplified_chinese": "简体中文",
        "english": "English",
        "invisible_time" : "秦始皇出現時間:",
        "is_key_obtained" : "已獲得鑰匙",
        "game_paused" : "遊戲暫停",
        "resume" : "繼續遊戲",
        "back_menu" : "回到主選單",
        "invincible_time" : "無敵時間：",
        "red_time" : "反傷持續：",
        "blue_time" : "冰凍持續：",
        "difficulty" : "難度",
        "difficulty_setting" : "難度設定",
        "now_difficulty" : "現在難度:",
        "easy" : "簡單",
        "normal" : "普通",
        "difficult" : "困難",
        "gameover" : "遊戲結束，你被秦始皇抓到了",
        "pass" : "恭喜通關！逃離秦始皇的魔掌！",
        "master_volume" : "主音量",
        "bgm" : "背景音量",
        "se" : "音效音量",
    },
    "zh_cn": {
        "title": "逃离秦始皇",
        "play": "开始游戏",
        "setting": "设置",
        "how_to_play" : "如何游玩",
        "htp_line1" : "1. 你将扮演北极熊，在迷宫中逃离秦始皇的魔掌",
        "htp_line2" : "2. 透过 ↑ ↓ ← → 四个方向键移动",
        "htp_line3" : "3. 路途上有道具，用于干扰秦始皇",
        "exit" : "离开游戏",
        "language": "语言",
        "sound": "音效",
        "back": "返回",
        "select_language": "选择语言",
        "traditional_chinese": "繁体中文",
        "simplified_chinese": "简体中文",
        "english": "English",
        "invisible_time" : "秦始皇出现时间:",
        "is_key_obtained" : "已获得钥匙",
        "game_paused" : "游戏暂停",
        "resume" : "继续游戏",
        "back_menu" : "回到主菜单",
        "invincible_time" : "无敌时间：",
        "red_time" : "反伤持续：",
        "blue_time" : "冰凍持续：",
        "difficulty" : "难度",
        "difficulty_setting" : "难度设置",
        "now_difficulty" : "现在难度:",
        "easy" : "简单",
        "normal" : "普通",
        "difficult" : "困难",
        "gameover" : "游戏结束，你被秦始皇抓到了",
        "pass" : "恭喜通关！逃离秦始皇的魔掌！",
        "master_volume" : "主音量",
        "bgm" : "背景音量",
        "se" : "音效音量",
    },
    "en": {
        "title": "Escape from Qin Shi Huang",
        "play": "Play",
        "setting": "Setting",
        "how_to_play" : "How To Play",
        "htp_line1" : "1. You play as a polar bear and escape from the clutches of Qin Shi Huang in the maze",
        "htp_line2" : "2. Use the ↑ ↓ ← → arrow keys to move",
        "htp_line3" : "3. There are items on the road to interfere with Qin Shi Huang",
        "exit" : "Exit",
        "language": "Language",
        "sound": "Sound",
        "back": "Back",
        "select_language": "Select Language",
        "traditional_chinese": "Traditional Chinese",
        "simplified_chinese": "Simplified Chinese",
        "english": "English",
        "invisible_time" : "Time of Qin Shi Huang's appearance:",
        "is_key_obtained" : "Key Obtained",
        "game_paused" : "Pause",
        "resume" : "Resume",
        "back_menu" : "Back to menu",
        "invincible_time" : "Invincible time:",
        "red_time" : "Thorn Sword Time:",
        "blue_time" : "Frozen Time:",
        "difficulty" : "Difficulty",
        "difficulty_setting" : "Difficulty Setting",
        "now_difficulty" : "Current Difficulty:",
        "easy" : "Easy",
        "normal" : "Normal",
        "difficult" : "Difficult",
        "gameover" : "Game Over, You Failed",
        "pass" : "Complete the game!",
        "master_volume" : "Main Volume",
        "bgm" : "BGM Volume",
        "se" : "Sound Effect Volume",
    }
}

# === Maze Map ===

def generate_maze(width, height, loop_chance=0.1):
    """
    width: Odd Width
    height: Odd Height
    loop_chance: The probability of deliberately breaking through a wall near an open path (0~1). 
                 The larger the value, the more loops there are. 0 means no loops.
    """
    
    assert width % 2 == 1 and height % 2 == 1

    maze = [[1 for _ in range(width)] for _ in range(height)]

    # Start Point
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0

    # Storage backtracking path
    stack = [(start_x, start_y)]

    directions = [(2,0), (-2,0), (0,2), (0,-2)]

    while stack:
        x, y = stack[-1]

        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width-1 and 1 <= ny < height-1:
                if maze[ny][nx] == 1:
                    neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)

            maze[(y + ny)//2][(x + nx)//2] = 0
            maze[ny][nx] = 0

            stack.append((nx, ny))

            # Form a loop (optional) and try to break through non-traversed neighbor walls near the current point
            if random.random() < loop_chance:
                loop_dirs = [(2,0), (-2,0), (0,2), (0,-2)]
                random.shuffle(loop_dirs)
                for ldx, ldy in loop_dirs:
                    lx, ly = x + ldx, y + ldy
                    wall_x, wall_y = x + ldx//2, y + ldy//2
                    if 1 <= lx < width-1 and 1 <= ly < height-1:
                        if maze[ly][lx] == 0 and maze[wall_y][wall_x] == 1:
                            maze[wall_y][wall_x] = 0  # Break the wall to connect two paths
                            break  # Only one loop wall can be opened per round
        else:
            # No neighbors, backtracing
            stack.pop()

    return maze

""" 
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,1,1,1,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
"""

# random generate the maze map
MAZE = generate_maze(MAZE_COLS+1, MAZE_ROWS-1)

walls = [pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
          for row, line in enumerate(MAZE)
          for col, tile in enumerate(line) if tile == 1]

def load_gif_frames(filename):
    pil_img = Image.open(filename)
    frames = []
    try:
        while True:
            frame = pil_img.convert("RGBA")
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            py_image = pygame.image.fromstring(data, size, mode)
            frames.append(py_image)
            pil_img.seek(pil_img.tell() + 1)
    except EOFError:
        pass
    return frames

# detect if can walk
def is_path(x, y):
    col, row = x // TILE_SIZE, y // TILE_SIZE
    return 0 <= row < len(MAZE) and 0 <= col < len(MAZE[0]) and MAZE[row][col] == 0

# heuristic algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Algorithm, for enemy
def a_star(start, goal, return_full=False):
    start_tile = (start[0] // TILE_SIZE, start[1] // TILE_SIZE)
    goal_tile = (goal[0] // TILE_SIZE, goal[1] // TILE_SIZE)
    frontier = [(0, start_tile)]
    came_from = {start_tile: None}
    cost_so_far = {start_tile: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal_tile:
            break

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[1] < len(MAZE) and 0 <= neighbor[0] < len(MAZE[0]) and MAZE[neighbor[1]][neighbor[0]] == 0:
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal_tile, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

    path = []
    if goal_tile in came_from:
        current = goal_tile
        while current != start_tile:
            path.append((current[0] * TILE_SIZE, current[1] * TILE_SIZE))
            current = came_from[current]
        path.reverse()
    return path if return_full else (path[0] if path else start)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load a multi-frame animation. Assumes you have split it into multiple images or decomposed the GIF.
        self.frames = [pygame.image.load(f"img/player/frame-{i}.png").convert_alpha() for i in range(1, 14)]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = self.rect.inflate(-10, -10) # setting collision_rect to comfort to move
        self.speed = PLAYER_SPEED
        self.facing_right = True

        self.animation_timer = 0
        self.animation_speed = 3  # millisecond, player animation speed every fps
        # ---------------------------------------------------
        self.conditional_effect_active_red = False
        self.conditional_effect_start_time_red = 0
        self.conditional_effect_active_blue = False
        self.conditional_effect_start_time_blue = 0
        self.invincible = False
        self.invincible_start_time = 0

    def update(self, keys):
        # movement logics
        
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.facing_right = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.facing_right = False
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Predicted horizontal new position
        new_rect = self.collision_rect.move(dx, 0)
        for wall in walls:
            if new_rect.colliderect(wall):
                if dx > 0:  # Hit the wall to the right
                    new_rect.right = wall.left
                elif dx < 0:  # Hit the wall to the left
                    new_rect.left = wall.right
                dx = 0  # resist the wall

        self.collision_rect.x = new_rect.x  # Finalize the x coordinate

        # Predict new vertical position
        new_rect = self.collision_rect.move(0, dy)
        for wall in walls:
            if new_rect.colliderect(wall):
                if dy > 0:  # Hit the wall to the down
                    new_rect.bottom = wall.top
                elif dy < 0:  # Hit the wall to the up
                    new_rect.top = wall.bottom
                dy = 0  # resist the wall

        self.collision_rect.y = new_rect.y  # Finalize the y coordinate

        self.rect.center = self.collision_rect.center

        # Control animation frame switching
        now = pygame.time.get_ticks()
        if dx != 0 or dy != 0:  # Play animation only when moving
            if now - self.animation_timer > self.animation_speed:
                self.animation_timer = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        else:
            # Set back to first frame when stationary (standing)
            self.current_frame = 0
            self.image = self.frames[self.current_frame]

        # Flip the image based on its orientation
        if self.facing_right:
            self.image = self.frames[self.current_frame]
        else:
            self.image = pygame.transform.flip(self.frames[self.current_frame], True, False)

        # Handle the end of invincibility
        if self.invincible and now - self.invincible_start_time > 3000:
            self.invincible = False

        # The 7-second condition window automatically expires
        if self.conditional_effect_active_red and now - self.conditional_effect_start_time_red > RED_DURATION:
            self.conditional_effect_active_red = False
        if self.conditional_effect_active_blue and now - self.conditional_effect_start_time_blue > BLUE_DURATION:
            self.conditional_effect_active_blue = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load a multi-frame animation. Assumes you have split it into multiple images or decomposed the GIF.
        self.frames = [pygame.image.load(f"img/enemy/frame-{i}.png").convert_alpha() for i in range(1, 27)]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.spawn_time = time.time()
        self.frozen = False
        self.path = []
        self.path_index = 0
        self.move_timer = 0
        self.animation_timer = 0
        self.animation_speed = 10  # millisecond, enemy animation speed every fps

        self.facing_right = True

    def update(self, player):
        if self.frozen or time.time() - self.spawn_time < 1:
            return
        
        now = pygame.time.get_ticks()

        if now - self.move_timer > ENEMY_MOVE_INTERVAL:
            self.move_timer = now
            # Calculate the full path
            self.path = a_star((self.rect.x, self.rect.y), player.rect.center, return_full=True)
            self.path_index = 0

        if self.path and self.path_index < len(self.path):
            target = self.path[self.path_index]
            step_x = 0
            step_y = 0
            if target[0] > self.rect.x:
                step_x = ENEMY_SPEED
                self.facing_right = False
            elif target[0] < self.rect.x:
                step_x = -ENEMY_SPEED
                self.facing_right = True
            if target[1] > self.rect.y:
                step_y = ENEMY_SPEED
            elif target[1] < self.rect.y:
                step_y = -ENEMY_SPEED

            self.rect.x += step_x
            self.rect.y += step_y

            # When the enemy approaches the target coordinates, go to the next path node
            if abs(self.rect.x - target[0]) < ENEMY_SPEED and abs(self.rect.y - target[1]) < ENEMY_SPEED:
                self.rect.topleft = target
                self.path_index += 1

        # Animation logics
        if now - self.animation_timer > self.animation_speed:
            self.animation_timer = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        if self.facing_right:
            self.image = self.frames[self.current_frame]
        else:
            self.image = pygame.transform.flip(self.frames[self.current_frame], True, False)

class Item(pygame.sprite.Sprite):
    def __init__(self, image, pos, type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.type = type

class Key(pygame.sprite.Sprite):
    def __init__(self, images, pos):
        super().__init__()
        self.images = images
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect(topleft=pos)

def random_walkable_position():
    while True:
        x = random.randint(0, MAZE_COLS - 1) * TILE_SIZE
        y = random.randint(0, MAZE_ROWS - 1) * TILE_SIZE
        if is_path(x + TILE_SIZE // 2, y + TILE_SIZE // 2):
            return x, y

def spawn_items():
    global SPAWN_ITEMS_TIMES
    for _ in range(SPAWN_ITEMS_TIMES):
        for type in ['red', 'yellow', 'blue']:
            pos = random_walkable_position()
            item_group.add(Item(item_images[type], pos, type))

def draw_text_center(text, font, color, surface, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    surface.blit(text_surface, text_rect)
    return text_rect  # Returns position to detect mouse collision

def show_menu():
    global start_time, has_key, boost_timer, spawn_enemy_after_delay, spawn_enemy_delay_start, paused, player_group, enemy_group, item_group, key_group, player, key, game_exit_rect, key_pos, exit_pos, HATE_VALUE
    kill_all_sprite()

    title_font = pygame.font.Font("Cubic_11.ttf", 48)
    running_menu = True

    pygame.mixer.music.stop()
    pygame.mixer.music.load(menu_music_path)
    pygame.mixer.music.play(-1)

    while running_menu:
        screen.fill(WHITE)
        screen_title = translations[current_language]["title"]
        draw_text_center(screen_title, title_font, BLACK, screen, HEIGHT // 4)

        mouse_pos = pygame.mouse.get_pos()

        play_text = translations[current_language]["play"]
        play_y = HEIGHT // 2
        play_hover = pygame.Rect(WIDTH // 2 - 100, play_y - 20, 200, 40).collidepoint(mouse_pos)
        play_color = RED if play_hover else GRAY
        play_rect = draw_text_center(play_text, font, play_color, screen, play_y)

        setting_text = translations[current_language]["setting"]
        setting_y = HEIGHT // 2 + 60
        setting_hover = pygame.Rect(WIDTH // 2 - 100, setting_y - 20, 200, 40).collidepoint(mouse_pos)
        setting_color = RED if setting_hover else GRAY
        setting_rect = draw_text_center(setting_text, font, setting_color, screen, setting_y)

        htp_text = translations[current_language]["how_to_play"]
        htp_y = HEIGHT // 2 + 120
        htp_hover = pygame.Rect(WIDTH // 2 - 100, htp_y - 20, 200, 40).collidepoint(mouse_pos)
        htp_color = RED if htp_hover else GRAY
        htp_rect = draw_text_center(htp_text, font, htp_color, screen, htp_y)

        exit_text = translations[current_language]["exit"]
        exit_y = HEIGHT // 2 + 180
        exit_hover = pygame.Rect(WIDTH // 2 - 100, exit_y - 20, 200, 40).collidepoint(mouse_pos)
        exit_color = RED if exit_hover else GRAY
        exit_rect = draw_text_center(exit_text, font, exit_color, screen, exit_y)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    
                    menu_click_sound.play()

                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(playing_music_path)
                    pygame.mixer.music.play(-1)

                    player = Player((TILE_SIZE, TILE_SIZE))
                    player_group = pygame.sprite.Group(player)
                    enemy_group = pygame.sprite.Group()
                    item_group = pygame.sprite.Group()
                    key_group = pygame.sprite.Group()

                    difficulty_parameter_setting(DIFFICULTY)

                    spawn_items()

                    key_pos, exit_pos = get_non_overlapping_positions()

                    key_group = pygame.sprite.Group()
                    key = Key(key_images, key_pos)
                    key_group.add(key)

                    game_exit_rect = pygame.Rect(exit_pos[0], exit_pos[1], TILE_SIZE, TILE_SIZE)

                    has_key = False
                    start_time = time.time()
                    boost_timer = 0
                    spawn_enemy_after_delay = False
                    spawn_enemy_delay_start = 0

                    HATE_VALUE = 0

                    paused = False
                    running_menu = False
                elif setting_rect.collidepoint(event.pos):
                    menu_click_sound.play()
                    show_settings()
                elif htp_rect.collidepoint(event.pos):
                    menu_click_sound.play()
                    show_HowToPlay()
                elif exit_rect.collidepoint(event.pos):
                    menu_click_sound.play()
                    pygame.quit()
                    sys.exit()
                    

def show_settings():
    running_settings = True

    while running_settings:
        options = [
            translations[current_language]["language"], 
            translations[current_language]["sound"],
            translations[current_language]["difficulty"],
            translations[current_language]["back"],
        ]

        screen.fill(WHITE)

        draw_text_center(translations[current_language]["setting"], font, BLACK, screen, HEIGHT // 4)

        mouse_pos = pygame.mouse.get_pos()
        option_rects = []

        for i, option in enumerate(options):
            y_pos = HEIGHT // 2 + i * 50
            color = RED if pygame.Rect(WIDTH // 2 - 100, y_pos - 20, 200, 40).collidepoint(mouse_pos) else GRAY
            rect = draw_text_center(option, font, color, screen, y_pos)
            option_rects.append((option, rect))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running_settings = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option, rect in option_rects:
                    if rect.collidepoint(event.pos):
                        if option == translations[current_language]["back"]:
                            menu_click_sound.play()
                            running_settings = False
                        elif option == translations[current_language]["language"]:
                            menu_click_sound.play()
                            show_language_selection()
                        elif option == translations[current_language]["difficulty"]:
                            menu_click_sound.play()
                            show_difficulty()
                        elif option == translations[current_language]["sound"]:
                            menu_click_sound.play()
                            show_sound_setting()

def show_language_selection():
    global current_language

    languages = [
        ("zh_tw", translations["zh_tw"]["traditional_chinese"]),
        ("zh_cn", translations["zh_cn"]["simplified_chinese"]),
        ("en", translations["en"]["english"]),
        ("back", translations[current_language]["back"])
    ]
    running_language = True

    while running_language:
        screen.fill(WHITE)
        draw_text_center(translations[current_language]["select_language"], font, BLACK, screen, HEIGHT // 4)

        mouse_pos = pygame.mouse.get_pos()
        option_rects = []

        for i, lang in enumerate(languages):
            y_pos = HEIGHT // 2 + i * 50
            color = RED if pygame.Rect(WIDTH // 2 - 100, y_pos - 20, 200, 40).collidepoint(mouse_pos) else GRAY
            rect = draw_text_center(lang[1], font, color, screen, y_pos)
            option_rects.append((lang[0], rect))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running_language = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for lang_code, rect in option_rects:
                    if rect.collidepoint(event.pos):
                        if lang_code == "back":
                            menu_click_sound.play()
                            running_language = False
                        else:
                            menu_click_sound.play()
                            current_language = lang_code
                            print(f"選擇語言: {translations[lang_code]['traditional_chinese' if lang_code == 'zh_tw' else 'simplified_chinese' if lang_code == 'zh_cn' else 'english']}")

def show_difficulty():
    global DIFFICULTY

    difficulties = [
        translations[current_language]["easy"], 
        translations[current_language]["normal"], 
        translations[current_language]["difficult"], 
        translations[current_language]["back"]
    ]
    running_difficulty = True

    while running_difficulty:
        screen.fill(WHITE)
        draw_text_center(translations[current_language]["difficulty_setting"], font, BLACK, screen, HEIGHT // 4)

        draw_text_center(f"{translations[current_language]["now_difficulty"]} {translations[current_language][DIFFICULTY]}", font, BLACK, screen, HEIGHT // 4 + 50)

        mouse_pos = pygame.mouse.get_pos()
        option_rects = []

        for i, difficulty in enumerate(difficulties):
            y_pos = HEIGHT // 2 + i * 50
            color = RED if pygame.Rect(WIDTH // 2 - 100, y_pos - 20, 200, 40).collidepoint(mouse_pos) else GRAY
            rect = draw_text_center(difficulty, font, color, screen, y_pos)
            option_rects.append((difficulty, rect))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running_difficulty = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for difficulty, rect in option_rects:
                    if rect.collidepoint(event.pos):
                        if difficulty == translations[current_language]["back"]:
                            menu_click_sound.play()
                            running_difficulty = False
                        elif difficulty == translations[current_language]["easy"]:
                            menu_click_sound.play()
                            DIFFICULTY = "easy"
                            print(f"選擇難度: {difficulty}")
                        elif difficulty == translations[current_language]["normal"]:
                            menu_click_sound.play()
                            DIFFICULTY = "normal"
                            print(f"選擇難度: {difficulty}")
                        elif difficulty == translations[current_language]["difficult"]:
                            menu_click_sound.play()
                            DIFFICULTY = "difficult"
                            print(f"選擇難度: {difficulty}")

def show_pause_menu():
    pause_running = True
    pause_font = pygame.font.Font("Cubic_11.ttf", 36)

    while pause_running:
        screen.fill(WHITE)
        draw_text_center(translations[current_language]["game_paused"], pause_font, BLACK, screen, HEIGHT // 4)

        mouse_pos = pygame.mouse.get_pos()

        options = [translations[current_language]["resume"], translations[current_language]["setting"], translations[current_language]["back_menu"]]
        option_rects = []

        for i, option in enumerate(options):
            y_pos = HEIGHT // 2 + i * 60
            color = RED if pygame.Rect(WIDTH // 2 - 100, y_pos - 25, 200, 50).collidepoint(mouse_pos) else GRAY
            rect = draw_text_center(option, pause_font, color, screen, y_pos)
            option_rects.append((option, rect))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # press ESC to resume the game
                    pause_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option, rect in option_rects:
                    if rect.collidepoint(event.pos):
                        if option == translations[current_language]["resume"]:
                            menu_click_sound.play()
                            pause_running = False
                        elif option == translations[current_language]["setting"]:
                            menu_click_sound.play()
                            show_settings()
                        elif option == translations[current_language]["back_menu"]:
                            menu_click_sound.play()
                            return "main_menu"
    return "resume"

def show_game_over_screen():
    running_game_over = True

    pygame.mixer.music.stop()
    pygame.mixer.music.load(gameover_music_path)
    pygame.mixer.music.play()

    game_over_font = pygame.font.Font("Cubic_11.ttf", 48)
    button_font = pygame.font.Font("Cubic_11.ttf", 36)
    
    while running_game_over:
        screen.fill(BLACK)
        
        # Show the text of Game Over
        draw_text_center(translations[current_language]["gameover"], game_over_font, RED, screen, HEIGHT // 3)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Button Text and position
        button_text = translations[current_language]["back_menu"]
        button_rect = draw_text_center(button_text, button_font, RED if pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 30, 300, 60).collidepoint(mouse_pos) else GRAY, screen, HEIGHT // 2)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    menu_click_sound.play()
                    running_game_over = False

def show_victory_screen():
    running_victory = True

    pygame.mixer.music.stop()
    pygame.mixer.music.load(victory_music_path)
    pygame.mixer.music.play()

    victory_font = pygame.font.Font("Cubic_11.ttf", 48)
    button_font = pygame.font.Font("Cubic_11.ttf", 36)
    
    while running_victory:
        screen.fill(WHITE)
        
        # Show the title of Pass
        draw_text_center(translations[current_language]["pass"], victory_font, GREEN, screen, HEIGHT // 3)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Button Settings
        button_text = translations[current_language]["back_menu"]
        button_rect = draw_text_center(button_text, button_font, RED if pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 30, 300, 60).collidepoint(mouse_pos) else GRAY,  screen, HEIGHT // 2)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                menu_click_sound.play()
                running_victory = False

def show_sound_setting():
    global master_volume, music_volume, sfx_volume
    
    slider_width = 300
    slider_height = 20
    slider_x = WIDTH // 2 - slider_width // 2
    start_y = HEIGHT // 3
    gap_y = 70

    dragging_slider = None  # None or "master" / "music" / "sfx"
    
    running_sound_setting = True
    while running_sound_setting:
        screen.fill(WHITE)
        draw_text_center(translations[current_language]["sound"], font, BLACK, screen, HEIGHT // 6)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Item titles and slider coordinates
        items = [
            (translations[current_language]["master_volume"], master_volume),
            (translations[current_language]["bgm"], music_volume),
            (translations[current_language]["se"], sfx_volume),
        ]

        font_size = font.get_height()
        slider_rects = []
        label_rects = []

        for i, (label, vol) in enumerate(items):
            y = start_y + i * gap_y
            # Show the labels
            label_rect = draw_text_center(label, font, BLACK, screen, y - 15)
            label_rects.append(label_rect)

            # Calculate the slider position (bar + slider)
            bar_rect = pygame.Rect(slider_x, y, slider_width, slider_height)
            # Slider x position: according to volume percentage
            knob_x = slider_x + int(vol * slider_width)
            knob_rect = pygame.Rect(knob_x - 10, y - 5, 20, slider_height + 10)

            # Draw a long background
            pygame.draw.rect(screen, GRAY, bar_rect)
            # Draw the filled proportion
            pygame.draw.rect(screen, RED, (slider_x, y, knob_x - slider_x, slider_height))
            # Draw the slider
            pygame.draw.rect(screen, RED if knob_rect.collidepoint(mouse_pos) or dragging_slider == label else BLACK, knob_rect)

            slider_rects.append((label, bar_rect, knob_rect))

            # Display volume percentage text
            vol_percent = int(vol * 100)
            vol_text = font.render(f"{vol_percent}%", True, BLACK)
            screen.blit(vol_text, (slider_x + slider_width + 20, y - font_size // 2))

        # Show Back Button
        back_text = translations[current_language]["back"]
        back_color = RED if pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50).collidepoint(mouse_pos) else GRAY
        back_rect = draw_text_center(back_text, font, back_color, screen, HEIGHT - 60)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running_sound_setting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    menu_click_sound.play()
                    running_sound_setting = False
                # Press the slider to start dragging
                for label, bar_rect, knob_rect in slider_rects:
                    if knob_rect.collidepoint(event.pos) or bar_rect.collidepoint(event.pos):
                        dragging_slider = label
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_slider = None
        
        # Drag the slider to adjust the volume
        if dragging_slider:
            _, bar_rect, _ = next(i for i in slider_rects if i[0] == dragging_slider)
            # Calculate slider position (mouse x controls volume)
            relative_x = mouse_pos[0] - bar_rect.left
            new_vol = max(0, min(1, relative_x / slider_width))
            if dragging_slider == translations[current_language]["master_volume"]:
                master_volume = new_vol
            elif dragging_slider == translations[current_language]["bgm"]:
                music_volume = new_vol
            elif dragging_slider == translations[current_language]["se"]:
                sfx_volume = new_vol

        pygame.mixer.music.set_volume(music_volume * master_volume)

        menu_click_sound.set_volume(sfx_volume * master_volume)
        door_open_sound.set_volume(sfx_volume * master_volume)
        hit_sound.set_volume(sfx_volume * master_volume)

        pygame.display.flip()

def show_HowToPlay():
    running_HowToPlay = True

    while running_HowToPlay:
        screen.fill(GRAY)

        draw_text_center(translations[current_language]["how_to_play"], font, WHITE, screen, HEIGHT // 4)

        draw_text_center(translations[current_language]["htp_line1"], font, WHITE, screen, HEIGHT // 4 + 60)
        draw_text_center(translations[current_language]["htp_line2"], font, WHITE, screen, HEIGHT // 4 + 120)
        draw_text_center(translations[current_language]["htp_line3"], font, WHITE, screen, HEIGHT // 4 + 180)

        item_y_pos = HEIGHT // 4 + 240

        screen.blit(item_images['red'], (WIDTH // 2 - 20, item_y_pos))
        screen.blit(item_images['blue'], (WIDTH // 2 - 80, item_y_pos))
        screen.blit(item_images['yellow'], (WIDTH // 2 + 40, item_y_pos))

        mouse_pos = pygame.mouse.get_pos()

        y_pos = HEIGHT // 2 + 120
        color = RED if pygame.Rect(WIDTH // 2 - 100, y_pos - 20, 200, 40).collidepoint(mouse_pos) else WHITE
        rect = draw_text_center(translations[current_language]["back"], font, color, screen, y_pos)
        option_rects = [(translations[current_language]["back"], rect)]

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running_HowToPlay = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option, rect in option_rects:
                    if rect.collidepoint(event.pos):
                        if option == translations[current_language]["back"]:
                            menu_click_sound.play()
                            running_HowToPlay = False

def difficulty_parameter_setting(level):
    global BOOST_SPEED, ENEMY_SPEED, HATE_VALUE, BOOST_DURATION, FREEZE_DURATION, ENEMY_MOVE_INTERVAL, INVISIBLE_DURATION, RED_DURATION, BLUE_DURATION, SPAWN_ITEMS_TIMES
    if level == "easy":
        BOOST_SPEED = 4
        ENEMY_SPEED = 2 + HATE_VALUE
        BOOST_DURATION = 5000
        FREEZE_DURATION = 3000
        ENEMY_MOVE_INTERVAL = 275
        INVISIBLE_DURATION = 5
        RED_DURATION = 7000
        BLUE_DURATION = 7000
        SPAWN_ITEMS_TIMES = 5
        print("Now is easy")
    if level == "normal":
        BOOST_SPEED = 4
        ENEMY_SPEED = 3 + HATE_VALUE
        BOOST_DURATION = 4000
        FREEZE_DURATION = 3000
        ENEMY_MOVE_INTERVAL = 200
        INVISIBLE_DURATION = 3
        RED_DURATION = 5000
        BLUE_DURATION = 5000
        SPAWN_ITEMS_TIMES = 4
        print("Now is normal")
    if level == "difficult":
        BOOST_SPEED = 5
        ENEMY_SPEED = 4 + HATE_VALUE
        BOOST_DURATION = 4000
        FREEZE_DURATION = 3000
        ENEMY_MOVE_INTERVAL = 150
        INVISIBLE_DURATION = 3
        RED_DURATION = 3000
        BLUE_DURATION = 3000
        SPAWN_ITEMS_TIMES = 3
        print("Now is difficult")

def get_non_overlapping_positions():
    key_pos = random_walkable_position()
    while True:
        exit_pos = random_walkable_position()
        # Calculate the distance
        dx = abs(exit_pos[0] - key_pos[0])
        dy = abs(exit_pos[1] - key_pos[1])
        if dx >= TILE_SIZE*10 or dy >= TILE_SIZE*10:
            break
    return key_pos, exit_pos

def kill_all_sprite():
    player_group.empty()
    enemy_group.empty()
    item_group.empty()
    key_group.empty()

player = Player((TILE_SIZE, TILE_SIZE))
player_group = pygame.sprite.Group(player)
enemy_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()

key_pos, exit_pos = 0, 0

key = 0

game_exit_rect = 0

has_key = False
start_time = time.time()
boost_timer = 0
running = True

spawn_enemy_after_delay = False
spawn_enemy_delay_start = 0

paused = False

show_menu()

while running:
    dt = clock.tick(60) # Set a fixed FPS, default as 60
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = True
        elif event.type == pygame.USEREVENT + 2:
            # Accept the signal of enemy of frozen
            for enemy in enemy_group:
                enemy.frozen = False
    
    if paused:
        action = show_pause_menu()
        if action == "main_menu":
            show_menu()
        paused = False
        continue

    if spawn_enemy_after_delay:
        enemy_group.add(Enemy((TILE_SIZE, TILE_SIZE)))
        spawn_enemy_after_delay = False

    player.update(keys)

    if time.time() - start_time > INVISIBLE_DURATION and len(enemy_group) == 0:
        enemy_group.add(Enemy((TILE_SIZE, TILE_SIZE)))

    for enemy in enemy_group:
        enemy.update(player)

    # ==== Handling item pickup ====
    for item in pygame.sprite.spritecollide(player, item_group, True):
        if item.type == 'red':
            player.conditional_effect_active_red = True
            player.conditional_effect_start_time_red = pygame.time.get_ticks()
        elif item.type == 'blue':
            player.conditional_effect_active_blue = True
            player.conditional_effect_start_time_blue = pygame.time.get_ticks()
        elif item.type == 'yellow':
            player.speed = BOOST_SPEED
            boost_timer = pygame.time.get_ticks()

    # Speed-up effect restored
    if pygame.time.get_ticks() - boost_timer > BOOST_DURATION:
        player.speed = PLAYER_SPEED

    collected_keys = pygame.sprite.spritecollide(player, key_group, True)
    if collected_keys:
        has_key = True

    if has_key and player.rect.colliderect(game_exit_rect):
        door_open_sound.play()
        show_victory_screen()
        show_menu()
        continue

    # ==== Enemies collide with player ====
    enemy_hit = pygame.sprite.spritecollideany(player, enemy_group)
    now = pygame.time.get_ticks()
    if enemy_hit:
        if player.invincible:
            pass # Skip when invincible
        elif player.conditional_effect_active_red:
            # Trigger the red item effect (eliminate the enemy, restart the enemy production timer)
            for enemy in enemy_group:
                enemy.kill()
                HATE_VALUE += 2
            spawn_enemy_after_delay = True
            spawn_enemy_delay_start = pygame.time.get_ticks()
            player.conditional_effect_active_red = False
            player.invincible = True
            player.invincible_start_time = pygame.time.get_ticks()
        elif player.conditional_effect_active_blue:
            # Trigger blue item effect (freeze enemy, time to thaw)
            for enemy in enemy_group:
                enemy.frozen = True
            pygame.time.set_timer(pygame.USEREVENT + 2, FREEZE_DURATION, loops=1)
            player.conditional_effect_active_blue = False
            player.invincible = True
            player.invincible_start_time = now
        else:
            # caught by enemy
            hit_sound.play()
            show_game_over_screen()
            show_menu()
            continue

    # ==== Draw logics ====
    for row_idx, row in enumerate(MAZE):
        for col_idx, tile in enumerate(row):
            color = GRAY if tile == 0 else BLACK
            rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)

    player_group.draw(screen)
    enemy_group.draw(screen)
    item_group.draw(screen)
    key_group.draw(screen)
    screen.blit(exit_image, game_exit_rect.topleft)

    remain_time = max(0, int(INVISIBLE_DURATION - (time.time() - start_time)))
    screen.blit(font.render(f"{translations[current_language]["invisible_time"]} {remain_time}s", True, YELLOW), (10, 10))
    if has_key:
        screen.blit(font.render(translations[current_language]["is_key_obtained"], True, GREEN), (10, 40))

    red_icon = item_images['red']
    blue_icon = item_images['blue']

    y_start = 70  # The y coordinate of the text start
    line_height = font.get_height() + 2  # Line height spacing, adjustable
    icon_size = 40  # Image width and height

    # First line of message: Invincibility time
    msg1 = ""
    if player.invincible:
        left = 3 - (pygame.time.get_ticks() - player.invincible_start_time) / 1000
        msg1 += f"{translations[current_language]['invincible_time']}{max(0,int(left))}s"
    if msg1:
        text_surface1 = font.render(msg1, True, RED)
        screen.blit(text_surface1, (10, y_start))

    # The starting y coordinate of the second row (red item time)
    y_next = y_start + line_height

    if player.conditional_effect_active_red:
        left = RED_DURATION / 1000 - (pygame.time.get_ticks() - player.conditional_effect_start_time_red) / 1000
        msg_red = f"{translations[current_language]['red_time']}{max(0,int(left))}s"
        text_surface_red = font.render(msg_red, True, RED)

        # draw a icon for red item
        screen.blit(red_icon, (10, y_next))
        # Draw the text, offset 40 pixels to the right (the image width), plus a little spacing
        screen.blit(text_surface_red, (10 + icon_size + 5, y_next))

        y_next += line_height

    # The starting y coordinate of the third row (blue item time)
    if player.conditional_effect_active_blue:
        left = BLUE_DURATION / 1000 - (pygame.time.get_ticks() - player.conditional_effect_start_time_blue) / 1000
        msg_blue = f"{translations[current_language]['blue_time']}{max(0,int(left))}s"
        text_surface_blue = font.render(msg_blue, True, RED)

        # draw a icon for blue item
        screen.blit(blue_icon, (10, y_next))
        # Draw the text, offset 40 pixels to the right (the image width), plus a little spacing
        screen.blit(text_surface_blue, (10 + icon_size + 5, y_next))

    pygame.display.flip()

pygame.quit()
sys.exit()
