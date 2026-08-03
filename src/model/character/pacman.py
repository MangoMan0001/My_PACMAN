import pygame
import time

from src.model.game_state import GameState
from src.model.map import Map
from src.model.base_model.character import Character, Direction


# --- パックマン ---
class Pacman(Character):
    def __init__(self, x: int, y: int, px: int,  py: int,  speed: int):
        super().__init__(x, y, speed)
        self.direction: Direction = Direction.LEFT  # 現在の進行方向
        self.next_direction: Direction = Direction.LEFT
        self.px: int = px
        self.py: int = py
        self.size: int = 24

        self.space: int = self.size // 2

        self.img_closed = pygame.image.load('assets/pacman/pacman_closed.png').convert_alpha()
        self.img_open = {
            Direction.UP: pygame.image.load('assets/pacman/pacman_open_up.png').convert_alpha(),
            Direction.RIGHT: pygame.image.load('assets/pacman/pacman_open_right.png').convert_alpha(),
            Direction.DOWN: pygame.image.load('assets/pacman/pacman_open_down.png').convert_alpha(),
            Direction.LEFT: pygame.image.load('assets/pacman/pacman_open_left.png').convert_alpha()
        }

        self.is_mouth_opne: bool = False
        self.last_anim_time: float = time.time()
        self.anim_interval: float = 0.15

        self.key_status: dict[int, bool] = {
            pygame.K_w: False,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: False,
            }
        self.is_moving = False

    def update(self, game_state: GameState) -> None:
        # game-state内のkeys入力を受けて、game_state.maze と照らし合わせて移動判定
        assert game_state.map is not None
        map: Map = game_state.map

        # アニメーション
        current_time = time.time()
        if self.anim_interval < current_time - self.last_anim_time:
            self.is_mouth_opne = not self.is_mouth_opne
            self.last_anim_time = current_time

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

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_mouth_opne:
            screen.blit(self.img_open[self.direction], (self.px - self.space, self.py - self.space))
        else:
            screen.blit(self.img_closed, (self.px - self.space, self.py - self.space))

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理"""
        assert game_state.map is not None
        map: Map = game_state.map

        self.x, self.y = map.init_area_pacman()
        self.px, self.py = map.area_center(self.x, self.y)
        self.direction = Direction.LEFT
        self.next_direction: Direction = Direction.LEFT
        self.is_moving = False

    def get_pos(self) -> tuple[int, int]:
        return (self.x, self.y)
