import pygame
import time

from src.model.game_state import GameState
from src.model.map import Map
from src.model.base_model.character import Character, Direction


# --- パックマン ---
class Pacman(Character):
    def __init__(self, x: int, y: int, speed: int):
        super().__init__(x, y, speed)
        self.direction: Direction = Direction.LEFT  # 現在の進行方向
        self.px: int = 0
        self.py: int = 0
        self.size: int = 24

        self.space: int = self.size // 2

        self.img_closed = pygame.image.load('assets/pacman/pacman_closed.png').convert_alpha()
        self.img_open = {
            Direction.ABOVE: pygame.image.load('assets/pacman/pacman_open_above.png').convert_alpha(),
            Direction.RIGHT: pygame.image.load('assets/pacman/pacman_open_right.png').convert_alpha(),
            Direction.BOTTOM: pygame.image.load('assets/pacman/pacman_open_bottom.png').convert_alpha(),
            Direction.LEFT: pygame.image.load('assets/pacman/pacman_open_right.png').convert_alpha()
        }

        self.is_mouth_opne: bool = False
        self.last_anim_time: float = time.time()
        self.anim_interval: float = 0.15

    def update(self, game_state: GameState) -> None:
        # game-state内のkeys入力を受けて、game_state.maze と照らし合わせて移動判定
        assert game_state.map is not None
        map: Map = game_state.map

        current_time = time.time()
        if self.anim_interval < current_time - self.last_anim_time:
            self.is_mouth_opne = not self.is_mouth_opne
            self.last_anim_time = current_time

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
