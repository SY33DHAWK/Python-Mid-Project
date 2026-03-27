import pygame
import random
from settings import (
    WIDTH, HEIGHT,
    RED, ORANGE, YELLOW, CYAN, PURPLE,
    ENEMY_SPEED_BASE, ENEMY_HEALTH, WAVE_SIZE,
)

from enemy import Enemy
from boss import Boss           


class WaveManager:
    POINTS_ENEMY = 100
    POINTS_BOSS  = 1000

    def __init__(self):
        self.current_wave: int         = 0
        self.enemies:      list        = []
        self.boss:         Boss | None = None   
        self.score_earned: int         = 0

        self._spawning    = False
        self._spawn_queue: list = []
        self._spawn_timer = 0
        self._spawn_delay = 40

   

    def next_wave(self):
        self.current_wave += 1
        self._prepare_wave(self.current_wave)

    def update(self, bullets: list, pickups: list):
        self._handle_spawning()

        if self.boss:
            self.boss.update()
            self._check_bullet_hits_boss(bullets, pickups)
            if not self.boss.alive:
                self.score_earned += self.POINTS_BOSS
                self.boss = None
        else:
            for enemy in self.enemies:
                if enemy.alive:
                    enemy.update()

            self._check_bullet_hits_enemies(bullets, pickups)
            self.enemies = [e for e in self.enemies if e.alive]

    def draw(self, surface: pygame.Surface):
        if self.boss:
            self.boss.draw(surface)
        else:
            for enemy in self.enemies:
                enemy.draw(surface)

    def is_wave_clear(self) -> bool:
        if self._spawn_queue:
            return False
        if self.boss:
            return not self.boss.alive
        return len(self.enemies) == 0

    

    def _prepare_wave(self, wave: int):
        self.enemies.clear()
        self.boss = None

        if wave % 5 == 0:
            self._spawn_boss(wave)
        else:
            count  = min(WAVE_SIZE + 2 * (wave - 1), 20)
            speed  = min(ENEMY_SPEED_BASE + 0.3 * (wave - 1), 6.0)
            health = ENEMY_HEALTH + 10 * (wave - 1)
            color  = self._wave_color(wave)

            self._spawn_queue = self._build_spawn_queue(count, speed, health, color)
            self._spawning    = True
            self._spawn_timer = 0

    def _build_spawn_queue(self, count, speed, health, color) -> list:
        queue   = []
        cols    = min(count, 8)
        spacing = WIDTH // (cols + 1)

        for i in range(count):
            col = i % cols
            row = i // cols
            x   = spacing * (col + 1)
            y   = -Enemy.HEIGHT * 1.5 - row * (Enemy.HEIGHT + 10)
            queue.append(Enemy(x, y, speed, health, color))
        return queue

    def _spawn_boss(self, wave: int):
        phase_extra = (wave // 5) - 1
        self.boss   = Boss(WIDTH // 2, -60, phase_extra)   # fixed: was boss()
        self._spawning = False
        self._spawn_queue.clear()

    def _handle_spawning(self):
        if not self._spawning or not self._spawn_queue:
            self._spawning = False
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self._spawn_delay:
            self._spawn_timer = 0
            released = self._spawn_queue.pop(0)
            self.enemies.append(released)

    def _check_bullet_hits_enemies(self, bullets: list, pickups: list):
        for bullet in bullets[:]:
            if not getattr(bullet, "alive", True):
                continue
            b_rect = bullet.get_rect() if hasattr(bullet, "get_rect") else bullet.rect

            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                if b_rect.colliderect(enemy.get_rect()):
                    killed = enemy.take_damage(getattr(bullet, "damage", 25))
                    bullet.alive = False

                    if killed:
                        self.score_earned += self.POINTS_ENEMY
                        self._maybe_drop_pickup(enemy, pickups)
                    break

    def _check_bullet_hits_boss(self, bullets: list, pickups: list):
        for bullet in bullets[:]:
            if not getattr(bullet, "alive", True):
                continue
            b_rect = bullet.get_rect() if hasattr(bullet, "get_rect") else bullet.rect

            if b_rect.colliderect(self.boss.get_rect()):
                self.boss.take_damage(getattr(bullet, "damage", 25))
                bullet.alive = False

    def _maybe_drop_pickup(self, enemy: Enemy, pickups: list):
        from settings import PICKUP_DROP_CHANCE
        if random.random() < PICKUP_DROP_CHANCE:
            from pickup import Pickup
            pickups.append(Pickup(enemy.x, enemy.y))

    @staticmethod
    def _wave_color(wave: int) -> tuple:
        palette = [RED, ORANGE, YELLOW, CYAN, PURPLE]
        return palette[(wave - 1) % len(palette)]
