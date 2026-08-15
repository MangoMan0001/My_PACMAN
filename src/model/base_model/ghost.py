"""ゴーストオブジェクト基底クラス."""
import pygame
from collections import deque
from abc import abstractmethod
from enum import Enum, auto
from pathlib import Path

from .character import Character
from src.model.game_state import GameState
from src.model.map import Map
from src.model.base_model.character import Direction


class GhostMode(Enum):
    """ゴーストの状態を表す列挙型.

    Attributes:
        CHASE (auto): 追跡状態
        SCATTER (auto): 縄張り状態
        SCARED (auto): いじけ状態
        EATEN (auto): 捕食後状態
    """
    CHASE = auto()
    SCATTER = auto()
    SCARED = auto()
    EATEN = auto()
    READY = auto()


# --- ゴーストの基底クラス ---
class Ghost(Character):
    """ゴーストの基底クラス.

    Attributes:
        points (int): ゴーストを捕食した時のポイント
        current_mode (GhostMode): ゴーストの現在の状態
        mode_time (dict[GhostMode, int]): 各状態の持続時間を保持する辞書
        mode_timer (float): 現在の状態の経過時間
        direction (Direction): ゴーストの現在の移動方向
        px (int): ゴーストのピクセル単位でのx座標
        py (int): ゴーストのピクセル単位でのy座標
        size (int): ゴーストのサイズ（ピクセル単位）
        color (tuple[int, int, int]): ゴーストの色（RGB）
        init_cell (tuple[int, int]): ゴーストの初期座標（セル単位）
        space (int): 描画時にゴースト画像を中央に配置するためのオフセット値
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書。
        frame (int): アニメーション用フレーム番号
        anim_timer (float): アニメーション用タイマー
        anim_interval (float): アニメーション切り替え間隔
        skip_move (bool): いじけ状態で移動をスキップするかどうかを示すフラグ
        target (tuple[int, int]): ゴーストの移動目標座標（セル単位）
        route (list[Direction]): ゴーストが移動するルート（方向）のリスト
        cooltimer (float): 待機状態の経過時間
        blinking_time (float): 点滅状態の経過時間
        is_drawable (bool): ゴーストが描画可能かどうかを示すフラグ
    """

    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, speed)

        self.points: int = points
        self.current_mode: GhostMode = GhostMode.CHASE
        self.mode_time: dict[GhostMode, int] = {
            GhostMode.READY: 0,
            GhostMode.CHASE: 20,
            GhostMode.SCATTER: 8,
            GhostMode.SCARED: 8,
            GhostMode.EATEN: 0
        }
        self.mode_timer: float = 0.0

        self.direction: Direction = Direction.LEFT
        self.px: int = px
        self.py: int = py
        self.size: int = 24
        self.color: tuple[int, int, int] = color
        self.init_cell: tuple[int, int] = (x, y)

        self.space: int = self.size // 2

        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        self.images: dict[str, pygame.Surface] = {}
        for direction in Direction:
            for freme in [0, 1]:
                key = f"eye_{direction}"
                self.images[key] = pygame.image.load(f"{asset_root}/ghost/eyes/{key}.png")
                key = f"scared_{freme}"
                self.images[key] = pygame.image.load(f"{asset_root}/ghost/ghost_{key}.png")

        self.frame: int = 1
        self.anim_timer: float = 0.0
        self.anim_interval: float = 0.15

        self.skip_move: bool = False

        self.target: tuple[int, int] = (0, 0)
        self.route: list[Direction] = []

        self.cooltimer: float = 0.0
        self.blinking_time: float = 0.0
        self.is_drawable: bool = True

    def update(self, game_state: GameState) -> None:
        """Blinkyの状態を更新する関数.

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

        # Mode Swich
        self.mode_timer += game_state.dt
        self._mode_change(game_state)

        # Animation
        # 足元
        self.anim_timer += game_state.dt
        if self.anim_interval < self.anim_timer:
            self.frame = 1 - self.frame
            self.anim_timer = 0.0
        # 点滅
        if 0 < self.blinking_time:
            self.blinking_time -= game_state.dt
            if int(self.blinking_time * 10) % 2 == 0:
                self.is_drawable = False
            else:
                self.is_drawable = True
            if self.blinking_time <= 0:
                self.is_drawable = True

        # いじけ時　Frame skip
        if self.current_mode == GhostMode.SCARED:
            self.skip_move = not self.skip_move
            if self.skip_move:
                return

        # 待機時は移動しない
        if self.current_mode == GhostMode.READY:
            return

        # Movement
        move_step = 3 if self.current_mode == GhostMode.EATEN else 1
        for _ in range(move_step):
            if self.direction == Direction.UP:
                self.py -= self.speed
            elif self.direction == Direction.RIGHT:
                self.px += self.speed
            elif self.direction == Direction.DOWN:
                self.py += self.speed
            elif self.direction == Direction.LEFT:
                self.px -= self.speed
            if map.is_center(self.px, self.py) is not None:
                break

    def draw(self, screen: pygame.Surface) -> None:
        """ゴーストを描画する関数.

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        if not self.is_drawable:
            return

        if self.current_mode == GhostMode.EATEN:
            key = f"eye_{self.direction}"
        elif self.current_mode == GhostMode.SCARED:
            key = f"scared_{self.frame}"
        else:
            key = f"{self.direction}_{self.frame}"
        screen.blit(self.images[key], (self.px - self.space, self.py - self.space))

    @abstractmethod
    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理.

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        pass

    def be_scared(self) -> None:
        """いじけ状態にする関数."""
        self.current_mode = GhostMode.SCARED
        self.mode_timer = 0.0

    def be_eaten(self) -> None:
        """捕食後状態にする関数."""
        self.current_mode = GhostMode.EATEN

#    Praivate Method

    # 各ゴーストの独自アルゴリズム
    @abstractmethod
    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する.

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト

        Returns:
            tuple[int, int]: ゴーストの移動目標座標
        """
        pass

    def _get_route(self, game_state: GameState) -> list[Direction]:
        """ゴーストの移動ルートを取得する.

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

        # ゴールがスタートと同じ場合は、現在位置から抜ける方向を選ぶ
        if start == goal:
            if not map.is_wall(x, y, Direction.UP) and self.direction != Direction.DOWN:
                return [Direction.UP]
            elif not map.is_wall(x, y, Direction.RIGHT) and self.direction != Direction.LEFT:
                return [Direction.RIGHT]
            elif not map.is_wall(x, y, Direction.DOWN) and self.direction != Direction.UP:
                return [Direction.DOWN]
            elif not map.is_wall(x, y, Direction.LEFT) and self.direction != Direction.RIGHT:
                return [Direction.LEFT]
            # パックマンと同じセルかつゴーストが壁に囲まれている場合は、逆方向に進む
            else:
                return [reverse_direction[self.direction]]

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

        # ゴールに到達できなかった場合は、探索済みかつ到達可能なセルの中でゴールに最も近いセルを選ぶ
        if goal not in came_from or goal == start:
            # スタートじゃないセルの中で、到達可能なものを探す
            reachable_cells = [cell for cell in came_from.keys() if cell != start]
            # スタートとゴールが同じ場合逆方向に進む
            if not reachable_cells:
                return [reverse_direction[self.direction]]
            original_goal_x, original_goal_y = goal
            # 到達可能なセルの中で、ゴールに最も近いセルを選ぶ
            goal = min(
                reachable_cells, key=lambda cell: abs(cell[0] - original_goal_x) + abs(cell[1] - original_goal_y)
            )

        # ゴールからスタートまでのルートを逆順にたどり、方向のリストを作成する
        route: list[Direction] = []
        current = goal
        while current != start:
            direction, previous = came_from[current]
            route.append(direction)
            current = previous
        route.reverse()

        return route

    def _mode_change(self, game_state: GameState) -> None:
        """ゴーストの状態を切り替える関数.

        CHASE <-> SCATTER
        CHASE <-> SCARED -> EATEN -> READY -> CHASE

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト。
        """
        assert game_state.map is not None
        map: Map = game_state.map
        # 縄張り時、初期座標に戻ったら追跡へ
        if self.current_mode == GhostMode.SCATTER and (self.x, self.y) == self.init_cell:
            self.current_mode = GhostMode.CHASE

        # 捕食後、初期座標に戻ったら待機へ
        # fix:初期座標セル内にいる状態で捕食された場合、現在座標を初期座標に
        if self.current_mode == GhostMode.EATEN and (self.x, self.y) == self.init_cell:
            self.px, self.py = map.cell_center(self.x, self.y)
            self.current_mode = GhostMode.READY
            self.blinking_time += 3

        # 待機時、3秒経過したら追跡へ
        if self.current_mode == GhostMode.READY:
            self.cooltimer += game_state.dt
            if 3 <= self.cooltimer:
                self.current_mode = GhostMode.CHASE
                self.cooltimer = 0.0

        # Mode Switcher
        if self.mode_time[self.current_mode] <= self.mode_timer:
            self.mode_timer = 0.0
            if self.current_mode == GhostMode.CHASE:
                self.current_mode = GhostMode.SCATTER
            elif self.current_mode == GhostMode.SCATTER:
                self.current_mode = GhostMode.CHASE
            elif self.current_mode == GhostMode.SCARED:
                self.current_mode = GhostMode.CHASE
