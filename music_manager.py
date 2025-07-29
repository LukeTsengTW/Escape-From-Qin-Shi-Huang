import pygame
from assets import menu_music_path, playing_music_path, victory_music_path, gameover_music_path

class MusicManager:
    """Music Manager, ensuring music is switched only when needed"""
    def __init__(self):
        self.current_music = None
        self.music_files = {
            "menu": menu_music_path,
            "game": playing_music_path,
            "victory": victory_music_path,
            "gameover": gameover_music_path
        }
    
    def play_music(self, music_type, force_restart=False):
        """Play music of a specified type and switch only when the music type changes"""
        if self.current_music != music_type or force_restart:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music_files[music_type])
            pygame.mixer.music.play(-1)
            self.current_music = music_type
            print(f"Music switched to: {music_type}")
    
    def is_playing(self, music_type):
        """Check if music of a specific type is playing"""
        return self.current_music == music_type

music_manager = MusicManager()

def setup_menu_music():
    music_manager.play_music("menu")

def setup_game_music():
    music_manager.play_music("game")