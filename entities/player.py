import os
import pygame
from utils.spritesheet import SpriteSheet
from entities.block_breaking import BlockBreaker


def _dino_path():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "assets", "images", "DinoSprites - doux.png")


class Player(pygame.sprite.Sprite):
    """
    DinoSprites — doux: 24 frames in one row (idle 0–3, run 4–9, jump 17–23).
    Art faces right; flip when moving left.
    """

    DINO_FRAME_COUNT = 24

    def __init__(self, settings, pos=(100, 400)):
        super().__init__()
        self.st = settings

        sheet = SpriteSheet(_dino_path())
        sw, sh = sheet.sheet.get_size()
        scaled = pygame.transform.scale(
            sheet.sheet,
            (
                max(1, int(sw * settings.PLAYER_SPRITE_SCALE)),
                max(1, int(sh * settings.PLAYER_SPRITE_SCALE)),
            ),
        )
        frames = SpriteSheet.split_horizontal_strip(scaled, self.DINO_FRAME_COUNT)

        # Idle: use first frame only — full idle 0–3 includes blink and reads as "flashing"
        # Scale player to 1 tile for one-block tunnel fit
        target_size = (int(settings.TILE_SIZE), int(settings.TILE_SIZE))
        self.idle_frames = [pygame.transform.smoothscale(frames[0], target_size)]
        self.run_frames = [pygame.transform.smoothscale(f, target_size) for f in frames[4:10]]
        self.jump_frames = [pygame.transform.smoothscale(f, target_size) for f in frames[17:24]]

        self.facing_right = True
        self.image = self.idle_frames[0]
        self.rect = pygame.Rect(pos[0], pos[1], settings.TILE_SIZE, settings.TILE_SIZE)

        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.vy = 0.0

        self.anim_state = "idle"
        self.prev_anim_state = "idle"
        self.frame_index = 0
        self.timer = 0.0
        self.frame_ms_idle = 200.0
        self.frame_ms_run = 95.0
        self.frame_ms_jump = 75.0

        self.on_ground = False
        self._frames_off_ground = 0

        # Block breaking system
        self.breaker = BlockBreaker(500.0)  # milliseconds to break one block

    def _sync_rect(self):
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

    def _iter_tile_rects(self, world, tile_size):
        for gx, gy in world:
            yield pygame.Rect(gx * tile_size, gy * tile_size, tile_size, tile_size)

    def _resolve_x(self, world, tile_size, screen_w):
        for tile in self._iter_tile_rects(world, tile_size):
            if not self.rect.colliderect(tile):
                continue
            if self.rect.centerx < tile.centerx:
                self.rect.right = tile.left
            else:
                self.rect.left = tile.right
        self.pos_x = float(self.rect.x)
        self.rect.x = max(0, min(int(self.pos_x), screen_w - self.rect.width))
        self.pos_x = float(self.rect.x)

    def _get_break_target_pos(self, st):
        # break the tile in front of the player
        gx = (self.rect.centerx // st.TILE_SIZE) + (1 if self.facing_right else -1)
        gy = self.rect.centery // st.TILE_SIZE
        return (gx, gy)

    def _pos_in_reach(self, target, st):
        px = self.rect.centerx // st.TILE_SIZE
        py = self.rect.centery // st.TILE_SIZE
        return max(abs(target[0] - px), abs(target[1] - py)) <= st.REACH_BLOCKS

    def _break_block(self, world, tile_pos):
        if tile_pos in world:
            del world[tile_pos]
            self.break_target = None
            self.break_timer = 0.0

    def _feet_support(self, world, tile_size, screen_h):
        """True if feet rest on the floor or the top of a block (edge-touch counts)."""
        r = self.rect
        if r.bottom >= screen_h:
            return True
        tol = 3
        for t in self._iter_tile_rects(world, tile_size):
            if r.right <= t.left or r.left >= t.right:
                continue
            if abs(r.bottom - t.top) <= tol:
                return True
        return False

    def _resolve_y(self, world, tile_size, screen_h):
        self.on_ground = False
        colliding = [
            t
            for t in self._iter_tile_rects(world, tile_size)
            if self.rect.colliderect(t)
        ]

        if self.vy > 0 and colliding:
            tops = [t.top for t in colliding if self.rect.bottom > t.top]
            if tops:
                land = min(tops)
                self.rect.bottom = land
                self.pos_y = float(self.rect.y)
                self.vy = 0.0
                self.on_ground = True
        elif self.vy < 0 and colliding:
            bottoms = [t.bottom for t in colliding if self.rect.top < t.bottom]
            if bottoms:
                self.rect.top = max(bottoms)
                self.pos_y = float(self.rect.y)
                self.vy = 0.0

                # Attempt to break a directly-hit tile from below
                for t in colliding:
                    gx = t.left // tile_size
                    gy = t.top // tile_size
                    if (gx, gy) in world:
                        self._break_block(world, (gx, gy))
                        break

        if self.rect.bottom >= screen_h:
            self.rect.bottom = screen_h
            self.pos_y = float(self.rect.y)
            self.vy = 0.0
            self.on_ground = True

        if self.vy == 0 and not self.on_ground:
            self.on_ground = self._feet_support(world, tile_size, screen_h)

        if self.on_ground and abs(self.vy) < 40:
            self.vy = 0.0
            self._snap_feet_to_ground(world, tile_size, screen_h)

        self.pos_y = float(self.rect.y)

    def _snap_feet_to_ground(self, world, tile_size, screen_h):
        """Align feet to tile tops when resting to stop 1px jitter toggling ground checks."""
        r = self.rect
        if r.bottom >= screen_h:
            return
        tops = []
        for t in self._iter_tile_rects(world, tile_size):
            if r.right <= t.left or r.left >= t.right:
                continue
            if abs(r.bottom - t.top) <= 6:
                tops.append(t.top)
        if tops:
            land = min(tops)
            if r.bottom != land:
                r.bottom = land
                self.pos_y = float(r.y)

    def update(self, dt, keys, world):
        st = self.st
        dt_s = max(dt / 1000.0, 1e-6)

        speed = st.PLAYER_SPEED * dt_s
        dx = 0.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = speed
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -speed
            self.facing_right = False

        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
        if jump_pressed and self.on_ground:
            self.vy = st.JUMP_VELOCITY
            self.on_ground = False
            self._frames_off_ground = 2
            self.frame_index = 0
            self.timer = 0.0

        self.pos_x += dx
        self._sync_rect()
        self._resolve_x(world, st.TILE_SIZE, st.WIDTH)

        self.vy += st.GRAVITY * dt_s
        self.pos_y += self.vy * dt_s
        self._sync_rect()
        self._resolve_y(world, st.TILE_SIZE, st.HEIGHT)

        if self.on_ground:
            self._frames_off_ground = 0
        else:
            self._frames_off_ground = min(self._frames_off_ground + 1, 30)

        # Always break with left mouse hold (target under cursor when in reach)
        mouse_buttons = pygame.mouse.get_pressed()
        _ = self.breaker.update(dt, mouse_buttons, self.rect, world, st)

        # Jump anim only after 2+ frames airborne — stops flicker when on_ground jitters
        if self._frames_off_ground >= 2:
            self.anim_state = "jump"
        elif dx != 0:
            self.anim_state = "run"
        else:
            self.anim_state = "idle"

        if self.anim_state != self.prev_anim_state:
            self.frame_index = 0
            self.timer = 0.0
        self.prev_anim_state = self.anim_state

        if self.anim_state == "idle":
            frames = self.idle_frames
            fd = self.frame_ms_idle
        elif self.anim_state == "run":
            frames = self.run_frames
            fd = self.frame_ms_run
        else:
            frames = self.jump_frames
            fd = self.frame_ms_jump

        base = frames[self.frame_index % len(frames)]
        self.image = (
            pygame.transform.flip(base, True, False)
            if not self.facing_right
            else base
        )

        self.timer += dt
        if self.timer >= fd:
            self.timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(frames)