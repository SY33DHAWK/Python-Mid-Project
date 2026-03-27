import pygame
import random
from settings import (
    WIDTH, HEIGHT,
    RED, ORANGE, YELLOW, WHITE, BLACK, PURPLE, CYAN,
    BOSS_HEALTH, BULLET_DAMAGE,
)

class BossBullet:
    WIDTH  = 8
    HEIGHT = 16
    SPEED  = 4
    DAMAGE = 15

    def __init__(self, x: float, y: float):
        self.x     = float(x)
        self.y     = float(y)
        self.alive = True
        self.damage = self.DAMAGE
        self.rect  = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self._sync_rect()
 
    def update(self):
        self.y += self.SPEED
        self._sync_rect()
        if self.y > HEIGHT + self.HEIGHT:
            self.alive = False
 
    def draw(self, surface: pygame.Surface):
        if not self.alive:
            return
        pygame.draw.ellipse(surface, ORANGE, self.rect)

        inner = self.rect.inflate(-4, -6)
        pygame.draw.ellipse(surface, YELLOW, inner)

    
    def get_rect(self) -> pygame.Rect:
        return self.rect
 
    def _sync_rect(self):
        self.rect.x = int(self.x - self.WIDTH  // 2)
        self.rect.y = int(self.y - self.HEIGHT // 2)


class Boss:
    WIDTH = 100
    HEIGHT = 70

    SHOOT_INTERVAL_P1 = 90
    SHOOT_INTERVAL_P2 = 45
    ENTRY_SPEED = 2

    SPEED_P1 =2.0

    def __init__(self, x: float, y: float, extra_cycles: int = 0):
        self.x        = float(x)
        self.y        = float(y)          
        self.extra    = extra_cycles

        self.max_health = BOSS_HEALTH + 100 * extra_cycles
        self.health     = self.max_health
        self.alive      = True
 
        self.phase      = 1
        self._speed_p2  = self.SPEED_P1 * 2 + extra_cycles * 0.5

        self._dx        = self.SPEED_P1
        self._target_y  = 80.0          
        self._entered   = False

        self.bullets: list[BossBullet] = []
        self._shoot_timer = 0
 
        self._flash_timer = 0
 
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self._sync_rect()



    def update(self):
        if not self.alive:
            return
 
        if not self._entered:
            self.y += self.ENTRY_SPEED
            if self.y >= self._target_y:
                self.y       = self._target_y
                self._entered = True
            self._sync_rect()
            return
 
        speed = self._speed_p2 if self.phase == 2 else self.SPEED_P1
        self.x += self._dx * (speed / self.SPEED_P1)

        half_w = self.WIDTH // 2
        if self.x <= half_w:
            self.x = float(half_w)
            self._dx = abs(self._dx)
        elif self.x >= WIDTH - half_w:
            self.x = float(WIDTH - half_w)
            self._dx = -abs(self._dx)
 
        self._sync_rect()
 
        self._shoot_timer += 1
        interval = self.SHOOT_INTERVAL_P2 if self.phase == 2 else self.SHOOT_INTERVAL_P1
        if self._shoot_timer >= interval:
            self._shoot_timer = 0
            self._fire()

        for b in self.bullets:
            b.update()
        self.bullets = [b for b in self.bullets if b.alive]
 
        if self._flash_timer > 0:
            self._flash_timer -= 1

    def take_damage(self, amount: int = BULLET_DAMAGE):
        
        if not self.alive:
            return
        self.health -= amount
        self._flash_timer = 6
 
        if self.phase == 1 and self.health <= self.max_health // 2:
            self.phase = 2
            
            self._dx = self._speed_p2 if self._dx > 0 else -self._speed_p2
 
        if self.health <= 0:
            self.health = 0
            self.alive  = False
    

    def draw(self, surface: pygame.Surface):
        if not self.alive:
            return
        
        cx, cy= int(self.x), int(self.y)
        hw, hh= self.WIDTH // 2, self.HEIGHT // 2

        if self._flash_timer > 0:
            body_color   = WHITE
            accent_color = WHITE
        elif self.phase == 2:
            body_color   = ORANGE
            accent_color = YELLOW
        else:
            body_color   = PURPLE
            accent_color = CYAN

        
        hull = [
            (cx,          cy - hh),       
            (cx + hw,     cy - hh // 2),  
            (cx + hw,     cy + hh // 2),  
            (cx,          cy + hh),      
            (cx - hw,     cy + hh // 2),  
            (cx - hw,     cy - hh // 2),
        ]

        pygame.draw.polygon(surface, body_color, hull)
        pygame.draw.polygon(surface, WHITE, hull, 2)

        nozzle_ys = [(cy + hh - 6, 14, 8)]
        if self.phase == 2:
            nozzle_ys = [
                (cy + hh - 5,  12, 8),
                (cy + hh - 5,  12, 8),
                (cy + hh - 5,  12, 8),
            ]
            offsets = [-28, 0, 28]
        else:
            offsets = [0]
 
        for nx, (ny, nw, nh) in zip(offsets if self.phase == 2 else [0],
                                    nozzle_ys):
            pygame.draw.ellipse(surface, accent_color,
                                (cx + nx - nw // 2, ny, nw, nh))
            
        dome_rect = pygame.Rect(cx - 18, cy - 18, 36, 28)
        pygame.draw.ellipse(surface, accent_color, dome_rect)
        pygame.draw.ellipse(surface, WHITE, dome_rect, 1)


        for side in (-1, 1):
            cannon_x = cx + side * (hw - 4)
            cannon_y = cy + 8
            pygame.draw.rect(surface, accent_color,
                             (cannon_x - 4, cannon_y, 8, 18), border_radius=2)
            
        bar_w  = self.WIDTH + 20
        bar_h  = 8
        bar_x  = cx - bar_w // 2
        bar_y  = cy - hh - 18
        ratio  = self.health / self.max_health
 
        pygame.draw.rect(surface, BLACK,      (bar_x - 1, bar_y - 1, bar_w + 2, bar_h + 2))
        pygame.draw.rect(surface, (140, 0, 0),(bar_x, bar_y, bar_w, bar_h))
        fill_color = (220, 50, 50) if self.phase == 1 else ORANGE
        pygame.draw.rect(surface, fill_color, (bar_x, bar_y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(surface, WHITE,      (bar_x, bar_y, bar_w, bar_h), 1)

        font = pygame.font.SysFont(None, 22)
        label = font.render(f"BOSS  HP {self.health}/{self.max_health}", True, WHITE)
        surface.blit(label, (bar_x, bar_y - 18))

        if self.phase == 2:
            p2_label = font.render("!! PHASE 2 !!", True, ORANGE)
            surface.blit(p2_label, (cx - p2_label.get_width() // 2, cy + hh + 6))

        for b in self.bullets:
            b.draw(surface)
    

    def _fire(self):
        """Spawn one bullet (phase 1) or three spread bullets (phase 2)."""
        if self.phase == 1:
            self.bullets.append(BossBullet(self.x, self.y + self.HEIGHT // 2))
        else:
            for offset in (-20, 0, 20):
                self.bullets.append(BossBullet(self.x + offset, self.y + self.HEIGHT // 2))
    
    def _sync_rect(self):
        self.rect.x = int(self.x - self.WIDTH  // 2)
        self.rect.y = int(self.y - self.HEIGHT // 2)
 
    def get_rect(self) -> pygame.Rect:
        self._sync_rect()
        return self.rect
    


