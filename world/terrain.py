import pygame
import random as r
from utils.game_state import GameState

state = GameState()

def create_block(color):
    surface = pygame.Surface((state.TILE_SIZE, state.TILE_SIZE))
    surface.fill(color)

    # add pixel noise (makes it look less flat)
    for _ in range(60):
        x = r.randint(0, state.TILE_SIZE - 1)
        y = r.randint(0, state.TILE_SIZE - 1)

        shade = (
            max(0, min(255, color[0] + r.randint(-20, 20))),
            max(0, min(255, color[1] + r.randint(-20, 20))),
            max(0, min(255, color[2] + r.randint(-20, 20)))
        )

        surface.set_at((x, y), shade)

    return surface



class Worldgen:
    def __init__(self):

        self.x, self.y = r.randint(70,90), r.randint(110,140)
        

        self.block_images = {
            "grass": create_block((self.x, self.x + self.y, self.y)),
            "dirt": create_block((self.y, self.x, self.x // 2)),
            "stone": create_block((self.y, self.y, self.y)),
            "sand": create_block((self.x+self.y+20, self.x+self.y, self.y+self.x//2)), 
            "wood": create_block((self.y, self.x, self.x // 4)),   
        }
        

        self.world = {}


        self.block_types = ["dirt", "grass", "stone" , "sand" , "wood"]


        self.random_block_type = r.choice(self.block_types)

        
        for x in range(25):
            for y in range(-15, -20, -1):
                self.world[(x, -y)] = self.random_block_type
        self.selected_block = "grass"

