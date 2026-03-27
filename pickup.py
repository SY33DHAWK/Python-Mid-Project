import pygame
import random
from settings import (
    WIDTH, HEIGHT,
    GREEN, CYAN, YELLOW, WHITE, BLACK,
    HEALTH_PICKUP_VALUE, AMMO_PICKUP_VALUE,
)


class Pickup:
    SIZE = 16
    SPEED = 1.2

    KIND_HEALTH = "health"
    KIND_AMMO   = "ammo"

    def __init__(self, x: float, y: float):
        self.x  = float(x)
        self.y = float(y)
        self.alive = True


        self.kind = random.choice([self.KIND_HEALTH, self.KIND_AMMO])

        if self.kind == self.KIND_HEALTH:
         self.color   = GREEN
         self.inner_color = WHITE
         self.value  = HEALTH_PICKUP_VALUE
        else:
           self.color = CYAN
           self.inner_color = YELLOW
           self.value = AMMO_PICKUP_VALUE


           self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
           self._sync_rect()



           def update(self):
              if not self.alive:
                 return
              
              self.y += self.SPEED
              self._sync_rect()

              if self.y > HEIGHT + self.SIZE:
                 self.alive = False

                 def apply(self, player) -> None:
                    if not self.alive:
                       return
                    
                    if self.kind == self.KIND_HEALTH:
                       player.add_health(self.value)
                    else:
                       player.add_ammo(self.value)

                       self.alive = False

                       def draw(self, surface: pygame.Surface):
                          if not self.alive:
                             return
                          
                          cx = int(self.x)
                          cy = int(self.y)
                          r  = self.SIZE


                          pygame.draw.circle(surface, self.color, (cx, cy), r)
                          pygame.draw.circle(surface, WHITE, (cx, cy), r, 1)


                          pygame.draw.circle(surface, self.inner_color, (cx - 2, cy - 2))


                          font = pygame.font.SysFont(None, 14)
                          label = "H" if self.kind == self.KIND_HEALTH else "A"
                          text = font.render(label, True, BLACK)
                          surface.blit(text, (cx - text.get_width(), cy - text.get_height()))



                          def get_rect(self) -> pygame.Rect:
                             self._sync_rect()
                             return self.rect
                          
                          def _sync_rect(self):
                             self.rect.x = int(self.x - self.SIZE)
                             self.rect.y = int(self.y - self.SIZE)                       








