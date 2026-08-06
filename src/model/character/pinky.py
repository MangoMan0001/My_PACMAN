import pygame

from src.model.game_state import GameState
from src.model.base_model.ghost import Ghost
from src.model.base_model.character import Direction
from src.model.map import Map


class Pinky(Ghost):
    """GhostのPinkyを表すクラス。

    Pinky、ピンキー、待ちぶせ、speedy、素早いキャラクター。

    Attributes:
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書。
    """
    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, px, py, speed, color, points)
        self.direction = Direction.LEFT

        for direction in Direction:
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"assets/ghost/ghost_pinky_{key}.png")

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト。
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.init_cell = (map.x - 1, 0)
        self.x, self.y = self.init_cell
        self.px, self.py = map.cell_center(self.x, self.y)
        self.direction = Direction.LEFT

    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する。

        パックマンが今向いている方向の、4マス先の座標を狙って移動する。

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト。

        Returns:
            tuple[int, int]: ゴーストの移動目標座標。
        """
        assert game_state.map is not None
        map: Map = game_state.map
        pacman = game_state.pacman
        assert pacman is not None

        # Direction: 目標座標のズレ
        offset: dict[Direction, tuple[int, int]] = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
        }
        # パックマンが向いている方向からズレる値を取得
        offset_x, offset_y = offset.get(pacman.direction, (0, 0))
        # pinkyの目標座標は4マス先か、マップ外ならマップ内の端に設定
        target_x = max(0, min(map.x - 1, pacman.x + offset_x * 4))
        target_y = max(0, min(map.y - 1, pacman.y + offset_y * 4))

        return (target_x, target_y)
