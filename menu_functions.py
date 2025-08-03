import pygame
import sys
import webbrowser
import constants
from assets import *
from translations import translations, current_language
from menu_system import *
from music_manager import setup_menu_music, setup_game_music
from game_state import initialize_game_state, kill_all_sprite
from config import save_config, load_config

config = load_config()

# Global variables to be set by main.py
screen = None
clock = None

def get_game_logic():
    """Delay import of game_logic to avoid circular dependencies"""
    from game_logic import main_game_loop
    return main_game_loop

def create_menu_buttons():
    """Create all menu buttons"""
    return [
        MenuButton(translations[current_language]["play"], constants.HEIGHT // 2, "play"),
        MenuButton(translations[current_language]["setting"], constants.HEIGHT // 2 + 60, "setting"),
        MenuButton(translations[current_language]["how_to_play"], constants.HEIGHT // 2 + 120, "how_to_play"),
        MenuButton("github", constants.HEIGHT // 2 + 180, "website"),
        MenuButton(translations[current_language]["exit"], constants.HEIGHT // 2 + 240, "exit")
    ]

def show_menu():
    """Main menu function"""
    global FIRST_OPEN_GAME, config
    
    if screen is None:
        raise RuntimeError("Screen not initialized. Please set screen in main.py")
    
    # Set first open flag and cleanup
    FIRST_OPEN_GAME = True
    config["first_open_game"] = FIRST_OPEN_GAME
    kill_all_sprite()
    
    setup_menu_music()
    buttons = create_menu_buttons()
    running_menu = True

    while running_menu:
        # Draw background
        draw_menu_background()
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw buttons
        button_rects = {}
        for button in buttons:
            rect = button.draw(screen, font, mouse_pos)
            button_rects[button.action] = (button, rect)
        
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_config(config)
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for action, (button, rect) in button_rects.items():
                    if rect.collidepoint(event.pos):
                        running_menu = handle_menu_action(action)
                        break

def show_settings():
    handler = SettingsMenuHandler(translations[current_language]["setting"], [])
    handler.run()

def show_language_selection():
    options = [
        MenuOption(translations["zh_tw"]["traditional_chinese"], "zh_tw"),
        MenuOption(translations["zh_cn"]["simplified_chinese"], "zh_cn"),
        MenuOption(translations["en"]["english"], "en"),
        MenuOption(translations[current_language]["back"], "back")
    ]
    handler = LanguageMenuHandler(translations[current_language]["select_language"], options)
    handler.run()

def show_difficulty():
    options = [
        MenuOption(translations[current_language]["easy"], "easy"),
        MenuOption(translations[current_language]["normal"], "normal"),
        MenuOption(translations[current_language]["difficult"], "difficult"),
        MenuOption(translations[current_language]["back"], "back")
    ]
    handler = DifficultyMenuHandler(translations[current_language]["difficulty_setting"], options)
    handler.run()

def show_resolution_selection():
    options = []
    
    for width, height in constants.RESOLUTION_OPTIONS:
        resolution_text = f"{width}x{height}"
        options.append(MenuOption(resolution_text, resolution_text))
    
    options.append(MenuOption(translations[current_language]["back"], "back"))
    
    handler = ResolutionMenuHandler(translations[current_language]["resolution_setting"], options)
    handler.run()

def show_pause_menu():
    options = [
        MenuOption(translations[current_language]["resume"], "resume"),
        MenuOption(translations[current_language]["setting"], "setting"),
        MenuOption(translations[current_language]["back_menu"], "back_menu")
    ]
    handler = PauseMenuHandler(translations[current_language]["game_paused"], options)
    return handler.run()

def show_game_over_screen():
    """Show game over screen and handle return"""
    handler = GameOverMenuHandler()
    result = handler.run()
    return "back_menu"

def show_victory_screen():
    """Show victory screen and handle return"""
    handler = VictoryMenuHandler()
    result = handler.run()
    return "back_menu"

def show_sound_setting():
    handler = SoundSettingHandler()
    handler.run()

def show_HowToPlay():
    handler = HowToPlayMenuHandler()
    handler.run()

def show_game_mode_selection():
    """Show game mode selection menu"""
    handler = GameModeMenuHandler()
    return handler.run()

def show_level_selection():
    """Show level selection menu"""
    handler = LevelSelectionMenuHandler()
    return handler.run()

def draw_menu_background():
    """Draw menu background elements"""
    if screen is None or font is None:
        raise RuntimeError("Screen or font not initialized")
        
    screen.fill(constants.WHITE)
    
    # Draw title
    title_font = pygame.font.Font("assets/Cubic_11.ttf", 48)
    screen_title = translations[current_language]["title"]
    draw_text_center(screen_title, title_font, constants.BLACK, screen, constants.HEIGHT // 4)
    
    # Draw version
    draw_text_center(constants.current_version, font, constants.BLACK, screen, constants.HEIGHT - 18)
    
    # Draw background images (only if loaded)
    if menu_image_1 and menu_image_2:
        left_margin = constants.WIDTH * 0.05  # The left margin is 5% of the screen width
        image1_width = 194 * 1.5
        image1_height = 259 * 1.5
        image1_x = left_margin
        image1_y = constants.HEIGHT // 4 + 20
        
        menu_image_1_scaled = pygame.transform.scale(menu_image_1, (int(image1_width), int(image1_height)))
        menu_image_1_scaled = pygame.transform.flip(menu_image_1_scaled, True, False)
        
        right_margin = constants.WIDTH * 0.03  # The right margin is 5% of the screen width
        image2_width = 408 * 0.8  # Slightly scaled down to accommodate different resolutions
        image2_height = 612 * 0.8
        image2_x = constants.WIDTH - right_margin - image2_width
        image2_y = constants.HEIGHT // 4 + 20
        
        menu_image_2_scaled = pygame.transform.scale(menu_image_2, (int(image2_width), int(image2_height)))
        
        screen.blit(menu_image_1_scaled, (image1_x, image1_y))
        screen.blit(menu_image_2_scaled, (image2_x, image2_y))

def handle_menu_action(action):
    global config
    """Handle menu button actions"""
    config = load_config()
    menu_click_sound.play()
    
    if action == "play":
        # Show game mode selection first
        selected_mode = show_game_mode_selection()
        if selected_mode == "level_mode":
            # Show level selection menu
            selected_level = show_level_selection()
            if selected_level is not None:
                # Level mode - use selected level
                main_game_loop = get_game_logic()
                initialize_game_state(regenerate_maze_flag=False, game_mode="level", level_number=selected_level)
                result = main_game_loop()
                setup_menu_music()
        elif selected_mode == "random_mode":
            # Random mode - use existing random generation
            main_game_loop = get_game_logic()
            initialize_game_state(regenerate_maze_flag=True, game_mode="random")
            result = main_game_loop()
            setup_menu_music()
        # If user pressed back, do nothing and return to main menu
        return True  # Continue menu loop
        
    elif action == "setting":
        show_settings()
        
    elif action == "how_to_play":
        show_HowToPlay()
        
    elif action == "website":
        webbrowser.open("https://github.com/LukeTsengTW/Escape-From-Qin-Shi-Huang")
        
    elif action == "exit":
        config = load_config()
        save_config(config)
        pygame.quit()
        sys.exit()
    
    return True  # Continue menu loop