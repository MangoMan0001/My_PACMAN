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

        self.area_size: int = 64
        self.wall_size: int = 1
        self.wall_color: tuple[int, int, int] = (255, 255, 255)
        self.space: int = 40

        self.remake_screen: bool = True

    def update(self, game_state: GameState) -> None:
        if self.remake_screen:
            game_state.screen = pygame.display.set_mode((self.x * self.area_size + self.space * 2,
                                                         self.y * self.area_size + self.space * 2))
            self.remake_screen = False
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """mapのみを画面に描画する"""

        map_len = self.x * self.area_size + self.wall_size
        pygame.draw.rect(screen, self.wall_color, (self.space, self.space, map_len, self.wall_size))
        pygame.draw.rect(screen, self.wall_color, (self.space, self.space, self.wall_size, map_len))

        for y, line in enumerate(self.wall_map):
            for x, cell in enumerate(line):
                px = x * self.area_size + self.space
                py = y * self.area_size + self.space

                # # above
                # if cell & 1:
                #     pygame.draw.rect(screen, self.wall_color, (px, py, self.area_size, self.wall_size))
                # right
                if cell & 2:
                    pygame.draw.rect(screen, self.wall_color, (px + self.area_size, py,
                                                               self.wall_size, self.area_size))

                # # bottom
                if cell & 4:
                    pygame.draw.rect(screen, self.wall_color, (px, py + self.area_size,
                                                               self.area_size, self.wall_size))
                # # left
                # if cell & 8:
                #     pygame.draw.rect(screen, self.wall_color, (px, py, self.wall_size, self.area_size))

                if cell == 15:
                    pygame.draw.rect(screen, (0, 0, 255), (px + self.wall_size,
                                                           py + self.wall_size,
                                                           self.area_size - self.wall_size,
                                                           self.area_size - self.wall_size))

    def is_wall(self, x: int, y: int) -> bool:
        """指定された座標が壁かどうかを判定する"""
        return True

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理"""
        self.x = game_state.config.level[game_state.current_level].width
        self.y = game_state.config.level[game_state.current_level].height

        self.generate = MazeGenerator((self.x, self.y), perfect=False, seed=game_state.config.seed)

        self.wall_map = self.generate.maze
        self.remake_screen = True
        pass

#    Private functions
