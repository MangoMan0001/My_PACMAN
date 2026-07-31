from enum import StrEnum

from src.model.base_model.entity import Entity


class Direction(StrEnum):
    ABOVE = 'above'
    RIGHT = 'right'
    BOTTOM = 'bottom'
    LEFT = 'left'
    STOP = 'stop'


# --- キャラクター系 (動く) ---
class Character(Entity):
    def __init__(self, x: int, y: int, speed: int):
        super().__init__(x, y)
        self.speed: int = speed
        self.direction: Direction = Direction.STOP  # 現在の進行方向
