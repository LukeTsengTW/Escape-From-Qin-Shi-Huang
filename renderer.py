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

    """Draw all game elements with camera offset"""
    # Update camera
    game_state.update_camera()
    
    # Clear screen
    screen.fill(constants.BLACK)
    
    # Draw maze with camera offset
    visible_area = game_state.camera.get_visible_area()
    
    # Calculate the range of tiles that need to be rendered
    start_col = max(0, int(visible_area.left // constants.TILE_SIZE))
    end_col = min(len(MAZE[0]), int((visible_area.right // constants.TILE_SIZE) + 1))
    start_row = max(0, int(visible_area.top // constants.TILE_SIZE))
    end_row = min(len(MAZE), int((visible_area.bottom // constants.TILE_SIZE) + 1))
    
    for row_idx in range(start_row, end_row):
        for col_idx in range(start_col, end_col):
            if row_idx < len(MAZE) and col_idx < len(MAZE[0]):
                tile = MAZE[row_idx][col_idx]
                color = constants.GRAY if tile == 0 else constants.BLACK
                world_rect = pygame.Rect(col_idx * constants.TILE_SIZE, row_idx * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE)
                screen_rect = game_state.camera.apply(world_rect)
                pygame.draw.rect(screen, color, screen_rect)

    # Draw sprites with camera offset
    draw_sprites_with_camera(game_state.item_group)
    draw_sprites_with_camera(game_state.key_group)
    
    # Draw exit
    exit_screen_rect = game_state.camera.apply(game_state.game_exit_rect)
    screen.blit(exit_image, exit_screen_rect.topleft)

    # Draw enemies with special effects
    for enemy in game_state.enemy_group:
        enemy_screen_rect = game_state.camera.apply(enemy.rect)
        # Only draw enemies within the visible area
        if enemy_screen_rect.colliderect(pygame.Rect(0, 0, constants.WIDTH, constants.HEIGHT)):
            # Create a temporary surface to draw the enemy effects
            temp_surface = pygame.Surface((enemy.rect.width, enemy.rect.height), pygame.SRCALPHA)
            enemy.draw(temp_surface)
            screen.blit(temp_surface, enemy_screen_rect.topleft)

    # Draw player with effects
    player_screen_rect = game_state.camera.apply(game_state.player.rect)
    # Create a larger temporary surface to hold the stamina bar
    temp_surface_width = game_state.player.rect.width
    temp_surface_height = game_state.player.rect.height + 20  # Add 20 pixels to the stamina bar
    temp_surface = pygame.Surface((temp_surface_width, temp_surface_height), pygame.SRCALPHA)
    
    # Draw the player on a temporary surface (offset to the bottom)
    temp_surface.blit(game_state.player.image, (0, 20))
    
    # Drawing acceleration effect
    if game_state.player.is_boost and len(game_state.player.boost_frames) > 0:
        temp_surface.blit(game_state.player.boost_frames[game_state.player.boost_current_frame], (0, 20))
    
    # Draw the stamina bar at the top
    game_state.player.draw_stamina_bar_at_top(temp_surface)
    
    # Adjust drawing position
    adjusted_rect = pygame.Rect(player_screen_rect.x, player_screen_rect.y - 20, temp_surface_width, temp_surface_height)
    screen.blit(temp_surface, adjusted_rect.topleft)

    # Draw UI (UI elements don't use camera offset)
    draw_ui()

    pygame.display.flip()

def draw_sprites_with_camera(sprite_group):
    """Drawing sprite groups using camera offset"""
    game_state = get_game_state()
    
    for sprite in sprite_group:
        screen_rect = game_state.camera.apply(sprite.rect)
        # Only draw sprites within the visible area
        if screen_rect.colliderect(pygame.Rect(0, 0, constants.WIDTH, constants.HEIGHT)):
            screen.blit(sprite.image, screen_rect.topleft)

def draw_ui():
    """Draw UI elements (UI is not affected by the camera)"""
    game_state = get_game_state()
    font, item_images, exit_image = get_assets()
    
    # Timer (using adjusted time)
    elapsed_time = game_state.get_elapsed_time()
    remain_time = max(0, int((constants.INVISIBLE_DURATION - elapsed_time) / 1000))
    screen.blit(font.render(f"{translations[current_language]['invisible_time']} {remain_time}s", True, constants.YELLOW), (10, 10))
    
    # Key status
    if game_state.has_key:
        screen.blit(font.render(translations[current_language]["is_key_obtained"], True, constants.GREEN), (10, 40))
    
    draw_stamina_ui()

    # Effects UI
    draw_effects_ui()

def draw_stamina_ui():
    game_state = get_game_state()
    font, item_images, exit_image = get_assets()
    
    player = game_state.player
    
    # Stamina bar location (upper right corner of the screen)
    bar_width = 100
    bar_height = 8
    bar_x = constants.WIDTH - bar_width - 10
    bar_y = 10
    
    # Label
    stamina_text = font.render(f"{translations[current_language]['stamina']}: ", True, constants.WHITE)
    screen.blit(stamina_text, (bar_x - stamina_text.get_width() - 5, bar_y - 2))
    
    # Background strips (gray)
    bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
    pygame.draw.rect(screen, constants.GRAY, bg_rect)
    
    # Stamina bar (green to red gradient)
    stamina_ratio = player.stamina / constants.STAMINA_MAX
    stamina_width = int(bar_width * stamina_ratio)
    
    if stamina_width > 0:
        # Change color according to stamina ratio
        if stamina_ratio > 0.6:
            color = constants.GREEN
        elif stamina_ratio > 0.3:
            color = (255, 255, 0)  # Yellow
        else:
            color = constants.RED
        
        stamina_rect = pygame.Rect(bar_x, bar_y, stamina_width, bar_height)
        pygame.draw.rect(screen, color, stamina_rect)
    
    # frame
    pygame.draw.rect(screen, constants.BLACK, bg_rect, 1)

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