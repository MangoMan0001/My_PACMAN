import pygame

from model.game_state import GameState
from src.model.base_model.ghost import Ghost


# --- 「現在のパックマンがいるマスの座標」に最短距離で向かう
class Blinky(Ghost):
    def __init__(self, x: int, y: int, speed: int, color: str) -> None:
        super().__init__(x, y, speed)
        self.color: str = color

    def update(self, game_state: GameState) -> None:
        self._get_target(game_state)
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def _get_target(self, game_state: GameState) -> None:
        self.target = (0, 0)
        pass
