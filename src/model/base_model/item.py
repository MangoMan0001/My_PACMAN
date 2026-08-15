"""アイテムオブジェクト基底クラス."""
import pygame

from src.model.game_state import GameState
from src.model.base_model.entity import Entity
from src.model.map import Map


# --- アイテムの基底クラス ---
class Item(Entity):
    """アイテムの基底クラス.

    Attributes:
        px (int): アイテムのピクセル単位でのx座標
        py (int): アイテムのピクセル単位でのy座標
        points (int): アイテム取得時のポイント
        color (tuple[int, int, int]): アイテムの色（RGB）
        size (int): アイテムのサイズ（ピクセル単位）
        is_eaten (bool): アイテムが食べられたかどうかを示すフラグ
    """
    def __init__(self, x: int, y: int, points: int, color: tuple[int, int, int], size: int) -> None:
        super().__init__(x, y)
        self.px: int = 0
        self.py: int = 0
        self.points: int = points  # 取得時のポイント
        self.color: tuple[int, int, int] = color
        self.size: int = size

        self.is_eaten: bool = False  # 食べられているか

    def update(self, game_state: GameState) -> None:
        """パックガムの状態を更新する関数.

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.px, self.py = map.cell_center(self.x, self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """パックガムを描画する関数.

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        if self.is_eaten:
            return
        self._draw_rect(screen, self.color, (self.px - self.size // 2, self.py - self.size // 2,
                                             self.size, self.size))

    def level_up(self, game_state: GameState) -> None:
        """レベルアップ時にパックガムをリセットする関数.

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        self.is_eaten = False

#    Private functions

    def _draw_rect(self, screen: pygame.Surface, color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
        """指定された矩形領域に色を塗る関数.

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
            color (tuple[int, int, int]): 塗る色を表すRGB値のタプル
            rect (tuple[int, int, int, int]): 矩形領域を表す(x, y, width, height)のタプル
        """
        x, y, w, h = rect
        for current_y in range(y, y + h):
            for current_x in range(x, x + w):
                screen.set_at((current_x, current_y), color)
