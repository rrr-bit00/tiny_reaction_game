"""Core game loop organised into a class-based architecture."""
import random
from typing import Optional

import pygame
from pygame.locals import MOUSEBUTTONDOWN

from .config import BLACK, RECT_DEFAULT, WindowConfig
from .state import GameState, choose_color_change_delay
from .ui import draw_countdown, draw_instruction, draw_results


class ReactionGame:
    def __init__(self, window: WindowConfig = WindowConfig()):
        pygame.init()
        self.window = window
        self.screen = pygame.display.set_mode((window.width, window.height))
        self.clock = pygame.time.Clock()
        self.state = GameState.create(start_time_ms=pygame.time.get_ticks())

    def run(self) -> None:
        while True:
            self._process_events()
            self._update_state()
            self._render()
            self.clock.tick(self.window.fps)

    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == MOUSEBUTTONDOWN:
                self._handle_click(event.pos)

    def _handle_click(self, position: tuple) -> None:
        reaction = self.state.reaction
        if reaction.awaiting_click and reaction.rectangle.collidepoint(position):
            now = pygame.time.get_ticks()
            reaction.record_attempt(now - reaction.last_change_at_ms)

    def _update_state(self) -> None:
        now = pygame.time.get_ticks()
        countdown_label = self.state.countdown.remaining_label(now)
        if countdown_label:
            return

        if self.state.reaction.ready_for_results():
            return

        self._update_reaction(now)

    def _update_reaction(self, now: int) -> None:
        reaction = self.state.reaction
        if reaction.pending_color_change_ms is None and not reaction.awaiting_click:
            reaction.last_change_at_ms = now
            reaction.schedule_color_change(choose_color_change_delay(random))

        if (
            not reaction.awaiting_click
            and reaction.pending_color_change_ms is not None
            and now - reaction.last_change_at_ms >= reaction.pending_color_change_ms
        ):
            reaction.start_listening(now)

    def _render(self) -> None:
        self.screen.fill(BLACK)

        countdown_label: Optional[str] = self.state.countdown.remaining_label(
            pygame.time.get_ticks()
        )
        if countdown_label:
            draw_countdown(self.screen, countdown_label)
            pygame.display.flip()
            return

        reaction = self.state.reaction
        if reaction.ready_for_results():
            average = sum(reaction.attempts) / len(reaction.attempts)
            draw_results(self.screen, average)
        else:
            rect_color = reaction.rect_color if reaction.awaiting_click else RECT_DEFAULT
            draw_instruction(self.screen, reaction.rectangle, rect_color, reaction.instruction)

        pygame.display.flip()
