import pygame
import time
from collections import deque
from abc import abstractmethod

from .character import Character
from src.model.game_state import GameState
from src.model.map import Map
from src.model.base_model.character import Direction


# --- ゴーストの基底クラス ---
class Ghost(Character):
    """ゴーストの基底クラス

    Attributes:
        is_scared (bool): ゴーストがいじけているかどうか
        points (int): ゴーストを取得したときのポイント

        direction (Direction): 現在の進行方向
        px (int): ピクセル座標のx位置
        py (int): ピクセル座標のy位置
        size (int): キャラクターのサイズ（ピクセル単位）
        color (tuple[int, int, int]): キャラクターの色を表すRGB値のタプル
        init_cell (tuple[int, int]): ゴーストの初期位置のセル座標
        space (int): キャラクターの描画位置調整
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書
        frame (int): アニメーションのフレーム番号
        last_anim_time (float): 最後にアニメーションを更新した時刻
        anim_interval (float): アニメーションの更新間隔（秒）

        target (tuple[int, int]): ゴーストの移動目標座標
        route (list[Direction]): ゴーストの移動ルートのリスト
    """

    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, speed)

        self.is_scared: bool = False
        self.points: int = points

        self.direction: Direction = Direction.LEFT
        self.px: int = px
        self.py: int = py
        self.size: int = 24
        self.color: tuple[int, int, int] = color
        self.init_cell: tuple[int, int] = (x, y)

        self.space: int = self.size // 2

        self.images: dict[str, pygame.Surface] = {}

        self.frame: int = 1
        self.last_anim_time: float = time.time()
        self.anim_interval: float = 0.15

        self.target: tuple[int, int] = (0, 0)
        self.route: list[Direction] = []

    # 各ゴーストの独自アルゴリズム
    @abstractmethod
    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト

        Returns:
            tuple[int, int]: ゴーストの移動目標座標
        """
        pass

    @abstractmethod
    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        pass

    def update(self, game_state: GameState) -> None:
        """Blinkyの状態を更新する関数。

        セルの中心に到達 -> 自分の座標を更新 -> ターゲットとルートを更新
        -> 次の方向を決定 -> 進行方向に応じて座標を更新 -> アニメーションのフレームを更新

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        # セルの中心に到達したら、現在の座標を確定
        # ターゲットとルートを更新し、次の方向を決定する
        coord = map.is_center(self.px, self.py)
        if coord is not None:
            self.x, self.y = coord
            self.target = self._get_target(game_state)
            self.route = self._get_route(game_state)
            if self.route:
                self.direction = self.route[0]

        if self.direction == Direction.UP:
            self.py -= self.speed
        elif self.direction == Direction.RIGHT:
            self.px += self.speed
        elif self.direction == Direction.DOWN:
            self.py += self.speed
        elif self.direction == Direction.LEFT:
            self.px -= self.speed

        current_time = time.time()
        if self.anim_interval < current_time - self.last_anim_time:
            self.frame = 1 - self.frame
            self.last_anim_time = current_time

    def draw(self, screen: pygame.Surface) -> None:
        """ゴーストを描画する関数。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        key = f"{self.direction}_{self.frame}"
        screen.blit(self.images[key], (self.px - self.space, self.py - self.space))

    def _get_route(self, game_state: GameState) -> list[Direction]:
        """ゴーストの移動ルートを取得する。

        ゴーストの現在位置からターゲットまでの最短経路を探索し、移動ルートを返す。

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト。

        Returns:
            list[Direction]: ゴーストの移動ルートのリスト。
        """
        assert game_state.map is not None
        map: Map = game_state.map

        # start: ゴーストの現在位置、goal: ターゲット(各ゴーストで異なる)の座標
        start = (self.x, self.y)
        goal = self.target
        x, y = start

        # ゴーストの現在位置とターゲットが同じ場合は空のリストを返す
        if start == goal:
            print("========== pin ==========")
            if not map.is_wall(x, y, Direction.UP) and self.direction != Direction.DOWN:
                return [Direction.UP]
            elif not map.is_wall(x, y, Direction.RIGHT) and self.direction != Direction.LEFT:
                return [Direction.RIGHT]
            elif not map.is_wall(x, y, Direction.DOWN) and self.direction != Direction.UP:
                return [Direction.DOWN]
            elif not map.is_wall(x, y, Direction.LEFT) and self.direction != Direction.RIGHT:
                return [Direction.LEFT]

        # 各方向のDirectionと座標の変化量の対応リスト
        moves: list[tuple[Direction, int, int]] = [
            (Direction.UP, 0, -1),
            (Direction.RIGHT, 1, 0),
            (Direction.DOWN, 0, 1),
            (Direction.LEFT, -1, 0)
        ]

        # 各方向の逆を持つ辞書
        reverse_direction: dict[Direction, Direction] = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.RIGHT: Direction.LEFT,
            Direction.LEFT: Direction.RIGHT,
        }

        # キューと訪問済みの座標を保存する
        queue: deque[tuple[int, int]] = deque([start])
        visited: set[tuple[int, int]] = {start}
        # 各座標をキーに、その座標に到達する直前の座標と方向をバリューとして保存
        came_from: dict[tuple[int, int], tuple[Direction, tuple[int, int]]] = {
            (x, y): (self.direction, (x, y))
            }

        while queue:
            current_x, current_y = queue.popleft()
            if (current_x, current_y) == goal:
                break

            for direction, direction_x, direction_y in moves:
                next_x = current_x + direction_x
                next_y = current_y + direction_y
                # マップの範囲外
                if not (0 <= next_x < map.x and 0 <= next_y < map.y):
                    continue
                # 壁がある
                if map.is_wall(current_x, current_y, direction):
                    continue
                # 逆方向への移動を除外
                pre_direction, _ = came_from[(current_x, current_y)]
                if reverse_direction[direction] == pre_direction:
                    continue
                # 訪問済み
                if (next_x, next_y) in visited:
                    continue

                visited.add((next_x, next_y))
                came_from[(next_x, next_y)] = (direction, (current_x, current_y))
                queue.append((next_x, next_y))

        # ゴールに到達できなかった場合は空のリストを返す
        if goal not in came_from:
            return [reverse_direction[self.direction]]

        # ゴールからスタートまでのルートを逆順にたどり、方向のリストを作成する
        route: list[Direction] = []
        current = goal
        while current != start:
            direction, previous = came_from[current]
            route.append(direction)
            current = previous
        route.reverse()

        return route
