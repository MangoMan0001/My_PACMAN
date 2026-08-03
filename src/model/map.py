import pygame

from mazegenerator import MazeGenerator
from src.model.game_state import GameState
from src.model.base_model.entity import Entity
from src.model.base_model.character import Direction


class Map(Entity):
    def __init__(self, game_state: GameState, screen: pygame.Surface):
        # 16進数や0,1などで構成された壁の配列データ
        self.x: int = game_state.config.level[0].width
        self.y: int = game_state.config.level[0].height

        self.generater: MazeGenerator = MazeGenerator((self.x, self.y), perfect=False, seed=42)

        self.wall_map: list[list[int]] = self.generater.maze  # 各要素16進数で各方向の壁の有無がリストで記録される

        self.area_size: int = 32
        self.wall_size: int = 2
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

                # # up
                # if cell & 1:
                #     self._draw_rect(screen, self.wall_color, (px, py, self.area_size, self.wall_size))
                # right
                if cell & 2:
                    self._draw_rect(screen, self.wall_color, (px + self.area_size, py - self.wall_size,
                                                              self.wall_size, self.area_size + self.wall_size * 2))

                # # down
                if cell & 4:
                    self._draw_rect(screen, self.wall_color, (px - self.wall_size, py + self.area_size,
                                                              self.area_size + self.wall_size * 2, self.wall_size))
                # # left
                # if cell & 8:
                #     self._draw_rect(screen, self.wall_color, (px, py, self.wall_size, self.area_size))

                if cell == 15:
                    self._draw_rect(screen, (0, 0, 255), (px,
                                                          py,
                                                          self.area_size,
                                                          self.area_size))

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
        """指定された座標の位置をピクセル座標で返す"""
        base_x = self.space_x + x * (self.area_size + self.wall_size) + self.wall_size
        base_y = self.space_y + y * (self.area_size + self.wall_size) + self.wall_size

        # 通路の開始位置(base_x)  ＋ 通路の幅の半分((area_size - wall_size) // 2)
        px = base_x + self.area_size // 2
        py = base_y + self.area_size // 2
        return (px, py)

    def area_coorner(self, x: int, y: int) -> tuple[int, int]:
        """セル内の左上のピクセル座標を返す"""
        base_x = self.space_x + x * (self.area_size + self.wall_size) + self.wall_size
        base_y = self.space_y + y * (self.area_size + self.wall_size) + self.wall_size

        return (base_x, base_y)

    def is_moveable(self, x: int, y: int, px: int, py: int, direction: Direction) -> bool:
        """指定された方向に移動できるかを判定する"""
        center = self.is_center(px, py)
        cx, cy = self.area_center(x, y)
        cell = self.wall_map[y][x]
        if direction == Direction.UP:
            if center is None:
                return px == cx
            else:
                return not bool(cell & 1)
        elif direction == Direction.RIGHT:
            if center is None:
                print(px == cx)
                return py == cy
            else:
                return not bool(cell & 2)
        elif direction == Direction.DOWN:
            if center is None:
                return px == cx
            else:
                return not bool(cell & 4)
        elif direction == Direction.LEFT:
            if center is None:
                print(px == cx)
                return py == cy
            else:
                return not bool(cell & 8)
        return False

    def is_center(self, px: int, py: int) -> tuple[int, int] | None:
        """指定されたピクセル座標が位置するセル内の中心か判定。真の場合はセル座標、偽の場合はNoneを返す。"""
        x, y = self._get_area(px, py)
        center = self.area_center(x, y)
        # print((x, y), (px - self.space_x, py - self.space_y), (px, py), center)
        if (px, py) == center:
            # print('center')
            return (x, y)
        else:
            # print('None')
            return None

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

    def _get_area(self, px: int, py: int) -> tuple[int, int]:
        x = (px - self.space_x) // (self.area_size + self.wall_size)
        y = (py - self.space_y) // (self.area_size + self.wall_size)

        return (x, y)
