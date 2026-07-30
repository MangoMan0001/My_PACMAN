import pygame

from src.model.game_state import GameState
from src.model.base_model.item import Item


class Pacgum(Item):
    def __init__(self, x: int, y: int, points: int) -> None:
        super().__init__(x, y, points)
        self.px: int = 0
        self.py: int = 0

    def update(self, game_state: GameState) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_eaten:
            return
