"""blinkyクラス."""
import pygame
from pathlib import Path

from src.model.game_state import GameState
from src.model.base_model.ghost import Ghost, GhostMode
from src.model.base_model.character import Direction
from src.model.map import Map


class Blinky(Ghost):
    """GhostのBlinkyを表すクラス.

    Blinky、アカベエ、追いかけ、shadow、つきまとうキャラクター。

    Attributes:
        direction (Direction): ゴーストの現在の移動方向
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書。
    """
    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        """blinkyクラスのコンストラクタ."""
        super().__init__(x, y, px, py, speed, color, points)
        self.direction = Direction.RIGHT

        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        for direction in Direction:
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"{asset_root}/ghost/ghost_blinky_{key}.png")

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理.

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト。
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.init_cell = (0, 0)
        self.x, self.y = self.init_cell
        self.px, self.py = map.cell_center(self.x, self.y)
        self.direction = Direction.RIGHT
        self.current_mode = GhostMode.CHASE
        self.cooltimer = 0.0
        self.blinking_time = 0.0
        self.is_drawable = True

    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する.

        現在のパックマンがいるマスの座標を目指して移動する。

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト。

        Returns:
            tuple[int, int]: ゴーストの移動目標座標。
        """
        pacman = game_state.pacman
        assert pacman is not None

        if self.current_mode != GhostMode.CHASE:
            return self.init_cell
        return (pacman.x, pacman.y)
