import sys
import random
import pygame

from settings import (
    WIDTH, HEIGHT, FPS, TITLE,
    BLACK, WHITE, CYAN, YELLOW,
    PLAYER_SPEED,
)
from player       import Player
from wave_manger  import WaveManager
from Hud          import HUD
from save_manager import SaveManager   # <-- persistence



class StarField:
    def __init__(self, n: int = 80):
        self.stars = [
            [random.randint(0, WIDTH),
             random.randint(0, HEIGHT),
             random.uniform(0.3, 1.8)]
            for _ in range(n)
        ]

    def update(self):
        for s in self.stars:
            s[1] += s[2]
            if s[1] > HEIGHT:
                s[1] = 0
                s[0] = random.randint(0, WIDTH)

    def draw(self, surface: pygame.Surface):
        for x, y, speed in self.stars:
            brightness = int(100 + speed / 1.8 * 155)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(surface, color, (int(x), int(y)), 1)




STATE_START     = "start"
STATE_PLAYING   = "playing"
STATE_GAME_OVER = "game_over"


def new_game():
    """Return a fresh (player, wave_manager, bullets, pickups, score, enemies_killed)."""
    player         = Player()
    wave_manager   = WaveManager()
    bullets        = []
    pickups        = []
    score          = 0
    enemies_killed = 0
    wave_manager.next_wave()
    return player, wave_manager, bullets, pickups, score, enemies_killed




def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    hud       = HUD()
    starfield = StarField()
    save_mgr  = SaveManager()          # load persistent data on startup

    state                                                         = STATE_START
    player, wave_manager, bullets, pickups, score, enemies_killed = new_game()

    new_record = False   # flash "NEW RECORD!" on game-over screen

    running = True
    while running:

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if state == STATE_START:
                    if event.key == pygame.K_RETURN:
                        player, wave_manager, bullets, pickups, score, enemies_killed = new_game()
                        new_record = False
                        state = STATE_PLAYING

                elif state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        player, wave_manager, bullets, pickups, score, enemies_killed = new_game()
                        new_record = False
                        state = STATE_PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                elif state == STATE_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        running = False

        
        starfield.update()

        if state == STATE_PLAYING:

            # Player input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]  and player.rect.left   > 0:
                player.rect.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player.rect.right  < WIDTH:
                player.rect.x += PLAYER_SPEED
            if keys[pygame.K_UP]    and player.rect.top    > 0:
                player.rect.y -= PLAYER_SPEED
            if keys[pygame.K_DOWN]  and player.rect.bottom < HEIGHT:
                player.rect.y += PLAYER_SPEED
            if keys[pygame.K_SPACE]:
                player.shoot(bullets)

            
            for b in bullets[:]:
                b.update()
                if not getattr(b, "alive", True):
                    bullets.remove(b)

            
            wave_manager.update(bullets, pickups)

            # Track enemies killed via score delta
            newly_earned = wave_manager.score_earned
            score       += newly_earned
            if newly_earned >= WaveManager.POINTS_ENEMY:
                enemies_killed += newly_earned // WaveManager.POINTS_ENEMY
            wave_manager.score_earned = 0

            
            if wave_manager.is_wave_clear():
                wave_manager.next_wave()

            
            for p in pickups[:]:
                p.update()
                if not p.alive:
                    pickups.remove(p)
                    continue
                if p.get_rect().colliderect(player.rect):
                    p.apply(player)
                    pickups.remove(p)

            
            if wave_manager.boss:
                for bb in wave_manager.boss.bullets:
                    if bb.alive and bb.get_rect().colliderect(player.rect):
                        player.take_damage(bb.damage)
                        bb.alive = False

            
            for enemy in wave_manager.enemies:
                if enemy.alive and enemy.get_rect().colliderect(player.rect):
                    player.take_damage(20)
                    enemy.alive = False

            
            if not player.is_alive:
                # ---- save progress when game ends ----
                new_record = save_mgr.update_after_game(
                    score, wave_manager.current_wave, enemies_killed
                )
                state = STATE_GAME_OVER

        
        screen.fill(BLACK)
        starfield.draw(screen)

        if state == STATE_START:
            hud.draw_start_screen(screen, save_mgr.high_score, save_mgr.best_wave)

        elif state == STATE_PLAYING:
            
            wave_manager.draw(screen)

            for b in bullets:
                b.draw(screen)

            for p in pickups:
                p.draw(screen)

            player.draw(screen)

            
            hud.draw(screen, player, wave_manager, score, save_mgr.high_score)

        elif state == STATE_GAME_OVER:
           
            wave_manager.draw(screen)
            player.draw(screen)
            hud.draw_game_over_screen(
                screen, score, wave_manager.current_wave,
                save_mgr.high_score, save_mgr.best_wave, new_record
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
