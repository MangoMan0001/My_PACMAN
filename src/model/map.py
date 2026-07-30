import pygame
from typing import Literal

from mazegenerator import MazeGenerator
from src.model.game_state import GameState
from src.model.base_model.entity import Entity

DIRECTION = Literal['ABOVE', 'RIGHT', 'BOTTOM', 'LEFT']


class Map(Entity):
    def __init__(self, game_state: GameState, screen: pygame.Surface):
        # 16進数や0,1などで構成された壁の配列データ
        self.x: int = game_state.config.level[0].width
        self.y: int = game_state.config.level[0].height

        self.generater: MazeGenerator = MazeGenerator((self.x, self.y), perfect=False, seed=42)

        self.wall_map: list[list[int]] = self.generater.maze  # 各要素16進数で各方向の壁の有無がリストで記録される

        self.area_size: int = 32
        self.wall_size: int = 1
        self.wall_color: tuple[int, int, int] = (255, 255, 255)

        self.map_len_x = self.x * self.area_size + self.wall_size
        self.map_len_y = self.y * self.area_size + self.wall_size

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.space_x = self.screen_width // 2 - self.map_len_x // 2
        self.space_y = self.screen_height // 2 - self.map_len_y // 2

    def update(self, game_state: GameState) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """mapのみを画面に描画する"""

        self.space_x = screen.get_width() // 2 - self.map_len_x // 2
        self.space_y = screen.get_height() // 2 - self.map_len_y // 2
        pygame.draw.rect(screen, self.wall_color, (self.space_x, self.space_y, self.map_len_x, self.wall_size))
        pygame.draw.rect(screen, self.wall_color, (self.space_x, self.space_y, self.wall_size, self.map_len_y))

        for y, line in enumerate(self.wall_map):
            for x, cell in enumerate(line):
                px = x * self.area_size + self.space_x
                py = y * self.area_size + self.space_y

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

    def is_wall(self, x: int, y: int, direction: DIRECTION) -> bool:
        """指定された座標が壁かどうかを判定する"""
        cell = self.wall_map[y][x]
        if direction == 'ABOVE':
            return bool(cell & 1)
        elif direction == 'RIGHT':
            return bool(cell & 2)
        elif direction == 'BOTTOM':
            return bool(cell & 4)
        elif direction == 'LEFT':
            return bool(cell & 8)
        return False

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理"""
        if len(game_state.config.level) <= game_state.current_level:
            return
        self.x = game_state.config.level[game_state.current_level].width
        self.y = game_state.config.level[game_state.current_level].height

        self.generate = MazeGenerator((self.x, self.y), perfect=False, seed=game_state.config.seed)

        self.wall_map = self.generate.maze

        self.map_len_x = self.x * self.area_size + self.wall_size
        self.map_len_y = self.y * self.area_size + self.wall_size

        self.space_x = self.screen_width // 2 - self.map_len_x // 2
        self.space_y = self.screen_height // 2 - self.map_len_y // 2

    def area_center(self, x: int, y: int) -> tuple[int, int]:
        """指定された座標の位置をピクセルで返す"""
        base_x = self.space_x + x * self.area_size
        base_y = self.space_y + y * self.area_size

        # 通路の開始位置(base_x + wall_size) ＋ 通路の幅の半分((area_size - wall_size) // 2)
        px = base_x + self.wall_size + (self.area_size - self.wall_size) // 2
        py = base_y + self.wall_size + (self.area_size - self.wall_size) // 2
        return (px, py)

#    Private functions
