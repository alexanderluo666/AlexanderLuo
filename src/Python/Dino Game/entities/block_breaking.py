import pygame
from utils.reach import cursor_grid_cell, player_grid_cell, grid_chebyshev


class BlockBreaker:
    def __init__(self, break_duration_ms=500.0):
        self.target = None
        self.timer = 0.0
        self.break_duration = break_duration_ms

    def update(self, dt, mouse_buttons, player_rect, world, st):
        if not mouse_buttons[0]:
            self.target = None
            self.timer = 0.0
            return False

        target_tile = cursor_grid_cell(pygame.mouse.get_pos(), st.TILE_SIZE)
        player_tile = player_grid_cell(player_rect, st.TILE_SIZE)

        if grid_chebyshev(player_tile, target_tile) > st.REACH_BLOCKS:
            self.target = None
            self.timer = 0.0
            return False

        if target_tile not in world:
            self.target = None
            self.timer = 0.0
            return False

        if self.target != target_tile:
            self.target = target_tile
            self.timer = 0.0

        self.timer += dt
        if self.timer >= self.break_duration:
            del world[target_tile]
            self.target = None
            self.timer = 0.0
            return True

        return False

    def progress(self):
        if not self.target:
            return 0.0
        return min(self.timer / self.break_duration, 1.0)
