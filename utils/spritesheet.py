import os
import pygame


def _project_path(*parts):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, *parts)


class SpriteSheet:
    def __init__(self, filename):
        path = filename if os.path.isabs(filename) else _project_path(filename)
        self.sheet = pygame.image.load(path).convert_alpha()

    def get_image(self, frame_index, width, height, row=0):
        rect = pygame.Rect(frame_index * width, row * height, width, height)
        return self.sheet.subsurface(rect).copy()

    @staticmethod
    def split_horizontal_strip(sheet_surface, frame_count):
        """
        One row of `frame_count` equal-width frames (e.g. Dino: 24 frames).
        Trims any extra width from scaling so slices stay aligned (reduces neighbor bleed).
        """
        sw, sh = sheet_surface.get_size()
        fw = sw // frame_count
        if fw < 1:
            raise ValueError("Invalid frame_count for sheet width")
        usable_w = fw * frame_count
        if usable_w < sw:
            sheet_surface = sheet_surface.subsurface((0, 0, usable_w, sh)).copy()
        frames = []
        for i in range(frame_count):
            r = pygame.Rect(i * fw, 0, fw, sh)
            frames.append(sheet_surface.subsurface(r).copy())
        return frames

    @staticmethod
    def split_four_frames(sheet_surface):
        """Backward-compatible helper for 4-frame sheets."""
        sw, sh = sheet_surface.get_size()
        if sw == sh and sw % 2 == 0:
            fw, fh = sw // 2, sh // 2
            frames = []
            for row in range(2):
                for col in range(2):
                    r = pygame.Rect(col * fw, row * fh, fw, fh)
                    frames.append(sheet_surface.subsurface(r).copy())
            return frames
        if sw % 4 == 0:
            fw = sw // 4
            frames = []
            for i in range(4):
                r = pygame.Rect(i * fw, 0, fw, sh)
                frames.append(sheet_surface.subsurface(r).copy())
            return frames
        raise ValueError(
            f"Could not split spritesheet of size {sw}x{sh} into 4 frames"
        )
