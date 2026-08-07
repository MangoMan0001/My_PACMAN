import pygame

from src.model.game_state import GameState
from src.model.base_model.ghost import Ghost, GhostMode
from src.model.base_model.character import Direction
from src.model.map import Map


class Clyde(Ghost):
    """GhostのClydeを表すクラス。

    Clyde、グズタ、おとぼけ、pokey、のろまなキャラクター。

    Attributes:
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書。
    """
    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, px, py, speed, color, points)
        self.direction = Direction.LEFT

        for direction in Direction:
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"assets/ghost/ghost_clyde_{key}.png")

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト。
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.init_cell = (map.x - 1, map.y - 1)
        self.x, self.y = self.init_cell
        self.px, self.py = map.cell_center(self.x, self.y)
        self.direction = Direction.LEFT
        self.current_mode = GhostMode.CHASE

    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する。

        パックマンとの距離によってターゲットが変わる。
        「8マス以上」離れている時はBlinkyと同じくパックマンをターゲットにする。
        「8マス以内」に近づくと自分の初期位置をターゲットにする。

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト。

        Returns:
            tuple[int, int]: ゴーストの移動目標座標。
        """
        pacman = game_state.pacman
        assert pacman is not None

        if self.current_mode != GhostMode.CHASE:
            return self.init_cell

        # パックマンとの距離を計算 ((x2 - x1)^2 + (y2 - y1)^2)の平方根なしで比較
        distance_x = self.x - pacman.x
        distance_y = self.y - pacman.y
        distance = distance_x ** 2 + distance_y ** 2

        # 8マス以上離れている場合はパックマンをターゲットにする
        if distance >= 8 ** 2:
            return (pacman.x, pacman.y)

        # 8マス以内に近づいた場合は自分の初期位置をターゲットにする
        return (self.init_cell[0], self.init_cell[1])
