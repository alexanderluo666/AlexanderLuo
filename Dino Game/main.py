import pygame
from world.terrain import Worldgen
from settings import Settings
from entities.player import Player
from utils.reach import (
    is_in_reach,
    set_window_icon_from_frame,
)

pygame.init()
st = Settings()
screen = pygame.display.set_mode((st.WIDTH, st.HEIGHT))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()

wg = Worldgen()
pl = Player(st)

set_window_icon_from_frame(pl.idle_frames[0])
font = pygame.font.SysFont(None, 20)

pet_timer = 0.0  # Timer for pet animation
pet_duration = 300.0  # Duration to show pet animation (ms)

running = True
while running:
    dt = clock.tick(st.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                wg.selected_block = "grass"
            elif event.key == pygame.K_2:
                wg.selected_block = "dirt"
            elif event.key == pygame.K_3:
                wg.selected_block = "stone"
            elif event.key == pygame.K_4:
                wg.selected_block = "sand"
            elif event.key == pygame.K_5:
                wg.selected_block = "wood"
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                st.PLAYER_SPRITE_SCALE = max(0.5, st.PLAYER_SPRITE_SCALE - 0.25)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            
            # Check if clicking on the dino to pet
            if event.button == 1 and pl.rect.collidepoint(mx, my):
                pet_timer = pet_duration
                continue
            
            if not is_in_reach(pl.rect, (mx, my), st.TILE_SIZE, st.REACH_BLOCKS):
                continue
            grid_pos = (mx // st.TILE_SIZE, my // st.TILE_SIZE)

            if event.button == 3:
                wg.world[grid_pos] = wg.selected_block
            elif event.button == 2 and grid_pos in wg.world:
                wg.selected_block = wg.world[grid_pos]
            # Left click now uses block breaker; no instant delete here

    # Update pet animation timer
    if pet_timer > 0:
        pet_timer -= dt
    
    keys = pygame.key.get_pressed()
    
    # Check for Shift key to decrease size and show jumping frame
    shift_held = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    if shift_held:
        st.PLAYER_SPRITE_SCALE = max(0.5, st.PLAYER_SPRITE_SCALE - dt * 0.0005)
    
    # Check for Ctrl key to increase size
    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
        st.PLAYER_SPRITE_SCALE = min(4.0, st.PLAYER_SPRITE_SCALE + dt * 0.0005)
    
    # Reduce speed by 50% when shifting
    original_speed = st.PLAYER_SPEED
    if shift_held:
        st.PLAYER_SPEED = st.PLAYER_SPEED * 0.5
    
    pl.update(dt, keys, wg.world)
    
    # Restore original speed
    st.PLAYER_SPEED = original_speed

    screen.fill((30, 30, 30))
    tile = st.TILE_SIZE
    blit = screen.blit
    images = wg.block_images
    for (gx, gy), block_type in wg.world.items():
        blit(images[block_type], (gx * tile, gy * tile))

    # Minecraft-style cracking overlay while mining
    if pl.breaker.target:
        progress = pl.breaker.progress()
        crack_stage = min(8, max(1, int(progress * 8)))
        target_x, target_y = pl.breaker.target
        overlay = pygame.Surface((tile, tile), pygame.SRCALPHA)
        for line_idx in range(crack_stage):
            offset = (line_idx + 1) * tile // 9
            alpha = int(120 * (line_idx + 1) / 8)
            color = (50, 50, 50, alpha)
            pygame.draw.line(overlay, color, (0, offset), (tile, offset), 2)
            pygame.draw.line(overlay, color, (offset, 0), (offset, tile), 2)
            pygame.draw.line(overlay, color, (0, 0), (offset, tile), 2)
            pygame.draw.line(overlay, color, (0, tile), (offset, 0), 2)
        screen.blit(overlay, (target_x * tile, target_y * tile))

    # Display appropriate frame based on state
    if shift_held:
        # Show jumping frame when shift is held (size adjustment mode)
        jump_frame = pl.jump_frames[len(pl.jump_frames) // 2]  # Middle frame of jump animation
        jump_image = pygame.transform.flip(jump_frame, not pl.facing_right, False) if not pl.facing_right else jump_frame
        blit(jump_image, pl.rect)
    elif pet_timer > 0:
        # Show petting animation if active
        pet_frame_index = int((1 - pet_timer / pet_duration) * len(pl.jump_frames))
        pet_frame = pl.jump_frames[min(pet_frame_index, len(pl.jump_frames) - 1)]
        pet_image = pygame.transform.flip(pet_frame, not pl.facing_right, False) if not pl.facing_right else pet_frame
        blit(pet_image, pl.rect)
    else:
        # Show normal image
        blit(pl.image, pl.rect)

    # Draw block-breaking progress bar if breaking currently
    if pl.breaker.target:
        progress = pl.breaker.progress()
        bar_w, bar_h = 100, 10
        bar_x = pl.rect.centerx - bar_w // 2
        bar_y = pl.rect.top - 20
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, (150, 200, 60), (bar_x, bar_y, int(bar_w * progress), bar_h))
        label = font.render(f"Breaking {int(progress * 100)}%", True, (255, 255, 255))
        screen.blit(label, (bar_x, bar_y - 18))

    pygame.display.flip()

pygame.quit()