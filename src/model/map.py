import pygame

from mazegenerator import MazeGenerator
from model.game_state import GameState
from src.model.base_model.entity import Entity


class Map(Entity):
    def __init__(self, level: list[dict[str, int]], seed: int):
        # 16進数や0,1などで構成された壁の配列データ
        self.x: int = level[0]['width']
        self.y: int = level[0]['height']

        self.level: list[dict[str, int]] = level  # config.jsonの中身をgameからもらう
        self.current_level: int = 0
        self.seed: int = seed

        self.generater: MazeGenerator = MazeGenerator((self.x, self.y), perfect=False, seed=42)

        self.wall_map: list[list[int]] = self.generater.maze  # 各要素16進数で各方向の壁の有無がリストで記録される

    def update(self, game_state: GameState) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """mapのみを画面に描画する"""
        pass

    def is_wall(self, x: int, y: int) -> bool:
        """指定された座標が壁かどうかを判定する"""
        return True

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理"""
        self.current_level += 1
        self.width = self.level[self.current_level]['width']
        self.height = self.level[self.current_level]['height']

        self.generate = MazeGenerator((self.x, self.y), perfect=False, seed=self.seed)

        self.wall_map = self.generate.maze
        pass

#    Private functions
