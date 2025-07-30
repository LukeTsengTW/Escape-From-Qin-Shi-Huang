import pygame
import sys
import webbrowser
import constants
from assets import *
from translations import translations, current_language
from config import save_config, load_config

config = load_config()

# Global variable to be set by main.py
screen = None

def get_music_functions():
    """Delayed import of music management functions"""
    from music_manager import setup_menu_music
    return setup_menu_music

def get_menu_functions():
    """Delay import of menu functions to avoid circular dependencies"""
    from menu_functions import show_language_selection, show_difficulty, show_settings, show_sound_setting, show_resolution_selection
    return show_language_selection, show_difficulty, show_settings, show_sound_setting, show_resolution_selection

def draw_text_center(text, font, color, surface, y):
    if font is None:
        raise RuntimeError("Font not initialized")
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(constants.WIDTH // 2, y))
    surface.blit(text_surface, text_rect)
    return text_rect  # Returns position to detect mouse collision

class MenuButton:
    """Menu button class for better organization"""
    def __init__(self, text, y_pos, action):
        self.text = text
        self.y_pos = y_pos
        self.action = action
        self.rect = pygame.Rect(constants.WIDTH // 2 - 100, y_pos - 20, 200, 40)
    
    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface, font, mouse_pos):
        color = constants.RED if self.is_hovered(mouse_pos) else constants.GRAY
        return draw_text_center(self.text, font, color, surface, self.y_pos)

class MenuOption:
    """Menu option class for unified menu handling"""
    def __init__(self, text, action, data=None):
        self.text = text
        self.action = action
        self.data = data

class BaseMenuHandler:
    """Base class for handling menu screens"""
    def __init__(self, title, options, background_color=constants.WHITE):
        self.title = title
        self.options = options
        self.background_color = background_color
        self.running = True
        self.font = font
        self.title_font = pygame.font.Font("assets/Cubic_11.ttf", 36)
        
        if screen is None:
            raise RuntimeError("Screen not initialized")
        
    def draw_background(self):
        """Draw the background and title"""
        screen.fill(self.background_color)
        if self.title:
            draw_text_center(self.title, self.title_font, constants.BLACK if self.background_color == constants.WHITE else constants.WHITE, screen, constants.HEIGHT // 4)
    
    def draw_options(self, mouse_pos):
        """Draw all options and return their rects"""
        option_rects = []
        start_y = constants.HEIGHT // 2 if not hasattr(self, 'start_y') else self.start_y
        
        for i, option in enumerate(self.options):
            y_pos = start_y + i * 50
            color = constants.RED if pygame.Rect(constants.WIDTH // 2 - 100, y_pos - 25, 200, 50).collidepoint(mouse_pos) else (constants.GRAY if self.background_color == constants.WHITE else constants.WHITE)
            rect = draw_text_center(option.text, self.font, color, screen, y_pos)
            option_rects.append((option, rect))
        
        return option_rects
    
    def handle_click(self, option):
        """Handle option click - override in subclasses"""
        menu_click_sound.play()
        if option.action == "back":
            self.running = False
            return None
        return option.action
    
    def run(self):
        global config
        """Main menu loop"""
        while self.running:
            self.draw_background()
            mouse_pos = pygame.mouse.get_pos()
            option_rects = self.draw_options(mouse_pos)
            
            # Additional drawing can be overridden
            self.additional_drawing()
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_config(config)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.handle_mouse_click(event.pos, option_rects)
                    if result:
                        return result
        return None
    
    def handle_mouse_click(self, pos, option_rects):
        """Handle mouse click on options"""
        for option, rect in option_rects:
            if rect.collidepoint(pos):
                return self.handle_click(option)
        return None
    
    def additional_drawing(self):
        """Override for additional drawing"""
        pass

class FullscreenMenuHandler:
    """Fullscreen toggle handler"""
    
    def __init__(self):
        self.config = load_config()
        self.screen = screen
        
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        # Toggle full screen mode
        self.config["fullscreen"] = not self.config["fullscreen"]
        save_config(self.config)
        
        # Apply a new display mode
        try:
            if self.config["fullscreen"]:
                # Switch to full screen mode
                pygame.display.set_mode((self.config["resolution_width"], self.config["resolution_height"]), pygame.FULLSCREEN)
            else:
                # Switch to windowed mode
                pygame.display.set_mode((self.config["resolution_width"], self.config["resolution_height"]))
            
            return True
        except pygame.error as e:
            print(f"Failed to toggle fullscreen: {e}")
            # If it fails, restore the original settings
            self.config["fullscreen"] = not self.config["fullscreen"]
            save_config(self.config)
            return False
    
    def get_current_mode_text(self):
        """Get text for current display mode option"""
        if self.config["fullscreen"]:
            return translations[current_language]["switch_to_windowed"]
        else:
            return translations[current_language]["switch_to_fullscreen"]

class SettingsMenuHandler(BaseMenuHandler):
    """Handler for settings menu"""
    
    def __init__(self, title, options):
        super().__init__(title, options)
        self.fullscreen_handler = FullscreenMenuHandler()
    
    def get_dynamic_options(self):
        """Get options with dynamic text for fullscreen toggle"""
        return [
            MenuOption(translations[current_language]["language"], "language"),
            MenuOption(translations[current_language]["sound"], "sound"),
            MenuOption(translations[current_language]["difficulty"], "difficulty"),
            MenuOption(translations[current_language]["resolution"], "resolution"),
            MenuOption(self.fullscreen_handler.get_current_mode_text(), "fullscreen"),
            MenuOption(translations[current_language]["back"], "back")
        ]
    
    def get_option_rect(self, i):
        """Get the rect for a specific option"""
        start_y = constants.HEIGHT // 2 if not hasattr(self, 'start_y') else self.start_y
        y_pos = start_y + i * 50
        return pygame.Rect(constants.WIDTH // 2 - 100, y_pos - 25, 200, 50)
    
    def run(self):
        """Override run method to use dynamic options"""
        global config
        self.running = True
        
        while self.running:
            # Update options to reflect current status
            self.options = self.get_dynamic_options()
            
            # Draw the background and title
            self.draw_background()
            
            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Drawing Options
            option_rects = self.draw_options(mouse_pos)
            
            # Additional drawing
            self.additional_drawing()
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_config(config)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for option, rect in option_rects:
                        if rect.collidepoint(event.pos):
                            result = self.handle_click(option)
                            if result:
                                return result
                            break
        return None
    
    def handle_click(self, option):
        """Handle settings menu selection with fullscreen support"""
        menu_click_sound.play()
        if option.action == "back":
            self.running = False
        elif option.action == "language":
            show_language_selection, show_difficulty, show_settings, show_sound_setting, show_resolution_selection = get_menu_functions()
            show_language_selection()
        elif option.action == "difficulty":
            show_language_selection, show_difficulty, show_settings, show_sound_setting, show_resolution_selection = get_menu_functions()
            show_difficulty()
        elif option.action == "sound":
            show_language_selection, show_difficulty, show_settings, show_sound_setting, show_resolution_selection = get_menu_functions()
            show_sound_setting()
        elif option.action == "resolution":
            show_language_selection, show_difficulty, show_settings, show_sound_setting, show_resolution_selection = get_menu_functions()
            show_resolution_selection()
        elif option.action == "fullscreen":
            if self.fullscreen_handler.toggle_fullscreen():
                import menu_functions
                import renderer
                import game_logic
                new_screen = pygame.display.get_surface()
                menu_functions.screen = new_screen
                renderer.screen = new_screen
                game_logic.screen = new_screen
            else:
                print("Failed to toggle fullscreen mode")
        return None

class LanguageMenuHandler(BaseMenuHandler):
    """Handler for language selection menu"""
    def __init__(self, title, options, background_color=constants.WHITE):
        super().__init__(title, options, background_color)
        self.start_y = constants.HEIGHT // 2 + 40
    
    def additional_drawing(self):
        """Draw language selection note"""
        note_text = translations[current_language]["select_language_note"]
        draw_text_center(note_text, self.font, constants.GRAY, screen, constants.HEIGHT // 4 + 50)
    
    def handle_click(self, option):
        global current_language, config
        menu_click_sound.play()
        if option.action == "back":
            self.running = False
        else:
            current_language = option.action
            config["current_language"] = current_language
            save_config(config)

class DifficultyMenuHandler(BaseMenuHandler):
    """Handler for difficulty selection menu"""
    def __init__(self, title, options, background_color=constants.WHITE):
        super().__init__(title, options, background_color)
        self.start_y = constants.HEIGHT // 2 + 50
    
    def additional_drawing(self):
        """Draw current difficulty"""
        current_text = f"{translations[current_language]['now_difficulty']} {translations[current_language][constants.DIFFICULTY]}"
        draw_text_center(current_text, self.font, constants.BLACK, screen, constants.HEIGHT // 4 + 50)
    
    def handle_click(self, option):
        menu_click_sound.play()
        if option.action == "back":
            self.running = False
        else:
            constants.DIFFICULTY = option.action
            config["DIFFICULTY"] = constants.DIFFICULTY
            save_config(config)

class PauseMenuHandler(BaseMenuHandler):
    """Handler for pause menu"""
    def __init__(self, title, options, background_color=constants.WHITE):
        super().__init__(title, options, background_color)
    
    def handle_click(self, option):
        menu_click_sound.play()
        if option.action == "resume":
            self.running = False
            return "resume"
        elif option.action == "setting":
            show_language_selection, show_difficulty, show_settings, show_sound_setting, show_resolution_selection = get_menu_functions()
            show_settings()
        elif option.action == "back_menu":
            self.running = False
            return "main_menu"

class GameOverMenuHandler(BaseMenuHandler):
    """Handler for game over screen"""
    def __init__(self):
        title = translations[current_language]["gameover"]
        options = [MenuOption(translations[current_language]["back_menu"], "back_menu")]
        super().__init__(title, options, constants.BLACK)
        
        def get_music_manager():
            from music_manager import music_manager
            return music_manager
        
        music_manager = get_music_manager()
        music_manager.play_music("gameover")
    
    def draw_background(self):
        """Custom background for game over"""
        screen.fill(constants.BLACK)
        draw_text_center(self.title, self.title_font, constants.RED, screen, constants.HEIGHT // 3)
    
    def handle_click(self, option):
        """Handle game over menu clicks"""
        menu_click_sound.play()
        if option.action == "back_menu":
            self.running = False
            setup_menu_music = get_music_functions()
            setup_menu_music()
            return "back_menu"
        return None

class VictoryMenuHandler(BaseMenuHandler):
    """Handler for victory screen"""
    def __init__(self):
        title = translations[current_language]["pass"]
        options = [MenuOption(translations[current_language]["back_menu"], "back_menu")]
        super().__init__(title, options, constants.WHITE)
        
        def get_music_manager():
            from music_manager import music_manager
            return music_manager
        
        music_manager = get_music_manager()
        music_manager.play_music("victory")
    
    def draw_background(self):
        """Custom background for victory"""
        screen.fill(constants.WHITE)
        draw_text_center(self.title, self.title_font, constants.GREEN, screen, constants.HEIGHT // 3)
    
    def handle_click(self, option):
        """Handle victory menu clicks"""
        menu_click_sound.play()
        if option.action == "back_menu":
            self.running = False
            setup_menu_music = get_music_functions()
            setup_menu_music()
            return "back_menu"
        return None

class HowToPlayMenuHandler(BaseMenuHandler):
    """Handler for how to play screen"""
    def __init__(self):
        title = translations[current_language]["how_to_play"]
        options = [MenuOption(translations[current_language]["back"], "back")]
        super().__init__(title, options, constants.GRAY)
        self.start_y = constants.HEIGHT // 2 + 180
    
    def additional_drawing(self):
        """Draw how to play instructions"""
        instructions = [
            translations[current_language]["htp_line1"],
            translations[current_language]["htp_line2"],
            translations[current_language]["htp_line3"],
            translations[current_language]["htp_line4"]
        ]
        
        for i, instruction in enumerate(instructions):
            draw_text_center(instruction, self.font, constants.WHITE, screen, constants.HEIGHT // 4 + 60 + i * 50)
        
        item_y_pos = constants.HEIGHT // 4 + 280
        screen.blit(item_images['red'], (constants.WIDTH // 2 - 20, item_y_pos))
        screen.blit(item_images['blue'], (constants.WIDTH // 2 - 80, item_y_pos))
        screen.blit(item_images['yellow'], (constants.WIDTH // 2 + 40, item_y_pos))

class SoundSettingHandler:
    """Handler for sound settings with sliders"""
    
    def __init__(self):
        self.running = True
        self.dragging_slider = None
        self.slider_width = 300
        self.slider_height = 20
        self.slider_x = constants.WIDTH // 2 - self.slider_width // 2
        self.start_y = constants.HEIGHT // 3
        self.gap_y = 70
        
        if screen is None:
            raise RuntimeError("Screen not initialized")
    
    def get_volume_items(self):
        """Get current volume settings"""
        return [
            (translations[current_language]["master_volume"], master_volume, "master"),
            (translations[current_language]["bgm"], music_volume, "music"),
            (translations[current_language]["se"], sfx_volume, "sfx"),
        ]
    
    def draw_slider(self, label, volume, y_pos, mouse_pos):
        """Draw a single volume slider"""
        # Draw label
        draw_text_center(label, font, constants.BLACK, screen, y_pos - 15)
        
        # Calculate slider position
        bar_rect = pygame.Rect(self.slider_x, y_pos, self.slider_width, self.slider_height)
        knob_x = self.slider_x + int(volume * self.slider_width)
        knob_rect = pygame.Rect(knob_x - 10, y_pos - 5, 20, self.slider_height + 10)
        
        # Draw slider components
        pygame.draw.rect(screen, constants.GRAY, bar_rect)
        pygame.draw.rect(screen, constants.RED, (self.slider_x, y_pos, knob_x - self.slider_x, self.slider_height))
        
        knob_color = constants.RED if knob_rect.collidepoint(mouse_pos) or self.dragging_slider == label else constants.BLACK
        pygame.draw.rect(screen, knob_color, knob_rect)
        
        # Draw volume percentage
        vol_percent = int(volume * 100)
        vol_text = font.render(f"{vol_percent}%", True, constants.BLACK)
        screen.blit(vol_text, (self.slider_x + self.slider_width + 20, y_pos - font.get_height() // 2))
        
        return bar_rect, knob_rect
    
    def update_volume(self, volume_type, new_vol):
        """Update volume setting"""
        global master_volume, music_volume, sfx_volume, config
        
        if volume_type == "master":
            master_volume = new_vol
            config["master_volume"] = master_volume
        elif volume_type == "music":
            music_volume = new_vol
            config["music_volume"] = music_volume
        elif volume_type == "sfx":
            sfx_volume = new_vol
            config["sfx_volume"] = sfx_volume
        
        # Apply volume changes
        pygame.mixer.music.set_volume(music_volume * master_volume)
        for sound in [menu_click_sound, door_open_sound, hit_sound, sword_sound, freeze_sound, pickUp_sound]:
            sound.set_volume(sfx_volume * master_volume)
    
    def run(self):
        global config
        """Main sound settings loop"""
        while self.running:
            screen.fill(constants.WHITE)
            draw_text_center(translations[current_language]["sound"], font, constants.BLACK, screen, constants.HEIGHT // 6)
            
            mouse_pos = pygame.mouse.get_pos()
            volume_items = self.get_volume_items()
            slider_rects = []
            
            # Draw all sliders
            for i, (label, vol, vol_type) in enumerate(volume_items):
                y_pos = self.start_y + i * self.gap_y
                bar_rect, knob_rect = self.draw_slider(label, vol, y_pos, mouse_pos)
                slider_rects.append((label, vol_type, bar_rect, knob_rect))
            
            # Draw back button
            back_color = constants.RED if pygame.Rect(constants.WIDTH // 2 - 100, constants.HEIGHT - 80, 200, 50).collidepoint(mouse_pos) else constants.GRAY
            back_rect = draw_text_center(translations[current_language]["back"], font, back_color, screen, constants.HEIGHT - 60)
            
            pygame.display.flip()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config = load_config()
                    save_config(config)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        menu_click_sound.play()
                        self.running = False
                    else:
                        # Check slider clicks
                        for label, vol_type, bar_rect, knob_rect in slider_rects:
                            if knob_rect.collidepoint(event.pos) or bar_rect.collidepoint(event.pos):
                                self.dragging_slider = label
                                break
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging_slider = None
                    save_config(config)
            
            # Handle slider dragging
            if self.dragging_slider:
                for label, vol_type, bar_rect, knob_rect in slider_rects:
                    if label == self.dragging_slider:
                        relative_x = mouse_pos[0] - bar_rect.left
                        new_vol = max(0, min(1, relative_x / self.slider_width))
                        self.update_volume(vol_type, new_vol)
                        break

class ResolutionMenuHandler(BaseMenuHandler):
    """Resolution setting menu handler"""
    
    def __init__(self, title, options):
        super().__init__(title, options)
        self.config = load_config()
        self.screen = screen
        
    def handle_click(self, option):
        """Handle resolution selection"""
        menu_click_sound.play()
        if option.action == "back":
            self.running = False
            return None
        
        # Parsing resolution string
        if "x" in option.action:
            try:
                width, height = map(int, option.action.split("x"))
                self.config["resolution_width"] = width
                self.config["resolution_height"] = height
                save_config(self.config)
                
                # Display a reboot prompt
                self.show_restart_message()
                self.running = False
                return None
            except ValueError:
                print(f"Invalid resolution format: {option.action}")
        
        return None
    
    def show_restart_message(self):
        """Show restart required message"""
        if screen is None:
            return
            
        # Create a semi-transparent overlay
        overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(constants.BLACK)
        screen.blit(overlay, (0, 0))
        
        # Display message
        message = translations[current_language]["resolution_restart_note"]
        text_surface = self.font.render(message, True, constants.WHITE)
        text_rect = text_surface.get_rect(center=(constants.WIDTH//2, constants.HEIGHT//2))
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        pygame.time.wait(2000)
    
    def additional_drawing(self):
        """Override to show current resolution"""
        # Display current resolution
        current_res = f"{self.config['resolution_width']}x{self.config['resolution_height']}"
        current_text = f"{translations[current_language]['current_resolution']} {current_res}"
        text_surface = self.font.render(current_text, True, constants.BLACK)
        text_rect = text_surface.get_rect(center=(constants.WIDTH//2, constants.HEIGHT//4 + 60))
        screen.blit(text_surface, text_rect)

