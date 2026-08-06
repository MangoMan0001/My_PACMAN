import pygame

from mazegenerator import MazeGenerator
from src.model.game_state import GameState
from src.model.base_model.entity import Entity
from src.model.base_model.character import Direction


class Map(Entity):
    """ゲームのマップを管理するクラス。

    Attributes:
        x (int): セル単位でのx座標
        y (int): セル単位でのy座標
        generater (MazeGenerator): 迷路生成器のインスタンス
        wall_map (list[list[int]]): 壁の配置を表す2次元リスト。各要素は16進数で各方向の壁の有無を表す。
        cell_size (int): セルのサイズ（ピクセル単位）
        wall_size (int): 壁のサイズ（ピクセル単位）
        wall_color (tuple[int, int, int]): 壁の色（RGB）
        map_len_x (int): マップの幅（ピクセル単位）
        map_len_y (int): マップの高さ（ピクセル単位）
        screen_width (int): 画面の幅（ピクセル単位）
        screen_height (int): 画面の高さ（ピクセル単位）
        space_x (int): マップの描画開始位置のx座標（ピクセル単位）
        space_y (int): マップの描画開始位置のy座標（ピクセル単位）
    """
    def __init__(self, game_state: GameState, screen: pygame.Surface):
        # 16進数や0,1などで構成された壁の配列データ
        self.x: int = game_state.config.level[0].width
        self.y: int = game_state.config.level[0].height

        self.generater: MazeGenerator = MazeGenerator((self.x, self.y), perfect=False, seed=42)

        self.wall_map: list[list[int]] = self.generater.maze  # 各要素16進数で各方向の壁の有無がリストで記録される

        self.cell_size: int = 32
        self.wall_size: int = 2
        self.wall_color: tuple[int, int, int] = (255, 255, 255)

        self.map_len_x = self.x * (self.cell_size + self.wall_size) + self.wall_size
        self.map_len_y = self.y * (self.cell_size + self.wall_size) + self.wall_size

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.space_x = self.screen_width // 2 - self.map_len_x // 2
        self.space_y = self.screen_height // 2 - self.map_len_y // 2

    def update(self, game_state: GameState) -> None:
        """マップの状態を更新する関数。現在は何も行わない"""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """マップを描画する関数。

        Args:
            screen (pygame.Surface): 描画先のpygame.Surfaceオブジェクト。
        """
        self._draw_rect(screen, self.wall_color, (self.space_x, self.space_y, self.map_len_x, self.wall_size))
        self._draw_rect(screen, self.wall_color, (self.space_x, self.space_y, self.wall_size, self.map_len_y))

        for y, line in enumerate(self.wall_map):
            for x, cell in enumerate(line):
                px = self.space_x + x * (self.cell_size + self.wall_size) + self.wall_size
                py = self.space_y + y * (self.cell_size + self.wall_size) + self.wall_size

                # # up
                # if cell & 1:
                #     self._draw_rect(screen, self.wall_color, (px, py, self.cell_size, self.wall_size))
                # right
                if cell & 2:
                    self._draw_rect(screen, self.wall_color, (px + self.cell_size, py - self.wall_size,
                                                              self.wall_size, self.cell_size + self.wall_size * 2))

                # # down
                if cell & 4:
                    self._draw_rect(screen, self.wall_color, (px - self.wall_size, py + self.cell_size,
                                                              self.cell_size + self.wall_size * 2, self.wall_size))
                # # left
                # if cell & 8:
                #     self._draw_rect(screen, self.wall_color, (px, py, self.wall_size, self.cell_size))

                if cell == 15:
                    self._draw_rect(screen, (0, 0, 255), (px,
                                                          py,
                                                          self.cell_size,
                                                          self.cell_size))

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        if len(game_state.config.level) <= game_state.current_level:
            return
        self.x = game_state.config.level[game_state.current_level].width
        self.y = game_state.config.level[game_state.current_level].height

        self.generate = MazeGenerator((self.x, self.y), perfect=False, seed=game_state.config.seed)

        self.wall_map = self.generate.maze

        self.map_len_x = self.x * (self.cell_size + self.wall_size) + self.wall_size
        self.map_len_y = self.y * (self.cell_size + self.wall_size) + self.wall_size

        self.space_x = self.screen_width // 2 - self.map_len_x // 2
        self.space_y = self.screen_height // 2 - self.map_len_y // 2

    def cell_center(self, x: int, y: int) -> tuple[int, int]:
        """セル内の中心のピクセル座標を返す

        Args:
            x (int): セル単位でのx座標
            y (int): セル単位でのy座標

        Returns:
            tuple[int, int]: セル内の中心のピクセル座標 (px, py)
        """
        base_x = self.space_x + x * (self.cell_size + self.wall_size) + self.wall_size
        base_y = self.space_y + y * (self.cell_size + self.wall_size) + self.wall_size

        px = base_x + self.cell_size // 2
        py = base_y + self.cell_size // 2
        return (px, py)

    def cell_coorner(self, x: int, y: int) -> tuple[int, int]:
        """セルの左上の角のピクセル座標を返す

        Args:
            x (int): セル単位でのx座標
            y (int): セル単位でのy座標

        Returns:
            tuple[int, int]: セルの左上の角のピクセル座標 (px, py)
        """
        base_x = self.space_x + x * (self.cell_size + self.wall_size) + self.wall_size
        base_y = self.space_y + y * (self.cell_size + self.wall_size) + self.wall_size

        return (base_x, base_y)

    def is_moveable(self, x: int, y: int, px: int, py: int, direction: Direction) -> bool:
        """指定されたピクセル座標が位置するセル内で、指定された方向に移動可能か判定する。
        x, yはセル座標、px, pyはピクセル座標。どちらも同一キャラクターの座標である必要がある。

        Args:
            x (int): セル単位でのx座標
            y (int): セル単位でのy座標
            px (int): ピクセル単位でのx座標
            py (int): ピクセル単位でのy座標
            direction (Direction): 移動方向を表すDirection列挙型

        Returns:
            bool: 移動可能な場合はTrue、移動不可能な場合はFalse
        """
        center = self.is_center(px, py)
        cx, cy = self.cell_center(x, y)
        cell = self.wall_map[y][x]
        if direction == Direction.UP:
            if center is None:
                return px == cx
            else:
                return not bool(cell & 1)
        elif direction == Direction.RIGHT:
            if center is None:
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
                return py == cy
            else:
                return not bool(cell & 8)
        return False

    def is_wall(self, x: int, y: int, direction: Direction) -> bool:
        """指定されたセル座標に壁があるか判定する。

        wall_mapの各要素は16進数で各方向の壁の有無を表す。
        壁なら 1: 上、2: 右、4: 下、8: 左 のビットが立っている。

        Args:
            x (int): セル単位でのx座標
            y (int): セル単位でのy座標
            direction (Direction): 判定する方向を表すDirection列挙型

        Returns:
            bool: 壁がある場合はTrue、壁がない(通れる)場合はFalse
        """
        cell = self.wall_map[y][x]
        if direction == Direction.UP:
            return bool(cell & 1)
        elif direction == Direction.RIGHT:
            return bool(cell & 2)
        elif direction == Direction.DOWN:
            return bool(cell & 4)
        elif direction == Direction.LEFT:
            return bool(cell & 8)
        return False

    def is_reachable(self, x: int, y: int) -> bool:
        """指定されたセル座標が中心の42ブロックかどうか判定し、到達可能かどうかを返す。

        Args:
            x (int): セル単位でのx座標
            y (int): セル単位でのy座標

        Returns:
            bool: 到達可能な場合はTrue、到達不可能な場合はFalse
        """
        if x < 0 or x >= self.x or y < 0 or y >= self.y:
            return False
        cell = self.wall_map[y][x]
        return cell != 15

    def is_center(self, px: int, py: int) -> tuple[int, int] | None:
        """指定されたピクセル座標が位置するセル内で、中心にいるか判定する。
        中心にいる場合はそのセルの座標を返し、中心にいない場合はNoneを返す。

        Args:
            px (int): ピクセル単位でのx座標
            py (int): ピクセル単位でのy座標

        Returns:
            tuple[int, int] | None: 中心にいる場合はそのセルの座標 (x, y) を返し、中心にいない場合はNoneを返す
        """
        x, y = self.get_cell(px, py)
        center = self.cell_center(x, y)
        # print((x, y), (px - self.space_x, py - self.space_y), (px, py), center)
        if (px, py) == center:
            # print('center')
            return (x, y)
        else:
            # print('None')
            return None

    def get_cell(self, px: int, py: int) -> tuple[int, int]:
        """指定されたピクセル座標が位置するセルの座標を返す。

        Args:
            px (int): ピクセル単位でのx座標
            py (int): ピクセル単位でのy座標

        Returns:
            tuple[int, int]: セルの座標 (x, y)
        """
        x = (px - self.space_x) // (self.cell_size + self.wall_size)
        y = (py - self.space_y) // (self.cell_size + self.wall_size)

        return (x, y)

#   Pacman method
    def init_area_pacman(self) -> tuple[int, int]:
        """Pacmanの初期位置を返す。

        Returns:
            tuple[int, int]: Pacmanの初期位置のセル座標 (x, y)
        """
        x = self.x // 2
        y = self.y // 2

        return (x, y)

#    Private functions

    def _draw_rect(self, screen: pygame.Surface, color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
        """指定された矩形を描画する。

        Args:
            screen (pygame.Surface): 描画先のpygame.Surfaceオブジェクト
            color (tuple[int, int, int]): 描画する矩形の色（RGB）
            rect (tuple[int, int, int, int]): 描画する矩形の座標とサイズ (x, y, width, height)
        """
        x, y, w, h = rect
        for current_y in range(y, y + h):
            for current_x in range(x, x + w):
                screen.set_at((current_x, current_y), color)
