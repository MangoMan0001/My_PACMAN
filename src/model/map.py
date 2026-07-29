import pygame

from mazegenerator import MazeGenerator
from src.model.game_state import GameState
from src.model.base_model.config_model import LevelModel
from src.model.base_model.entity import Entity


class Map(Entity):
    def __init__(self, game_state: GameState):
        # 16進数や0,1などで構成された壁の配列データ
        self.x: int = game_state.config.level[0].width
        self.y: int = game_state.config.level[0].height

        self.generater: MazeGenerator = MazeGenerator((self.x, self.y), perfect=False, seed=42)

        self.wall_map: list[list[int]] = self.generater.maze  # 各要素16進数で各方向の壁の有無がリストで記録される

        self.area_size: int = 32
        self.wall_size: int = 4
        self.wall_color: tuple[int, int, int] = (33, 33, 235)

    def update(self, game_state: GameState) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """mapのみを画面に描画する"""

        for y, line in enumerate(self.wall_map):
            for x, cell in enumerate(line):
                px = x * self.area_size
                py = y * self.area_size

                if cell & 8:
                    pygame.draw.rect(screen, self.wall_color, (px, py, self.area_size, self.wall_size))

    def is_wall(self, x: int, y: int) -> bool:
        """指定された座標が壁かどうかを判定する"""
        return True

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理"""
        self.x = game_state.config.level[game_state.current_level].width
        self.y = game_state.config.level[game_state.current_level].height

        self.generate = MazeGenerator((self.x, self.y), perfect=False, seed=game_state.config.seed)

        self.wall_map = self.generate.maze
        pass

#    Private functions
