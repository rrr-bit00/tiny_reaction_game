"""Font utilities for the game."""
from typing import Optional

import pygame

from .config import FONT_FILE


def resolve_font_path() -> Optional[str]:
    """Return a usable font path if the bundled font exists."""
    return str(FONT_FILE) if FONT_FILE.exists() else None


def load_font(size: int) -> pygame.font.Font:
    """Load a pygame font with a bundled fallback."""
    font_path = resolve_font_path()
    return pygame.font.Font(font_path, size)
