import pygame

from src.model.game_state import GameState
from src.model.map import Map
from src.model.base_model.character import Character, Direction


# --- パックマン ---
class Pacman(Character):
    """パックマンのクラス

    Attributes:
        direction (Direction): 現在の進行方向
        next_direction (Direction): 次の進行方向（予約）
        px (int): ピクセル単位でのx座標
        py (int): ピクセル単位でのy座標
        size (int): パックマンのサイズ（ピクセル単位）
        space (int): パックマンの描画位置調整用のスペース（ピクセル単位）
        img_closed (pygame.Surface): 口を閉じた状態のパックマンの画像
        img_open (dict[Direction, pygame.Surface]): 口を開いた状態のパックマンの画像を方向ごとに保持する辞書
        is_mouth_open (bool): パックマンの口が開いているかどうかのフラグ
        last_anim_time (float): 最後にアニメーションを更新した時刻
        anim_interval (float): アニメーションの更新間隔（秒）
        key_status (dict[int, bool]): キー入力の状態を保持する辞書
        is_moving (bool): パックマンが移動中かどうかのフラグ
        is_dash (bool): パックマンがダッシュ状態かどうかのフラグ
    """
    def __init__(self, x: int, y: int, px: int,  py: int,  speed: int):
        super().__init__(x, y, speed)
        self.direction: Direction = Direction.LEFT  # 現在の進行方向
        self.next_direction: Direction = Direction.LEFT
        self.px: int = px
        self.py: int = py
        self.size: int = 24

        self.space: int = self.size // 2

        self.img_closed = pygame.image.load('data/assets/pacman/pacman_closed.png').convert_alpha()
        self.img_open = {
            Direction.UP: pygame.image.load('data/assets/pacman/pacman_open_up.png').convert_alpha(),
            Direction.RIGHT: pygame.image.load('data/assets/pacman/pacman_open_right.png').convert_alpha(),
            Direction.DOWN: pygame.image.load('data/assets/pacman/pacman_open_down.png').convert_alpha(),
            Direction.LEFT: pygame.image.load('data/assets/pacman/pacman_open_left.png').convert_alpha()
        }

        self.is_mouth_opne: bool = False
        self.anim_timer: float = 0.0
        self.anim_interval: float = 0.15

        self.key_status: dict[int, bool] = {
            pygame.K_w: False,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: False,
            }

        # チートフラグ
        self.is_moving = False
        self.is_dash = False

    def update(self, game_state: GameState) -> None:
        """パックマンの状態を更新する関数。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        # game-state内のkeys入力を受けて、game_state.maze と照らし合わせて移動判定
        assert game_state.map is not None
        map: Map = game_state.map

        # アニメーション
        self.anim_timer += game_state.dt
        if self.anim_interval < self.anim_timer:
            self.is_mouth_opne = not self.is_mouth_opne
            self.anim_timer = 0.0

        # 座標変更
        coord = map.is_center(self.px, self.py)
        if coord is not None:
            self.x, self.y = coord

        # 移動操作
        events = game_state.events
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.is_moving = True
                if event.key == pygame.K_w:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_d:
                    self.next_direction = Direction.RIGHT
                elif event.key == pygame.K_s:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_a:
                    self.next_direction = Direction.LEFT

        # 方向の予約
        if map.is_moveable(self.x, self.y, self.px, self.py, self.next_direction):
            self.direction = self.next_direction

        # 実際の移動
        move_step = 3 if self.is_dash else 1
        for _ in range(move_step):
            if not self.is_moving:
                return
            if self.direction == Direction.UP and map.is_moveable(self.x, self.y, self.px, self.py, Direction.UP):
                self.py -= self.speed
            elif self.direction == Direction.RIGHT and map.is_moveable(self.x, self.y, self.px, self.py, Direction.RIGHT):
                self.px += self.speed
            elif self.direction == Direction.DOWN and map.is_moveable(self.x, self.y, self.px, self.py, Direction.DOWN):
                self.py += self.speed
            elif self.direction == Direction.LEFT and map.is_moveable(self.x, self.y, self.px, self.py, Direction.LEFT):
                self.px -= self.speed
            if map.is_center(self.px, self.py) is not None:
                break

    def draw(self, screen: pygame.Surface) -> None:
        """パックマンを描画する関数。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        if self.is_mouth_opne:
            screen.blit(self.img_open[self.direction], (self.px - self.space, self.py - self.space))
        else:
            screen.blit(self.img_closed, (self.px - self.space, self.py - self.space))

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        assert game_state.map is not None
        map: Map = game_state.map

        self.x, self.y = map.init_area_pacman()
        self.px, self.py = map.cell_center(self.x, self.y)
        self.direction = Direction.LEFT
        self.next_direction: Direction = Direction.LEFT
        self.is_moving = False

    def get_pos_cell(self) -> tuple[int, int]:
        """Pacmanの現在のセル座標を取得する。

        Returns:
            tuple[int, int]: Pacmanの現在のセル座標 (x, y)
        """
        return (self.x, self.y)

    def get_pos_pixel(self) -> tuple[int, int]:
        """Pacmanの現在のピクセル座標を取得する。

        Returns:
            tuple[int, int]: Pacmanの現在のピクセル座標 (px, py)
        """
        return (self.px, self.py)

    def dash(self) -> None:
        """パックマンのダッシュ状態を有効にする関数。"""
        self.is_dash = True

    def walk(self) -> None:
        """パックマンのダッシュ状態を無効にする関数。"""
        self.is_dash = False
