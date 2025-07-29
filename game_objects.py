import pygame
import time
import random
import os
import constants
from maze import walls, a_star, is_path

def get_game_state():
    from game_state import game_state
    return game_state

def load_frames_safely(base_path, count, start_from=1):
    """Safely load animation frames, skip if the file does not exist"""
    frames = []
    for i in range(start_from, start_from + count):
        file_path = f"{base_path}/frame-{i}.png"
        if os.path.exists(file_path):
            frames.append(pygame.image.load(file_path).convert_alpha())
        else:
            print(f"Warning: {file_path} not found, skipping...")
    return frames if frames else [pygame.Surface((40, 40))]  # Returns a blank image if no frame is found

def find_nearest_walkable_position(target_pos):
    """Find the nearest accessible location near the target location"""
    x, y = target_pos
    
    # First check whether the original location is accessible
    if is_path(x + constants.TILE_SIZE // 2, y + constants.TILE_SIZE // 2):
        return target_pos
    
    # If it is not accessible, search for accessible locations nearby
    search_radius = constants.TILE_SIZE
    for radius in range(constants.TILE_SIZE, search_radius * 3, constants.TILE_SIZE):
        for dx in range(-radius, radius + 1, constants.TILE_SIZE):
            for dy in range(-radius, radius + 1, constants.TILE_SIZE):
                if dx == 0 and dy == 0:
                    continue
                    
                test_x = x + dx
                test_y = y + dy
                
                # Make sure it's within the screen
                if 0 <= test_x < constants.WIDTH - constants.TILE_SIZE and 0 <= test_y < constants.HEIGHT - constants.TILE_SIZE:
                    if is_path(test_x + constants.TILE_SIZE // 2, test_y + constants.TILE_SIZE // 2):
                        return (test_x, test_y)
    
    # If not found, return to the original location
    return target_pos

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load animation frames safely
        self.frames = load_frames_safely("assets/img/player", 13, 1)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = self.rect.inflate(-10, -10)
        self.speed = constants.PLAYER_SPEED
        self.base_speed = constants.PLAYER_SPEED
        self.facing_right = True

        # Animation properties
        self.animation_timer = 0
        self.animation_speed = 3
        self.is_moving = False

        # Effect properties
        self.conditional_effect_active_red = False
        self.conditional_effect_start_time_red = 0
        self.conditional_effect_active_blue = False
        self.conditional_effect_start_time_blue = 0
        self.invincible = False
        self.invincible_start_time = 0

        # Boost effect
        self.boost_frames = load_frames_safely("assets/img/items/bolt_effect", 7, 1)
        self.boost_current_frame = 0
        self.boost_animation_timer = 0
        self.boost_animation_speed = 35
        self.is_boost = False
        
        # Stamina System
        self.stamina = constants.STAMINA_MAX  # Current stamina
        self.is_sprinting = False
        self.last_stamina_update = 0

    def get_center_position(self):
        """Get the player's center position for enemy tracking"""
        return (self.rect.centerx, self.rect.centery)
    
    def get_grid_position(self):
        """Get the player's position in the grid"""
        center_x, center_y = self.get_center_position()
        grid_x = (center_x // constants.TILE_SIZE) * constants.TILE_SIZE
        grid_y = (center_y // constants.TILE_SIZE) * constants.TILE_SIZE
        return (grid_x, grid_y)

    def handle_movement(self, keys):
        """Handle player movement with collision detection"""
        dx = dy = 0

        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        self.handle_sprint(shift_pressed)

        # Calculate current speed (base speed + boost + sprint)
        current_speed = self.base_speed
        if self.is_boost:
            current_speed = constants.BOOST_SPEED
        if self.is_sprinting:
            current_speed += constants.SPRINT_SPEED_BONUS
        
        # Get movement input
        if keys[pygame.K_LEFT]:
            dx = -current_speed
            self.facing_right = True
        elif keys[pygame.K_RIGHT]:
            dx = current_speed
            self.facing_right = False
        if keys[pygame.K_UP]:
            dy = -current_speed
        if keys[pygame.K_DOWN]:
            dy = current_speed

        self.is_moving = (dx != 0 or dy != 0)

        # Handle horizontal collision
        if dx != 0:
            new_rect = self.collision_rect.move(dx, 0)
            for wall in walls:
                if new_rect.colliderect(wall):
                    if dx > 0:
                        new_rect.right = wall.left
                    else:
                        new_rect.left = wall.right
                    break
            self.collision_rect.x = new_rect.x

        # Handle vertical collision
        if dy != 0:
            new_rect = self.collision_rect.move(0, dy)
            for wall in walls:
                if new_rect.colliderect(wall):
                    if dy > 0:
                        new_rect.bottom = wall.top
                    else:
                        new_rect.top = wall.bottom
                    break
            self.collision_rect.y = new_rect.y

        self.rect.center = self.collision_rect.center
    
    def handle_sprint(self, shift_pressed):
        """Processing running logic"""
        game_state = get_game_state()
        current_time = game_state.get_adjusted_time()
        
        if self.last_stamina_update == 0:
            self.last_stamina_update = current_time
        
        dt = current_time - self.last_stamina_update
        self.last_stamina_update = current_time
        
        # You can only start running when your stamina is full
        if shift_pressed and self.stamina >= constants.STAMINA_MAX and not self.is_sprinting:
            self.is_sprinting = True
        elif shift_pressed and self.is_sprinting and self.stamina > 0:
            self.stamina = max(0, self.stamina - dt)
            if self.stamina <= 0:
                self.is_sprinting = False
        else:
            self.is_sprinting = False
            if self.stamina < constants.STAMINA_MAX:
                self.stamina = min(constants.STAMINA_MAX, self.stamina + dt * constants.STAMINA_RECOVERY_RATE)

    def update_animation(self):
        """Update player animation"""
        now = pygame.time.get_ticks()
        
        # Update boost animation if active
        if self.is_boost and len(self.boost_frames) > 0 and now - self.boost_animation_timer > self.boost_animation_speed:
            self.boost_animation_timer = now
            self.boost_current_frame = (self.boost_current_frame + 1) % len(self.boost_frames)

        # Update main animation
        if self.is_moving:
            if now - self.animation_timer > self.animation_speed:
                self.animation_timer = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)
        else:
            self.current_frame = 0  # Standing frame

        # Apply facing direction
        frame_image = self.frames[self.current_frame]
        self.image = frame_image if self.facing_right else pygame.transform.flip(frame_image, True, False)

    def update_effects(self):
        """Update player effects and timers"""
        game_state = get_game_state()
        current_time = game_state.get_adjusted_time()

        # Handle invincibility
        if self.invincible and current_time - self.invincible_start_time > 3000:
            self.invincible = False

        # Handle red effect
        if self.conditional_effect_active_red and current_time - self.conditional_effect_start_time_red > constants.RED_DURATION:
            self.conditional_effect_active_red = False

        # Handle blue effect
        if self.conditional_effect_active_blue and current_time - self.conditional_effect_start_time_blue > constants.BLUE_DURATION:
            self.conditional_effect_active_blue = False

    def update(self, keys):
        """Main update method"""
        self.handle_movement(keys)
        self.update_animation()
        self.update_effects()

    def draw(self, surface):
        """Draw player with boost effect if active"""
        if self.is_boost and len(self.boost_frames) > 0:
            surface.blit(self.boost_frames[self.boost_current_frame], self.rect)
        
        self.draw_stamina_bar(surface)

    def draw_stamina_bar(self, surface):
        """Draw the stamina bar"""
        # The stamina bar is only displayed when the stamina is low or when running.
        if self.stamina < constants.STAMINA_MAX or self.is_sprinting:
            bar_x = self.rect.centerx - constants.STAMINA_BAR_WIDTH // 2
            bar_y = self.rect.top - 15
            
            # Background strips (gray)
            bg_rect = pygame.Rect(bar_x, bar_y, constants.STAMINA_BAR_WIDTH, constants.STAMINA_BAR_HEIGHT)
            pygame.draw.rect(surface, constants.GRAY, bg_rect)
            
            # Stamina bar (green to red gradient)
            stamina_ratio = self.stamina / constants.STAMINA_MAX
            stamina_width = int(constants.STAMINA_BAR_WIDTH * stamina_ratio)
            
            if stamina_width > 0:
                # Change color according to health ratio
                if stamina_ratio > 0.6:
                    color = constants.GREEN
                elif stamina_ratio > 0.3:
                    color = (255, 255, 0)  # Yellow
                else:
                    color = constants.RED
                
                stamina_rect = pygame.Rect(bar_x, bar_y, stamina_width, constants.STAMINA_BAR_HEIGHT)
                pygame.draw.rect(surface, color, stamina_rect)
            
            # frame
            pygame.draw.rect(surface, constants.BLACK, bg_rect, 1)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load enemy frames safely
        self.frames = load_frames_safely("assets/img/enemy", 8, 1)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        
        # Enemy properties
        self.speed = constants.ENEMY_SPEED
        self.path = []
        self.path_index = 0
        self.animation_timer = 0
        self.animation_speed = 25
        self.last_target_pos = None
        self.path_update_timer = 0
        self.path_update_interval = 500  # Update path every 500ms
        
        # Direction tracking for sprite flipping
        self.facing_right = True
        self.last_position = pos
        
        # Attack effects
        self.attack_frames = load_frames_safely("assets/img/hit/slash", 12, 0)
        self.attack_current_frame = 0
        self.attack_animation_timer = 0
        self.attack_animation_speed = 50
        self.attacking = False
        
        # Death state and animation
        self.dying = False
        self.death_animation_complete = False
        self.death_start_time = 0
        self.death_duration = len(self.attack_frames) * self.attack_animation_speed if self.attack_frames else 500
        
        # Freeze effect
        self.frozen = False
        self.freeze_current_frame = 0
        self.freeze_frames = load_frames_safely("assets/img/hit/freeze", 62, 1) 
        self.freeze_animation_timer = 0
        self.freeze_animation_speed = 10
        
        # Direct chase mode (Backup plan when path cannot be found)
        self.direct_chase_mode = False
        self.stuck_counter = 0
        self.max_stuck_count = 10

    def start_dying(self):
        """Start death animation"""
        self.dying = True
        self.attacking = True  # Use attack animation as death animation
        self.attack_current_frame = 0
        self.death_start_time = pygame.time.get_ticks()
        self.attack_animation_timer = pygame.time.get_ticks()  # Reset attack animation timer
        
    def is_death_animation_complete(self):
        """Check if the death animation is complete"""
        if not self.dying:
            return False
        
        current_time = pygame.time.get_ticks()
        return current_time - self.death_start_time >= self.death_duration

    def update(self, target):
        """Update enemy state"""
        # If dying, only update the animation
        if self.dying:
            self.update_death_animation()
            self.update_main_animation()  # Continue updating the main animation
            return
            
        if self.frozen:
            self.update_main_animation()
            self.update_freeze_animation()
            return
        
        # Record the position before moving
        old_position = (self.rect.x, self.rect.y)
            
        # Update path to target
        self.update_path(target)
        
        # Move along path
        if not self.move_along_path():
            # If enemy can't follow the path, try tracing it directly.
            self.direct_chase(target)
        
        # Update heading (based on actual movement)
        self.update_facing_direction(old_position)
        
        # Update animation
        self.update_main_animation()
        
        # Update attack animation if attacking (but not dying)
        if self.attacking and not self.dying:
            self.update_attack_animation()

    def update_freeze_animation(self):
        """Updated freezing animations"""
        if not self.freeze_frames:
            return
            
        now = pygame.time.get_ticks()
        if now - self.freeze_animation_timer > self.freeze_animation_speed:
            self.freeze_animation_timer = now
            self.freeze_current_frame = (self.freeze_current_frame + 1) % len(self.freeze_frames)

    def update_facing_direction(self, old_position):
        """Update enemy direction"""
        current_position = (self.rect.x, self.rect.y)
        dx = current_position[0] - old_position[0]
        
        # Update heading only when moving horizontally
        if abs(dx) > 0:
            self.facing_right = not dx > 0

    def update_death_animation(self):
        """Updated death animation"""
        now = pygame.time.get_ticks()
        
        if len(self.attack_frames) > 0 and now - self.attack_animation_timer > self.attack_animation_speed:
            self.attack_animation_timer = now
            self.attack_current_frame += 1
            
            # If the animation is finished playing, mark it as completed
            if self.attack_current_frame >= len(self.attack_frames):
                self.death_animation_complete = True
                self.attack_current_frame = len(self.attack_frames) - 1  # Keep in last frame

    def update_main_animation(self):
        """Updated main animations (enemy movement animations)"""
        now = pygame.time.get_ticks()
        
        # Update the main animation only when it is not in the death state or the death animation has not yet completed
        if not self.dying or not self.death_animation_complete:
            if now - self.animation_timer > self.animation_speed:
                self.animation_timer = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            
            # Set the main image
            base_image = self.frames[self.current_frame]
            self.image = base_image if self.facing_right else pygame.transform.flip(base_image, True, False)

    def update_attack_animation(self):
        """Updated attack animations (attacks in non-death states)"""
        now = pygame.time.get_ticks()
        
        if len(self.attack_frames) > 0 and now - self.attack_animation_timer > self.attack_animation_speed:
            self.attack_animation_timer = now
            self.attack_current_frame = (self.attack_current_frame + 1) % len(self.attack_frames)

    def update_path(self, target):
        """Update pathfinding to target"""
        current_time = pygame.time.get_ticks()
        
        # Use the player's grid position as the target, ensuring it is traversable
        target_grid_pos = target.get_grid_position()
        target_pos = find_nearest_walkable_position(target_grid_pos)
        
        # Only recalculate path if target moved significantly or enough time has passed
        if (self.last_target_pos is None or 
            abs(target_pos[0] - self.last_target_pos[0]) > constants.TILE_SIZE or
            abs(target_pos[1] - self.last_target_pos[1]) > constants.TILE_SIZE or
            current_time - self.path_update_timer > self.path_update_interval or
            not self.path or
            self.stuck_counter > self.max_stuck_count):
            
            start_pos = (self.rect.x, self.rect.y)
            self.path = a_star(start_pos, target_pos)
            self.path_index = 0
            self.last_target_pos = target_pos
            self.path_update_timer = current_time
            
            if self.path:
                self.stuck_counter = 0
                self.direct_chase_mode = False
            else:
                self.stuck_counter += 1
                if self.stuck_counter > self.max_stuck_count:
                    self.direct_chase_mode = True

    def move_along_path(self):
        """Move enemy along calculated path"""
        if not self.path or self.path_index >= len(self.path):
            return False
            
        target_pos = self.path[self.path_index]
        
        # Ensure target_pos is a tuple with two elements
        if not isinstance(target_pos, (tuple, list)) or len(target_pos) != 2:
            print(f"Warning: Invalid target_pos: {target_pos}")
            return False
            
        target_x, target_y = target_pos[0], target_pos[1]
        old_pos = (self.rect.x, self.rect.y)
        
        # Calculate direction
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        
        # Move towards target
        if abs(dx) > self.speed:
            self.rect.x += self.speed if dx > 0 else -self.speed
        else:
            self.rect.x = target_x
            
        if abs(dy) > self.speed:
            self.rect.y += self.speed if dy > 0 else -self.speed
        else:
            self.rect.y = target_y
            
        # Check if reached current path point
        if abs(self.rect.x - target_x) <= self.speed and abs(self.rect.y - target_y) <= self.speed:
            self.path_index += 1
        
        # Check if it moves (to avoid getting stuck)
        if old_pos == (self.rect.x, self.rect.y):
            self.stuck_counter += 1
        else:
            self.stuck_counter = max(0, self.stuck_counter - 1)
            
        return True

    def direct_chase(self, target):
        """Move directly towards the player (fallback if pathfinding fails)）"""
        target_center = target.get_center_position()
        enemy_center = (self.rect.centerx, self.rect.centery)
        
        # Calculation direction
        dx = target_center[0] - enemy_center[0]
        dy = target_center[1] - enemy_center[1]
        
        # Normalization direction
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            
            # Try to move
            new_x = self.rect.x + dx
            new_y = self.rect.y + dy
            
            # Simple wall detection
            test_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)
            collision = False
            for wall in walls:
                if test_rect.colliderect(wall):
                    collision = True
                    break
            
            if not collision:
                self.rect.x = new_x
                self.rect.y = new_y

    def start_attack(self):
        """Start attack animation"""
        if not self.dying:  # Can only attack when not dead
            self.attacking = True
            self.attack_current_frame = 0
            self.attack_animation_timer = pygame.time.get_ticks()  # Reset Timer
            print(f"Enemy started attack animation, frames available: {len(self.attack_frames)}")  # For Debugging

    def draw(self, surface):
        """Draw enemy with attack effects"""
        # Draw attack effects (if attacking and there is an attack frame)
        if self.attacking and len(self.attack_frames) > 0:
            # Attack effects based on direction flip
            attack_image = self.attack_frames[self.attack_current_frame]
            flipped_attack = attack_image if self.facing_right else pygame.transform.flip(attack_image, True, False)
            surface.blit(flipped_attack, self.rect)
        
        # Draws a freeze effect (if frozen and has a freeze frame)
        if self.frozen and len(self.freeze_frames) > 0:
            freeze_image = self.freeze_frames[self.freeze_current_frame]
            surface.blit(freeze_image, self.rect)

class Item(pygame.sprite.Sprite):
    def __init__(self, image, pos, item_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.type = item_type

class Key(pygame.sprite.Sprite):
    def __init__(self, images, pos):
        super().__init__()
        self.images = images
        self.current_frame = 0
        self.image = self.images[self.current_frame] if images else pygame.Surface((40, 40))
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_timer = 0
        self.animation_speed = 200

    def update(self):
        """Update key animation"""
        if not self.images:
            return
            
        now = pygame.time.get_ticks()
        if now - self.animation_timer > self.animation_speed:
            self.animation_timer = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]