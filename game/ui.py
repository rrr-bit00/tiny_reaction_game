"""Rendering helpers for the reaction game."""
import pygame

from . import fonts
from .config import BLACK, WHITE, YELLOW


def draw_countdown(screen: pygame.Surface, label: str) -> None:
    font = fonts.load_font(80)
    text = font.render(label, True, WHITE)
    screen.blit(text, [375, 50])


def draw_instruction(screen: pygame.Surface, rect: pygame.Rect, color: tuple, text: str) -> None:
    pygame.draw.rect(screen, color, rect)
    font = fonts.load_font(30)
    rendered = font.render(text, True, BLACK)
    text_rect = rendered.get_rect(center=rect.center)
    screen.blit(rendered, text_rect)


def draw_results(screen: pygame.Surface, average: float) -> None:
    font_small = fonts.load_font(40)
    font_large = fonts.load_font(70)
    intro = font_small.render("あなたの平均反応速度は・・・", True, WHITE)
    result = font_large.render(f"{average:.3f}", True, YELLOW)
    outro = font_small.render("でした！", True, WHITE)

    screen.blit(intro, [125, 100])
    screen.blit(result, [315, 180])
    screen.blit(outro, [325, 300])
