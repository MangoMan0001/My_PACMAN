import pygame
import time
from collections import deque

from src.model.game_state import GameState
from src.model.map import Map
from src.model.base_model.ghost import Ghost
from src.model.base_model.character import Direction


# --- パックマンとの距離が「8マス以上」離れている時はBlinkyと同じ 「8マス以内」に近づくと自分の初期位置をターゲットにする
class Clyde(Ghost):
    """GhostのClydeを表すクラス。
    追いかけるターゲットは「パックマンとの距離が「8マス以上」離れている時はBlinkyと同じ 「8マス以内」に近づくと自分の初期位置をターゲットにする」。

    Attributes:
        direction (Direction): 現在の進行方向
        px (int): ピクセル座標のx位置
        py (int): ピクセル座標のy位置
        size (int): キャラクターのサイズ（ピクセル単位）
        color (tuple[int, int, int]): キャラクターの色を表すRGB値のタプル
        space (int): キャラクターの描画位置調整
        images (dict[str, pygame.Surface]): キャラクターの画像を格納する辞書
        frame (int): アニメーションのフレーム番号
        last_anim_time (float): 最後にアニメーションを更新した時刻
        anim_interval (float): アニメーションの更新間隔（秒）
    """
    def __init__(self, x: int, y: int, px: int, py: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, speed, points)
        self.direction: Direction = Direction.LEFT  # 現在の進行方向
        self.px: int = px
        self.py: int = py
        self.size: int = 24
        self.color: tuple[int, int, int] = color

        self.space: int = self.size // 2

        self.images: dict[str, pygame.Surface] = {}
        for direction in Direction:
            if direction == Direction.STOP:
                continue
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"assets/ghost/ghost_clyde_{key}.png")

        self.frame: int = 1
        self.last_anim_time: float = time.time()
        self.anim_interval: float = 0.15

    def update(self, game_state: GameState) -> None:
        """Clydeの状態を更新する関数。

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
            else:
                self.direction = Direction.STOP

        # self.px, self.py = map.cell_center(self.x, self.y)
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
        """Clydeを描画する関数。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        key = f"{self.direction}_{self.frame}"
        screen.blit(self.images[key], (self.px - self.space, self.py - self.space))
        pass

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.x, self.y = map.x - 1, map.y - 1
        self.px, self.py = map.cell_center(self.x, self.y)

    def _get_target(self, game_state: GameState) -> tuple[int, int]:
        """ゴーストの移動目標座標を取得する

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト

        Returns:
            tuple[int, int]: ゴーストの移動目標座標
        """
        pacman = game_state.pacman
        assert pacman is not None

        return (pacman.x, pacman.y)

    def _get_route(self, game_state: GameState) -> list[Direction]:
        """ゴーストの移動ルートを取得する

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト

        Returns:
            list[Direction]: ゴーストの移動ルートのリスト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        start = (self.x, self.y)
        goal = self.target
        if start == goal:
            return []

        # 各方向のDirectionと座標の変化量
        moves: list[tuple[Direction, int, int]] = [
            (Direction.UP, 0, -1),
            (Direction.RIGHT, 1, 0),
            (Direction.DOWN, 0, 1),
            (Direction.LEFT, -1, 0)
        ]

        queue: deque[tuple[int, int]] = deque([start])
        visited: set[tuple[int, int]] = {start}
        # 各座標をキーに、その座標に到達する直前の座標を値として保持する辞書
        came_from: dict[tuple[int, int], tuple[Direction, tuple[int, int]]] = {}

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
                if not map.is_wall(current_x, current_y, direction):
                    continue
                # 訪問済み
                if (next_x, next_y) in visited:
                    continue
                visited.add((next_x, next_y))
                came_from[(next_x, next_y)] = (direction, (current_x, current_y))
                queue.append((next_x, next_y))

        # ゴールに到達できなかった場合は空のリストを返す
        if goal not in came_from:
            return []

        # ゴールからスタートまでのルートを逆順にたどり、方向のリストを作成する
        route: list[Direction] = []
        current = goal
        while current != start:
            direction, previous = came_from[current]
            route.append(direction)
            current = previous
        route.reverse()

        return route
