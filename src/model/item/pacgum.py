import pygame

from src.model.game_state import GameState
from src.model.base_model.item import Item
from src.model.map import Map


class Pacgum(Item):
    def __init__(self, x: int, y: int, points: int) -> None:
        super().__init__(x, y, points)
        self.color: tuple[int, int, int] = (0, 255, 255)
        self.size: int = 6

    def update(self, game_state: GameState) -> None:
        assert game_state.map is not None
        map: Map = game_state.map

        self.px, self.py = map.area_center(self.x, self.y)

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_eaten:
            return
        self._draw_rect(screen, self.color, (self.px - self.size // 2, self.py - self.size // 2,
                                             self.size, self.size))

    def level_up(self, game_state: GameState) -> None:
        self.is_eaten = False

#    Private functions

    def _draw_rect(self, screen: pygame.Surface, color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
        x, y, w, h = rect
        for current_y in range(y, y + h):
            for current_x in range(x, x + w):
                screen.set_at((current_x, current_y), color)
