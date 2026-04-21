import pygame
class GameState:
    def __init__(self):
        self.world = {}
        self.player_x = 100
        self.player_y = 100
        self.selected_block = "grass"
        self.WIDTH, self.HEIGHT = 800, 600
        self.TILE_SIZE = 32
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
