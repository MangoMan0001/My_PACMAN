import pygame

from src.model.game_state import GameState
from src.model.base_model.ghost import Ghost
from src.model.base_model.character import Direction


# --- パックマンとの距離が「8マス以上」離れている時はBlinkyと同じ 「8マス以内」に近づくと自分の初期位置をターゲットにする
class Clyde(Ghost):
    """GhostのClydeを表すクラス。
    追いかけるターゲットは「パックマンとの距離が「8マス以上」離れている時はBlinkyと同じ 「8マス以内」に近づくと自分の初期位置をターゲットにする」。

    Attributes:
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書
    """
    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, px, py, speed, color, points)

        for direction in Direction:
            if direction == Direction.STOP:
                continue
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"assets/ghost/ghost_clyde_{key}.png")

    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト

        Returns:
            tuple[int, int]: ゴーストの移動目標座標
        """
        pacman = game_state.pacman
        assert pacman is not None

        return (pacman.x, pacman.y)
