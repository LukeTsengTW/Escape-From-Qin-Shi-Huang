import pygame
import constants
from assets import *
from game_objects import Enemy
from music_manager import setup_game_music, setup_menu_music
from renderer import draw_game_screen

# Global variables to be set by main.py
screen = None
clock = None

def get_game_state():
    from game_state import game_state
    return game_state

def get_menu_functions():
    from menu_functions import show_pause_menu, show_victory_screen, show_game_over_screen
    return show_pause_menu, show_victory_screen, show_game_over_screen

def main_game_loop():
    if screen is None or clock is None:
        raise RuntimeError("Screen and clock not initialized")
        
    game_state = get_game_state()
    show_pause_menu, show_victory_screen, show_game_over_screen = get_menu_functions()

    """Main game loop"""
    setup_game_music()
    
    while game_state.running:
        dt = clock.tick(60)
        screen.fill(constants.BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state.pause_game()
            elif event.type == pygame.USEREVENT + 2:
                # Unfreeze enemies
                for enemy in game_state.enemy_group:
                    enemy.freeze_current_frame = 0
                    enemy.frozen = False
        
        if game_state.paused:
            action = show_pause_menu()
            if action == "main_menu":
                setup_menu_music()
                return "main_menu"
            elif action == "resume" or action is None:
                game_state.resume_game()
                setup_game_music()
            continue

        if game_state.spawn_enemy_after_delay:
            game_state.enemy_group.add(Enemy((constants.TILE_SIZE, constants.TILE_SIZE)))
            game_state.spawn_enemy_after_delay = False

        game_state.player.update(keys)

        # Spawn enemy after invisible duration (using adjusted time)
        if game_state.get_elapsed_time() > constants.INVISIBLE_DURATION and len(game_state.enemy_group) == 0:
            new_enemy = Enemy((constants.TILE_SIZE, constants.TILE_SIZE))
            new_enemy.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
            game_state.enemy_group.add(Enemy((constants.TILE_SIZE, constants.TILE_SIZE)))

        # Update enemies and remove completed death animations
        enemies_to_remove = []
        for enemy in game_state.enemy_group:
            enemy.update(game_state.player)
            
            # Check if the death animation is complete
            if enemy.dying and enemy.is_death_animation_complete():
                enemies_to_remove.append(enemy)
        
        # Remove enemies whose death animations have completed and respawn new enemies
        for enemy in enemies_to_remove:
            enemy.kill()
            # New enemies spawn at the starting point
            new_enemy = Enemy((constants.TILE_SIZE, constants.TILE_SIZE))
            new_enemy.speed = constants.ENEMY_SPEED + constants.HATE_VALUE
            game_state.enemy_group.add(new_enemy)

        # Handle item pickup
        handle_item_pickup()
        
        # Handle speed boost timer
        handle_speed_boost()
        
        # Handle key collection
        handle_key_collection()
        
        # Check victory condition
        if check_victory_condition():
            return "main_menu"
        
        # Handle enemy collision
        if handle_enemy_collision():
            return "main_menu"

        # Draw everything
        draw_game_screen()
    
    return "main_menu"

def handle_item_pickup():
    """Handle item pickup logic"""
    game_state = get_game_state()
    for item in pygame.sprite.spritecollide(game_state.player, game_state.item_group, True):
        pickUp_sound.play()
        if item.type == 'red':
            game_state.player.conditional_effect_active_red = True
            game_state.player.conditional_effect_start_time_red = game_state.get_adjusted_time()
        elif item.type == 'blue':
            game_state.player.conditional_effect_active_blue = True
            game_state.player.conditional_effect_start_time_blue = game_state.get_adjusted_time()
        elif item.type == 'yellow':
            game_state.player.increase_permanent_speed()

            game_state.player.is_boost = True
            game_state.player.speed = constants.BOOST_SPEED
            game_state.boost_timer = game_state.get_adjusted_time()

def handle_speed_boost():
    """Handle speed boost timer"""
    game_state = get_game_state()
    if game_state.get_adjusted_time() - game_state.boost_timer > constants.BOOST_DURATION:
        game_state.player.is_boost = False
        game_state.player.speed = game_state.player.base_speed

def handle_key_collection():
    """Handle key collection"""
    game_state = get_game_state()
    collected_keys = pygame.sprite.spritecollide(game_state.player, game_state.key_group, True)
    if collected_keys:
        game_state.has_key = True
        constants.HATE_VALUE += 1
        new_enemy_speed = constants.ENEMY_SPEED + constants.HATE_VALUE
        for enemy in game_state.enemy_group:
            enemy.speed = new_enemy_speed

def check_victory_condition():
    """Check if player has won"""
    game_state = get_game_state()
    show_pause_menu, show_victory_screen, show_game_over_screen = get_menu_functions()
    
    if game_state.has_key and game_state.player.rect.colliderect(game_state.game_exit_rect):
        door_open_sound.play()
        show_victory_screen()
        return True
    return False

def handle_enemy_collision():
    """Handle enemy collision with player"""
    game_state = get_game_state()
    show_pause_menu, show_victory_screen, show_game_over_screen = get_menu_functions()
    
    # Only check for non-dead enemies
    alive_enemies = [enemy for enemy in game_state.enemy_group if not enemy.dying]
    enemy_hit = None
    
    for enemy in alive_enemies:
        if enemy.rect.colliderect(game_state.player.rect):
            enemy_hit = enemy
            break
    
    now = game_state.get_adjusted_time()
    
    if enemy_hit:
        if game_state.player.invincible:
            return False
        elif game_state.player.conditional_effect_active_red:
            # Red item effect - Slash
            sword_sound.play()
            
            enemy_hit.start_dying()
            
            constants.HATE_VALUE += 1

            new_enemy_speed = constants.ENEMY_SPEED + constants.HATE_VALUE
            for enemy in game_state.enemy_group:
                enemy.speed = new_enemy_speed
            
            print(f"Hate value increased to: {constants.HATE_VALUE}, Enemy speed now: {new_enemy_speed}")
            
            for enemy in alive_enemies:
                if enemy != enemy_hit:
                    enemy.start_attack()
            
            # Removes red effect and grants temporary invincibility
            game_state.player.conditional_effect_active_red = False
            game_state.player.invincible = True
            game_state.player.invincible_start_time = now
            
        elif game_state.player.conditional_effect_active_blue:
            # Blue item effect - Freeze
            freeze_sound.play()

            constants.HATE_VALUE += 1
            
            new_enemy_speed = constants.ENEMY_SPEED + constants.HATE_VALUE
            for enemy in game_state.enemy_group:
                enemy.speed = new_enemy_speed
                if not enemy.dying:
                    enemy.frozen = True
            pygame.time.set_timer(pygame.USEREVENT + 2, constants.FREEZE_DURATION, loops=1)
            game_state.player.conditional_effect_active_blue = False
            game_state.player.invincible = True
            game_state.player.invincible_start_time = now
        else:
            # Game over - No Any Protect Effect
            hit_sound.play()
            show_game_over_screen()
            return True
    return False