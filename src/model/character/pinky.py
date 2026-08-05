import pygame

from src.model.game_state import GameState
from src.model.base_model.ghost import Ghost
from src.model.base_model.character import Direction
from src.model.map import Map


# --- 「パックマンが今向いている方向の、4マス先の座標」を狙って移動
class Pinky(Ghost):
    """GhostのPinkyを表すクラス。
    追いかけるターゲットは「パックマンが今向いている方向の、4マス先の座標」。

    Attributes:
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書
    """
    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, px, py, speed, color, points)
        self.direction = Direction.LEFT

        for direction in Direction:
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"assets/ghost/ghost_pinky_{key}.png")

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.init_cell = (map.x - 1, 0)
        self.x, self.y = self.init_cell
        self.px, self.py = map.cell_center(self.x, self.y)
        self.direction = Direction.LEFT

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
