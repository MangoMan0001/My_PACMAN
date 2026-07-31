import pygame
import time

from src.model.game_state import GameState
from src.model.map import Map
from src.model.base_model.ghost import Ghost
from src.model.base_model.character import Direction


# --- 「現在のパックマンがいるマスの座標」に最短距離で向かう
class Blinky(Ghost):
    def __init__(self, x: int, y: int, speed: int, color: tuple[int, int, int], points: int) -> None:
        super().__init__(x, y, speed, points)
        self.direction: Direction = Direction.LEFT  # 現在の進行方向
        self.px: int = 0
        self.py: int = 0
        self.size: int = 24
        self.color: tuple[int, int, int] = color

        self.space: int = self.size // 2

        self.images: dict[str, pygame.Surface] = {}
        for direction in Direction:
            if direction == Direction.STOP:
                continue
            for freme in [0, 1]:
                key = f"{direction}_{freme}"
                self.images[key] = pygame.image.load(f"assets/ghost/ghost_blinky_{key}.png")

        self.frame: int = 1
        self.last_anim_time: float = time.time()
        self.anim_interval: float = 0.15

    def update(self, game_state: GameState) -> None:
        assert game_state.map is not None
        map: Map = game_state.map

        self._get_target(game_state)

        self.px, self.py = map.area_center(self.x, self.y)

        current_time = time.time()
        if self.anim_interval < current_time - self.last_anim_time:
            self.frame = 1 - self.frame
            self.last_anim_time = current_time

    def draw(self, screen: pygame.Surface) -> None:

        key = f"{self.direction}_{self.frame}"
        screen.blit(self.images[key], (self.px - self.space, self.py - self.space))
        pass

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理"""
        assert game_state.map is not None
        map: Map = game_state.map

        self.x, self.y = 0, 0

    def _get_target(self, game_state: GameState) -> None:
        self.target = (0, 0)
        pass
