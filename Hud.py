import pygame
from settings import (
    WIDTH, HEIGHT,
    WHITE, BLACK, GREEN, RED, YELLOW, CYAN, ORANGE, GREY,
    MAX_HEALTH, MAX_AMMO,
)


class HUD:

    BAR_WIDTH  = 150
    BAR_HEIGHT = 16
    MARGIN     = 12
    PADDING    = 6

    HP_HIGH = (50,  210,  80)
    HP_MID  = (255, 180,   0)
    HP_LOW  = (220,  50,  50)

    def __init__(self):
        self.font_large  = pygame.font.SysFont(None, 32)
        self.font_medium = pygame.font.SysFont(None, 26)
        self.font_small  = pygame.font.SysFont(None, 20)

    

    def draw(self, surface: pygame.Surface, player, wave_manager, score: int = 0,
             high_score: int = 0) -> None:
        self._draw_health_bar(surface, player)
        self._draw_ammo_bar(surface, player)
        self._draw_score(surface, score, high_score)
        self._draw_wave(surface, wave_manager)

    

    def _draw_health_bar(self, surface: pygame.Surface, player) -> None:
        x = self.MARGIN
        y = self.MARGIN

        ratio = max(player.health / MAX_HEALTH, 0)

        if ratio > 0.5:
            fill_color = self.HP_HIGH
        elif ratio > 0.25:
            fill_color = self.HP_MID
        else:
            fill_color = self.HP_LOW

        pygame.draw.rect(surface, BLACK,     (x - 1, y - 1, self.BAR_WIDTH + 2, self.BAR_HEIGHT + 2))
        pygame.draw.rect(surface, (80, 0, 0),(x,     y,     self.BAR_WIDTH,     self.BAR_HEIGHT))
        pygame.draw.rect(surface, fill_color,(x,     y,     int(self.BAR_WIDTH * ratio), self.BAR_HEIGHT))
        pygame.draw.rect(surface, WHITE,     (x,     y,     self.BAR_WIDTH,     self.BAR_HEIGHT), 1)

        label = self.font_small.render(f"HP  {player.health} / {MAX_HEALTH}", True, WHITE)
        surface.blit(label, (x, y + self.BAR_HEIGHT + self.PADDING - 2))

    def _draw_ammo_bar(self, surface: pygame.Surface, player) -> None:
        x = self.MARGIN
        y = self.MARGIN + self.BAR_HEIGHT + 28

        ratio      = max(player.ammo / MAX_AMMO, 0)
        fill_color = CYAN if ratio > 0.25 else ORANGE

        pygame.draw.rect(surface, BLACK,       (x - 1, y - 1, self.BAR_WIDTH + 2, self.BAR_HEIGHT + 2))
        pygame.draw.rect(surface, (0, 50, 80), (x,     y,     self.BAR_WIDTH,     self.BAR_HEIGHT))
        pygame.draw.rect(surface, fill_color,  (x,     y,     int(self.BAR_WIDTH * ratio), self.BAR_HEIGHT))
        pygame.draw.rect(surface, WHITE,       (x,     y,     self.BAR_WIDTH,     self.BAR_HEIGHT), 1)

        label = self.font_small.render(f"AMMO {player.ammo} / {MAX_AMMO}", True, WHITE)
        surface.blit(label, (x, y + self.BAR_HEIGHT + self.PADDING - 2))

    def _draw_score(self, surface: pygame.Surface, score: int,
                    high_score: int = 0) -> None:
        score_text = self.font_medium.render(f"SCORE  {score}", True, YELLOW)
        x = WIDTH - score_text.get_width() - self.MARGIN
        y = self.MARGIN
        surface.blit(score_text, (x, y))

        if high_score > 0:
            hi_text = self.font_small.render(f"BEST  {high_score}", True, ORANGE)
            surface.blit(hi_text, (WIDTH - hi_text.get_width() - self.MARGIN, y + 28))

    def _draw_wave(self, surface: pygame.Surface, wave_manager) -> None:
        wave_text = self.font_medium.render(f"WAVE  {wave_manager.current_wave}", True, CYAN)
        x = WIDTH - wave_text.get_width() - self.MARGIN
        y = self.MARGIN + 54   # pushed down to make room for best-score line
        surface.blit(wave_text, (x, y))

    

    def draw_start_screen(self, surface: pygame.Surface,
                          high_score: int = 0, best_wave: int = 0) -> None:
        surface.fill(BLACK)

        title = self.font_large.render("SPACE SHOOTER", True, CYAN)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))

        sub = self.font_medium.render("Press ENTER to Start", True, WHITE)
        surface.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 - 20))

        controls = [
            "Arrow Keys – Move",
            "Space – Shoot",
            "Collect green (HP) and cyan (AMMO) pickups",
        ]
        for i, line in enumerate(controls):
            hint = self.font_small.render(line, True, GREY)
            surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2,
                                HEIGHT // 2 + 30 + i * 22))

        # Show persistent records if any games have been played
        if high_score > 0 or best_wave > 0:
            hi_line = self.font_small.render(
                f"Best Score: {high_score}   Best Wave: {best_wave}", True, YELLOW)
            surface.blit(hi_line, (WIDTH // 2 - hi_line.get_width() // 2,
                                   HEIGHT // 2 + 110))

    def draw_game_over_screen(self, surface: pygame.Surface,
                              score: int, wave: int,
                              high_score: int = 0, best_wave: int = 0,
                              new_record: bool = False) -> None:
        surface.fill(BLACK)

        title = self.font_large.render("GAME OVER", True, RED)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2,
                             HEIGHT // 2 - 100))

        score_line = self.font_medium.render(f"Final Score : {score}", True, YELLOW)
        surface.blit(score_line, (WIDTH // 2 - score_line.get_width() // 2,
                                  HEIGHT // 2 - 48))

        wave_line = self.font_medium.render(f"Wave Reached : {wave}", True, CYAN)
        surface.blit(wave_line, (WIDTH // 2 - wave_line.get_width() // 2,
                                 HEIGHT // 2 - 12))

        # Show all-time bests
        best_line = self.font_small.render(
            f"All-Time Best — Score: {high_score}   Wave: {best_wave}", True, ORANGE)
        surface.blit(best_line, (WIDTH // 2 - best_line.get_width() // 2,
                                 HEIGHT // 2 + 22))

        # Flash "NEW RECORD!" if the player just set one
        if new_record:
            rec_text = self.font_medium.render("★  NEW RECORD!  ★", True, YELLOW)
            surface.blit(rec_text, (WIDTH // 2 - rec_text.get_width() // 2,
                                    HEIGHT // 2 + 50))

        restart = self.font_small.render("Press R to Restart  |  ESC to Quit",
                                         True, WHITE)
        surface.blit(restart, (WIDTH // 2 - restart.get_width() // 2,
                               HEIGHT // 2 + 80))
