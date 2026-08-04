import pygame
import time

from src.model.game_state import GameState
from src.model.map import Map
from src.model.base_model.ghost import Ghost
from src.model.base_model.character import Direction


# --- 「パックマンが今向いている方向の、4マス先の座標」を狙って移動
class Pinky(Ghost):
    """GhostのPinkyを表すクラス。
    追いかけるターゲットは「パックマンが今向いている方向の、4マス先の座標」。

    Attributes:
        direction (Direction): 現在の進行方向
        px (int): ピクセル座標のx位置
        py (int): ピクセル座標のy位置
        size (int): キャラクターのサイズ（ピクセル単位）
        color (tuple[int, int, int]): キャラクターの色を表すRGB値のタプル
        space (int): キャラクターの描画位置調整
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書
        frame (int): アニメーションのフレーム番号
        last_anim_time (float): 最後にアニメーションを更新した時刻
        anim_interval (float): アニメーションの更新間隔（秒）
    """
    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, speed, points)
        self.direction: Direction = Direction.LEFT  # 現在の進行方向
        self.px: int = px
        self.py: int = py
        self.size: int = 24
        self.color: tuple[int, int, int] = color

        self.space: int = self.size // 2

        self.images: dict[str, pygame.Surface] = {}
        for direction in Direction:
            if direction == Direction.STOP:
                continue
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"assets/ghost/ghost_pinky_{key}.png")

        self.frame: int = 1
        self.last_anim_time: float = time.time()
        self.anim_interval: float = 0.15

    def update(self, game_state: GameState) -> None:
        """Pinkyの状態を更新する関数。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self._get_target(game_state)

        self.px, self.py = map.cell_center(self.x, self.y)

        current_time = time.time()
        if self.anim_interval < current_time - self.last_anim_time:
            self.frame = 1 - self.frame
            self.last_anim_time = current_time

    def draw(self, screen: pygame.Surface) -> None:
        """Pinkyを描画する関数。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        key = f"{self.direction}_{self.frame}"
        screen.blit(self.images[key], (self.px - self.space, self.py - self.space))
        pass

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.x, self.y = map.x - 1, 0
        self.px, self.py = map.cell_center(self.x, self.y)

    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト

        Returns:
            tuple[int, int]: ゴーストの移動目標座標
        """
        self.target = (0, 0)
        pass
