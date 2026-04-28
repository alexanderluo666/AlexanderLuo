class Settings:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 60
        self.TILE_SIZE = 32

        # Horizontal move (pixels per second)
        self.PLAYER_SPEED = 260.0

        # Gravity: downward acceleration (pixels per second²)
        self.GRAVITY = 2200.0

        # Initial upward speed when jumping (pixels per second, negative = up)
        self.JUMP_VELOCITY = -560.0

        # Scale raw sprite pixels (Dino frames are 24×24 before scale)
        self.PLAYER_SPRITE_SCALE = 2.25

        # Build / break blocks only when cursor tile is within this Chebyshev distance (tiles)
        self.REACH_BLOCKS = 3