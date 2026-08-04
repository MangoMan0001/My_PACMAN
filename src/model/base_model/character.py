from enum import StrEnum

from src.model.base_model.entity import Entity


class Direction(StrEnum):
    """キャラクターの進行方向を表す列挙型"""
    UP = 'up'
    RIGHT = 'right'
    DOWN = 'down'
    LEFT = 'left'
    STOP = 'stop'


# --- キャラクター系 (動く) ---
class Character(Entity):
    """キャラクターの基底クラス

    Attributes:
        speed (int): キャラクターの移動速度
        direction (Direction): キャラクターの進行方向
    """
    def __init__(self, x: int, y: int, speed: int):
        super().__init__(x, y)
        self.speed: int = speed
        self.direction: Direction = Direction.STOP  # 現在の進行方向
