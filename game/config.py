"""Configuration and constants for the reaction game."""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WindowConfig:
    width: int = 800
    height: int = 600
    fps: int = 60


# Colours (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RECT_DEFAULT = (255, 255, 255)


# Rectangles and timing
RECT_X = 150
RECT_Y = 200
RECT_WIDTH = 500
RECT_HEIGHT = 300
COUNTDOWN_DURATION_MS = 3000
COLOR_CHANGE_RANGE_MS = (1000, 5000)
REQUIRED_ATTEMPTS = 5


ASSETS_DIR = Path(__file__).resolve().parent.parent
FONT_FILE = ASSETS_DIR / "NotoSansJP-VariableFont_wght.ttf"
