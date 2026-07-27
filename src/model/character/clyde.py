import pygame

from model.game_state import GameState
from src.model.base_model.ghost import Ghost


# --- パックマンとの距離が「8マス以上」離れている時はBlinkyと同じ 「8マス以内」に近づくと自分の初期位置をターゲットにする
class Clyde(Ghost):
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
