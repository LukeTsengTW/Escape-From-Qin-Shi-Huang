import pygame
import constants
from translations import translations, current_language
from maze import MAZE

# Global variable to be set by main.py
screen = None

def get_game_state():
    from game_state import game_state
    return game_state

def get_assets():
    from assets import font, item_images, exit_image
    return font, item_images, exit_image

def draw_game_screen():
    if screen is None:
        raise RuntimeError("Screen not initialized")
        
    game_state = get_game_state()
    font, item_images, exit_image = get_assets()

    """Draw all game elements"""
    # Draw maze
    for row_idx, row in enumerate(MAZE):
        for col_idx, tile in enumerate(row):
            color = constants.GRAY if tile == 0 else constants.BLACK
            rect = pygame.Rect(col_idx * constants.TILE_SIZE, row_idx * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE)
            pygame.draw.rect(screen, color, rect)

    # Draw sprites
    game_state.player_group.draw(screen)
    game_state.enemy_group.draw(screen)
    game_state.item_group.draw(screen)
    game_state.key_group.draw(screen)
    screen.blit(exit_image, game_state.game_exit_rect.topleft)

    # Draw UI
    draw_ui()
    
    # Draw enemies with special effects
    for enemy in game_state.enemy_group:
        enemy.draw(screen)

    # Draw player with effects
    game_state.player.draw(screen)

    pygame.display.flip()

def draw_ui():
    """Draw UI elements"""
    game_state = get_game_state()
    font, item_images, exit_image = get_assets()
    
    # Timer (using adjusted time)
    elapsed_time = game_state.get_elapsed_time()
    remain_time = max(0, int((constants.INVISIBLE_DURATION - elapsed_time) / 1000))
    screen.blit(font.render(f"{translations[current_language]['invisible_time']} {remain_time}s", True, constants.YELLOW), (10, 10))
    
    # Key status
    if game_state.has_key:
        screen.blit(font.render(translations[current_language]["is_key_obtained"], True,constants. GREEN), (10, 40))

    # Effects UI
    draw_effects_ui()

def draw_effects_ui():
    """Draw effects UI"""
    game_state = get_game_state()
    font, item_images, exit_image = get_assets()
    
    red_icon = item_images['red']
    blue_icon = item_images['blue']
    y_start = 70
    line_height = font.get_height() + 25
    icon_size = 40
    
    current_time = game_state.get_adjusted_time()

    # Invincibility
    if game_state.player.invincible:
        left = 3 - (current_time - game_state.player.invincible_start_time) / 1000
        msg = f"{translations[current_language]['invincible_time']}{max(0,int(left))}s"
        text_surface = font.render(msg, True, constants.RED)
        screen.blit(text_surface, (10, y_start))

    y_next = y_start + line_height

    # Red effect
    if game_state.player.conditional_effect_active_red:
        left = constants.RED_DURATION / 1000 - (current_time - game_state.player.conditional_effect_start_time_red) / 1000
        msg = f"{translations[current_language]['red_time']}{max(0,int(left))}s"
        text_surface = font.render(msg, True, constants.RED)
        screen.blit(red_icon, (10, y_next))
        screen.blit(text_surface, (10 + icon_size + 5, y_next))
        y_next += line_height

    # Blue effect
    if game_state.player.conditional_effect_active_blue:
        left = constants.BLUE_DURATION / 1000 - (current_time - game_state.player.conditional_effect_start_time_blue) / 1000
        msg = f"{translations[current_language]['blue_time']}{max(0,int(left))}s"
        text_surface = font.render(msg, True, constants.RED)
        screen.blit(blue_icon, (10, y_next))
        screen.blit(text_surface, (10 + icon_size + 5, y_next))