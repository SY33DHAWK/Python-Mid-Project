import pygame
from settings import (BULLET_SPEED, ORANGE)

class Bullet:
    def __init__(self, x, y):
        self.alive = True

        self.image = pygame.Surface((6, 16))
        self.image.fill(ORANGE)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.damage = 55  

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.alive = False

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)
