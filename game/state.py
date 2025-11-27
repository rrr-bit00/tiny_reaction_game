"""Game state objects to keep the loop organised."""
from dataclasses import dataclass, field
from typing import List, Optional

import pygame

from .config import (
    BLUE,
    COLOR_CHANGE_RANGE_MS,
    COUNTDOWN_DURATION_MS,
    RECT_DEFAULT,
    RECT_HEIGHT,
    RECT_WIDTH,
    RECT_X,
    RECT_Y,
    REQUIRED_ATTEMPTS,
)


@dataclass
class CountdownState:
    start_time_ms: int = 0
    active: bool = True

    def remaining_label(self, current_time_ms: int) -> Optional[str]:
        """Return the current countdown label or None when finished."""
        if not self.active:
            return None

        elapsed = current_time_ms - self.start_time_ms
        if elapsed < 1000:
            return "3"
        if elapsed < 2000:
            return "2"
        if elapsed < COUNTDOWN_DURATION_MS:
            return "1"

        self.active = False
        return None


@dataclass
class ReactionState:
    instruction: str = "青色になったらここをクリック！！"
    rect_color: tuple = RECT_DEFAULT
    pending_color_change_ms: Optional[int] = None
    last_change_at_ms: int = 0
    awaiting_click: bool = False
    attempts: List[float] = field(default_factory=list)

    @property
    def rectangle(self) -> pygame.Rect:
        return pygame.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)

    def schedule_color_change(self, random_ms: int) -> None:
        self.pending_color_change_ms = random_ms

    def start_listening(self, current_time_ms: int) -> None:
        self.awaiting_click = True
        self.rect_color = BLUE
        self.last_change_at_ms = current_time_ms
        self.pending_color_change_ms = None
        self.instruction = "クリック！！"

    def reset_for_next_round(self) -> None:
        self.awaiting_click = False
        self.rect_color = RECT_DEFAULT
        self.instruction = "青色になったらここをクリック！！"

    def record_attempt(self, reaction_ms: int) -> None:
        self.attempts.append(reaction_ms / 1000)
        self.reset_for_next_round()

    def ready_for_results(self) -> bool:
        return len(self.attempts) >= REQUIRED_ATTEMPTS


@dataclass
class GameState:
    countdown: CountdownState
    reaction: ReactionState

    @classmethod
    def create(cls, start_time_ms: int) -> "GameState":
        return cls(
            CountdownState(start_time_ms=start_time_ms),
            ReactionState(last_change_at_ms=start_time_ms),
        )


def choose_color_change_delay(random_generator) -> int:
    """Pick a random millisecond delay for the colour change."""
    return random_generator.randint(*COLOR_CHANGE_RANGE_MS)
