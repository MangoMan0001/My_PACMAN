import pygame

from src.model.game_state import GameState
from src.model.base_model.item import Item
from src.model.map import Map


class SuperPacgum(Item):
    def __init__(self, x: int, y: int, points: int) -> None:
        super().__init__(x, y, points)
        self.px: int = 0
        self.py: int = 0

    def update(self, game_state: GameState) -> None:
        assert game_state.map is not None
        map: Map = game_state.map

        self.px, self.py = map.area_center(self.x, self.y)

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_eaten:
            return
        pygame.draw.rect(screen, (255, 0, 0), (self.px - 3, self.py - 3, 6, 6))
