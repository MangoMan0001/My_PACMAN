import pygame

from src.model.game_state import GameState
from src.model.base_model.item import Item
from src.model.map import Map


class SuperPacgum(Item):
    """スーパー・パックガムのクラス

    Attributes:
        color (tuple[int, int, int]): スーパー・パックガムの色を表すRGB値のタプル
        size (int): スーパー・パックガムのサイズ（ピクセル単位）
    """
    def __init__(self, x: int, y: int, points: int) -> None:
        super().__init__(x, y, points)
        self.color: tuple[int, int, int] = (0, 0, 255)
        self.size: int = 8

    def update(self, game_state: GameState) -> None:
        """スーパー・パックガムの状態を更新する関数。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.px, self.py = map.cell_center(self.x, self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """スーパー・パックガムを描画する関数。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        if self.is_eaten:
            return
        self._draw_rect(screen, self.color, (self.px - self.size // 2, self.py - self.size // 2,
                                             self.size, self.size))

    def level_up(self, game_state: GameState) -> None:
        """レベルアップ時にスーパー・パックガムをリセットする関数。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        self.is_eaten = False

#    Private functions

    def _draw_rect(self, screen: pygame.Surface, color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
        """指定された矩形領域に色を塗る関数。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
            color (tuple[int, int, int]): 塗る色を表すRGB値のタプル
            rect (tuple[int, int, int, int]): 矩形領域を表す(x, y, width, height)のタプル
        """
        x, y, w, h = rect
        for current_y in range(y, y + h):
            for current_x in range(x, x + w):
                screen.set_at((current_x, current_y), color)
