import pygame

from src.model.game_state import GameState
from src.model.base_model.ghost import Ghost
from src.model.base_model.character import Direction
from src.model.map import Map


# --- パックマンの位置と、赤ゴースト（Blinky）の位置の両方を使って計算する...?
class Inky(Ghost):
    """GhostのInkyを表すクラス。
    追いかけるターゲットは「パックマンの位置と、赤ゴースト（Blinky）の位置の両方から挟み込むように移動する」。

    Attributes:
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書
    """
    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, px, py, speed, color, points)
        self.direction = Direction.RIGHT

        for direction in Direction:
            # if direction == Direction.STOP:
            #     continue
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"assets/ghost/ghost_inky_{key}.png")

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.init_cell = (0, map.y - 1)
        self.x, self.y = self.init_cell
        self.px, self.py = map.cell_center(self.x, self.y)
        self.direction = Direction.RIGHT

    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト

        Returns:
            tuple[int, int]: ゴーストの移動目標座標
        """
        assert game_state.map is not None
        map: Map = game_state.map
        pacman = game_state.pacman
        assert pacman is not None
        blinky = game_state.ghosts[0]
        assert blinky is not None

        # --- パックマンの位置と、赤ゴースト（Blinky）の位置の両方を使って計算する...?
        offset: dict[Direction, tuple[int, int]] = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
        }
        offset_x, offset_y = offset.get(pacman.direction, (0, 0))
        target_x = max(0, min(map.x - 1, pacman.x + (pacman.x - blinky.x)))
        target_y = max(0, min(map.y - 1, pacman.y + (pacman.y - blinky.y)))

        while map.is_reachable(target_x, target_y) is False:
            print("Inky入れた入れた入れた入れた入れた入れた入れた入れた")
            if pacman.direction == Direction.LEFT or pacman.direction == Direction.RIGHT:
                if target_x > pacman.x:
                    target_x -= 1
                elif target_x < pacman.x:
                    target_x += 1
            if pacman.direction == Direction.UP or pacman.direction == Direction.DOWN:
                if target_y > pacman.y:
                    target_y -= 1
                elif target_y < pacman.y:
                    target_y += 1

        return (target_x, target_y)
