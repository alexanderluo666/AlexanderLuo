import os
import pygame


def _project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def set_window_icon_from_frame(dino_frame):
    """Use a scaled dino frame as the OS window icon (replaces default pygame dragon)."""
    icon = pygame.transform.smoothscale(dino_frame, (32, 32))
    pygame.display.set_icon(icon)


def grid_chebyshev(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def player_grid_cell(rect, tile_size):
    return rect.centerx // tile_size, rect.centery // tile_size


def cursor_grid_cell(mouse_pos, tile_size):
    mx, my = mouse_pos
    return mx // tile_size, my // tile_size


def is_in_reach(player_rect, mouse_pos, tile_size, reach_blocks):
    pg = player_grid_cell(player_rect, tile_size)
    cg = cursor_grid_cell(mouse_pos, tile_size)
    return grid_chebyshev(pg, cg) <= reach_blocks