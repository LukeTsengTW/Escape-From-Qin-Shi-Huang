import pygame
from config import load_config

config = load_config()

# Volume settings
master_volume, music_volume, sfx_volume = config["master_volume"], config["music_volume"], config["sfx_volume"]

# Initialize mixer (can be done before display initialization)
pygame.mixer.init()

# Load sounds (can be done anytime after mixer init)
menu_click_sound = pygame.mixer.Sound("assets/sound/sound_effect/menu/menu_selection_click.ogg")
door_open_sound = pygame.mixer.Sound("assets/sound/sound_effect/door_open/door_open.ogg")
hit_sound = pygame.mixer.Sound("assets/sound/sound_effect/hit/hit.ogg")
sword_sound = pygame.mixer.Sound("assets/sound/sound_effect/hit/sword.ogg")
freeze_sound = pygame.mixer.Sound("assets/sound/sound_effect/hit/freeze.ogg")
pickUp_sound = pygame.mixer.Sound("assets/sound/sound_effect/pick_up/pick_up.ogg")

# Set initial volumes
pygame.mixer.music.set_volume(music_volume * master_volume)
for sound in [menu_click_sound, door_open_sound, hit_sound, sword_sound, freeze_sound, pickUp_sound]:
    sound.set_volume(sfx_volume * master_volume)

# Load music paths (just strings, no pygame operations needed)
menu_music_path = "assets/sound/bgm/menu/menu_bgm.ogg"
playing_music_path = "assets/sound/bgm/playing/c1.ogg"
victory_music_path = "assets/sound/bgm/victory/victory.ogg"
gameover_music_path = "assets/sound/bgm/gameover/gameover.ogg"

# Initialize font (can be done after pygame.init())
font = None

# Image variables (will be loaded after display initialization)
menu_image_1 = None
menu_image_2 = None
exit_image = None
item_images = {}
key_images = []

def load_images():
    """Load all images after pygame display is initialized"""
    global menu_image_1, menu_image_2, exit_image, item_images, key_images, font
    
    # Load images with convert_alpha() for better performance
    menu_image_1 = pygame.image.load("assets/img/menu/background_1.png").convert_alpha()
    menu_image_2 = pygame.image.load("assets/img/menu/background_2.png").convert_alpha()
    exit_image = pygame.image.load("assets/img/exit/exit.png").convert_alpha()

    item_images = {
        'red': pygame.image.load("assets/img/items/sword/sword.png").convert_alpha(),
        'yellow': pygame.image.load("assets/img/items/bolt/bolt.png").convert_alpha(),
        'blue': pygame.image.load("assets/img/items/snowflake/snowflake.png").convert_alpha()
    }

    key_images = [
        pygame.image.load("assets/img/items/keys/key_1.png").convert_alpha(),
        pygame.image.load("assets/img/items/keys/key_2.png").convert_alpha(),
        pygame.image.load("assets/img/items/keys/key_3.png").convert_alpha(),
        pygame.image.load("assets/img/items/keys/key_4.png").convert_alpha()
    ]
    
    # Load font
    font = pygame.font.Font("assets/Cubic_11.ttf", 18)

def update_volumes():
    """Update all sound volumes when settings change"""
    pygame.mixer.music.set_volume(music_volume * master_volume)
    for sound in [menu_click_sound, door_open_sound, hit_sound, sword_sound, freeze_sound, pickUp_sound]:
        sound.set_volume(sfx_volume * master_volume)