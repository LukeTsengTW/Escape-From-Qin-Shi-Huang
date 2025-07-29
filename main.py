"""
Game Name : Escape from Qin Shi Huang
Author : LukeTseng
Programming Language : Python
"""

import pygame
import constants

# === initial Pygame ===
pygame.init()
icon = pygame.image.load("assets/icon.ico")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("逃離秦始皇 ( Escape from Qin Shi Huang )")
clock = pygame.time.Clock()

from assets import load_images

# Load images after display is initialized
load_images()

# Import menu_functions after everything is set up
from menu_functions import show_menu

# Set global variables for other modules to access
import menu_functions
import menu_system
import renderer
import game_logic

# Pass screen and clock to modules that need them
menu_functions.screen = screen
menu_functions.clock = clock
menu_system.screen = screen
renderer.screen = screen
game_logic.screen = screen
game_logic.clock = clock

show_menu()