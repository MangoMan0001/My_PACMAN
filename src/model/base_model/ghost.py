from abc import abstractmethod

from character import Character
from model.game_state import GameState


# --- ゴーストとその派生 ---
class Ghost(Character):
    def __init__(self, x: int, y: int, speed: int, points: int) -> None:
        super().__init__(x, y, speed)
        self.is_scared: bool = False  # いじけてるかどうか
        self.target: tuple[int, int] = (0, 0)  # 移動目標座標
        self.points: int = points  # 取得時のポイント

    # 各ゴーストの独自アルゴリズム
    @abstractmethod
    def _get_target(self, game_state: GameState) -> None:
        pass
