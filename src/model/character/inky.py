import pygame

from src.model.game_state import GameState
from src.model.base_model.ghost import Ghost, GhostMode
from src.model.base_model.character import Direction
from src.model.map import Map
from src.model.character.blinky import Blinky


class Inky(Ghost):
    """GhostのInkyを表すクラス。

    Inky、アオスケ、きまぐれ、bashful、恥ずかしがりのキャラクター。

    Attributes:
        direction (Direction): ゴーストの現在の移動方向
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書。
    """
    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, px, py, speed, color, points)
        self.direction = Direction.RIGHT

        for direction in Direction:
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"data/assets/ghost/ghost_inky_{key}.png")

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト。
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.init_cell = (0, map.y - 1)
        self.x, self.y = self.init_cell
        self.px, self.py = map.cell_center(self.x, self.y)
        self.direction = Direction.RIGHT
        self.current_mode = GhostMode.CHASE

    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する。

        パックマンの向きから2個先の位置と、赤ゴースト（Blinky）の位置の両方を使って計算する。

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト。

        Returns:
            tuple[int, int]: ゴーストの移動目標座標。
        """
        assert game_state.map is not None
        map: Map = game_state.map
        pacman = game_state.pacman
        assert pacman is not None

        if self.current_mode != GhostMode.CHASE:
            return self.init_cell

        # blinkyを探し、見つからなければパックマンの位置を目標座標として返す
        blinky: Ghost | None = None
        for ghost in game_state.ghosts:
            if isinstance(ghost, Blinky):
                blinky = ghost
                break
        if blinky is None:
            return (pacman.x, pacman.y)
        assert blinky is not None

        # Direction: 目標座標のズレ
        offset: dict[Direction, tuple[int, int]] = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
        }
        # パックマンが向いている方向からズレる値を取得
        offset_x, offset_y = offset.get(pacman.direction, (0, 0))

        # パックマンの位置から2マス先の座標を計算
        pacman_x = pacman.x + offset_x * 2
        pacman_y = pacman.y + offset_y * 2

        # マップの端とターゲットで近い方を採用
        target_x = max(0, min(map.x - 1, pacman_x + (pacman_x - blinky.x)))
        target_y = max(0, min(map.y - 1, pacman_y + (pacman_y - blinky.y)))

        return (target_x, target_y)
