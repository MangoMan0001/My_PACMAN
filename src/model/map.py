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

        self.map_len_x = self.x * (self.area_size + self.wall_size) + self.wall_size
        self.map_len_y = self.y * (self.area_size + self.wall_size) + self.wall_size

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.space_x = self.screen_width // 2 - self.map_len_x // 2
        self.space_y = self.screen_height // 2 - self.map_len_y // 2

    def update(self, game_state: GameState) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """mapのみを画面に描画する"""
        self._draw_rect(screen, self.wall_color, (self.space_x, self.space_y, self.map_len_x, self.wall_size))
        self._draw_rect(screen, self.wall_color, (self.space_x, self.space_y, self.wall_size, self.map_len_y))

        for y, line in enumerate(self.wall_map):
            for x, cell in enumerate(line):
                px = self.space_x + x * (self.area_size + self.wall_size) + self.wall_size
                py = self.space_y + y * (self.area_size + self.wall_size) + self.wall_size

                # # above
                # if cell & 1:
                #     self._draw_rect(screen, self.wall_color, (px, py, self.area_size, self.wall_size))
                # right
                if cell & 2:
                    self._draw_rect(screen, self.wall_color, (px + self.area_size, py,
                                                              self.wall_size, self.area_size + self.wall_size))

                # # bottom
                if cell & 4:
                    self._draw_rect(screen, self.wall_color, (px, py + self.area_size,
                                                              self.area_size + self.wall_size, self.wall_size))
                # # left
                # if cell & 8:
                #     self._draw_rect(screen, self.wall_color, (px, py, self.wall_size, self.area_size))

                if cell == 15:
                    self._draw_rect(screen, (0, 0, 255), (px,
                                                          py,
                                                          self.area_size,
                                                          self.area_size))

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

        self.map_len_x = self.x * (self.area_size + self.wall_size) + self.wall_size
        self.map_len_y = self.y * (self.area_size + self.wall_size) + self.wall_size

        self.space_x = self.screen_width // 2 - self.map_len_x // 2
        self.space_y = self.screen_height // 2 - self.map_len_y // 2

    def area_center(self, x: int, y: int) -> tuple[int, int]:
        """指定された座標の位置をピクセルで返す"""
        base_x = self.space_x + x * (self.area_size + self.wall_size) + self.wall_size
        base_y = self.space_y + y * (self.area_size + self.wall_size) + self.wall_size

        # 通路の開始位置(base_x)  ＋ 通路の幅の半分((area_size - wall_size) // 2)
        px = base_x + self.area_size // 2
        py = base_y + self.area_size // 2
        return (px, py)

    def area_coorner(self, x: int, y: int) -> tuple[int, int]:
        base_x = self.space_x + x * (self.area_size + self.wall_size) + self.wall_size
        base_y = self.space_y + y * (self.area_size + self.wall_size) + self.wall_size

        return (base_x, base_y)

#   Pacman method
    def init_area_pacman(self) -> tuple[int, int]:
        """PACMANが生成される初期座標の位置を返す"""
        x = self.x // 2
        y = self.y // 2

        return (x, y)

#    Private functions

    def _draw_rect(self, screen: pygame.Surface, color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
        x, y, w, h = rect
        for current_y in range(y, y + h):
            for current_x in range(x, x + w):
                screen.set_at((current_x, current_y), color)
