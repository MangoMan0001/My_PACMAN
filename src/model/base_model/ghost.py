from abc import abstractmethod

from .character import Character
from src.model.game_state import GameState


# --- ゴーストの基底クラス ---
class Ghost(Character):
    """ゴーストの基底クラス

    Attributes:
        is_scared (bool): ゴーストがいじけているかどうか
        target (tuple[int, int]): ゴーストの移動目標座標
        points (int): ゴーストを取得したときのポイント
    """
    def __init__(self, x: int, y: int, speed: int, points: int) -> None:
        super().__init__(x, y, speed)
        self.is_scared: bool = False  # いじけてるかどうか
        self.target: tuple[int, int] = (0, 0)  # 移動目標座標
        self.points: int = points  # 取得時のポイント

    # 各ゴーストの独自アルゴリズム
    @abstractmethod
    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト

        Returns:
            tuple[int, int]: ゴーストの移動目標座標
        """
        pass

    @abstractmethod
    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト
        """
        pass
