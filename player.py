import pygame
from settings import (
    WIDTH, HEIGHT, CYAN, MAX_HEALTH, MAX_AMMO, SHOOT_COOLDOWN)
from bullet import Bullet

class Player:
    def __init__(self):

        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        

        self.health = MAX_HEALTH
        self.ammo = MAX_AMMO
        self.last_shot_time = 0
        self.is_alive = True  

    def shoot(self, bullet_list):
        now = pygame.time.get_ticks()
        
        if self.ammo > 0 and now - self.last_shot_time > SHOOT_COOLDOWN:
            
            new_bullet = Bullet(self.rect.centerx, self.rect.top)
            
            bullet_list.append(new_bullet)

            self.ammo -= 1
            self.last_shot_time = now

    def take_damage(self, amount):
        self.health -= amount
        
        if self.health <= 0:
            self.health = 0
            self.is_alive = False 

    def add_health(self, amount):
        self.health += amount
        if self.health > MAX_HEALTH:
            self.health = MAX_HEALTH

    def add_ammo(self, amount):
        self.ammo += amount
        if self.ammo > MAX_AMMO:
            self.ammo = MAX_AMMO

    def draw(self, screen):
        if self.is_alive:
            screen.blit(self.image, self.rect)