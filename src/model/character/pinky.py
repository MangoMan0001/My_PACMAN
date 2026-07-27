import pygame

from model.game_state import GameState
from src.model.base_model.ghost import Ghost


# --- 「パックマンが今向いている方向の、4マス先の座標」を狙って移動
class Pinky(Ghost):
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
