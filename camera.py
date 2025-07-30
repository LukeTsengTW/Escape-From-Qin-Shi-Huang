import pygame
import constants

class Camera:
    """Camera system to follow the player and handle field of view offsets"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        
    def update(self, target):
        """Update the camera position to follow the target (usually the player)"""
        # Center the lens on the target
        self.x = target.rect.centerx - self.width // 2
        self.y = target.rect.centery - self.height // 2
        
        # Make sure the camera doesn't go outside the maze boundaries (if necessary)
        # Here you can limit the size of the maze
        # self.x = max(0, min(self.x, maze_width - self.width))
        # self.y = max(0, min(self.y, maze_height - self.height))
        
    def apply(self, rect):
        """Convert world coordinates to screen coordinates"""
        return pygame.Rect(rect.x - self.x, rect.y - self.y, rect.width, rect.height)
    
    def apply_pos(self, pos):
        """Convert world position to screen position"""
        return (pos[0] - self.x, pos[1] - self.y)
    
    def world_to_screen(self, world_pos):
        """Convert world coordinates to screen coordinates"""
        return (world_pos[0] - self.x, world_pos[1] - self.y)
    
    def screen_to_world(self, screen_pos):
        """Convert screen coordinates to world coordinates"""
        return (screen_pos[0] + self.x, screen_pos[1] + self.y)
    
    def get_visible_area(self):
        """Get the world coordinate range of the visible area"""
        return pygame.Rect(self.x, self.y, self.width, self.height)