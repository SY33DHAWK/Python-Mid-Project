import pygame
import random
from settings import(
    WIDTH, HEIGHT,
    RED, ORANGE, YELLOW, WHITE, BLACK,
    ENEMY_SPEED_BASE, ENEMY_HEALTH,
    BULLET_DAMAGE,
)

class Enemy:
    
    WIDTH = 40
    HEIGHT = 30

    def __init__(self, x: float, y: float, speed: float, health: int, color=None):
        self.x      = float(x)
        self.y      = float(y)
        self.width  = Enemy.WIDTH
        self.height = Enemy.HEIGHT
        self.speed  = speed
        self.health = health
        self.max_health = health
        self.alive  = True
        self.color  = color if color else RED

        self._drift = random.uniform(-0.4, 0.4)

        self.rect = pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height,
        )

    def update(self):
        
        self.y += self.speed
        self.x += self._drift

        if self.x < self.width // 2 or self.x> WIDTH - self.width // 2:
            self._drift *= -1
        
        self._sync_rect()


        if self.y > HEIGHT + self.height:
            self.alive = False

    
    def take_damage(self, amount: int = BULLET_DAMAGE):
        
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive  = False
            return True
        return False
    
    def draw(self, surface: pygame.Surface):
        
        if not self.alive:
            return
 
        cx, cy = int(self.x), int(self.y)
        hw, hh = self.width // 2, self.height // 2

        body_points = [
            (cx,          cy + hh),      
            (cx - hw,     cy - hh),      
            (cx - hw + 6, cy - hh + 10), 
            (cx,          cy - hh + 6),  
            (cx + hw - 6, cy - hh + 10), 
            (cx + hw,     cy - hh),      
        ]
        pygame.draw.polygon(surface, self.color, body_points)
        pygame.draw.polygon(surface, WHITE, body_points, 1) 

        glow_rect = pygame.Rect(cx - 4, cy - hh - 4, 8, 5)
        pygame.draw.rect(surface, YELLOW, glow_rect, border_radius=2)

        bar_w  = self.width
        bar_h  = 4
        bar_x  = cx - bar_w // 2
        bar_y  = cy - hh - 10
        ratio  = self.health / self.max_health
 
        pygame.draw.rect(surface, BLACK, (bar_x - 1, bar_y - 1, bar_w + 2, bar_h + 2))
        pygame.draw.rect(surface, (180, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, (50, 220, 50),
                         (bar_x, bar_y, int(bar_w * ratio), bar_h))
        
    def _sync_rect(self):
        self.rect.x = int(self.x - self.width // 2)
        self.rect.y = int(self.y - self.height // 2)
    

    def get_rect(self) -> pygame.Rect:
        self._sync_rect()
        return self.rect
    