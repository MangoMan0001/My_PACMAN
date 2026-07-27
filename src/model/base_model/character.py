from entity import Entity


# --- キャラクター系 (動く) ---
class Character(Entity):
    def __init__(self, x: int, y: int, speed: int):
        super().__init__(x, y)
        self.speed = speed
        self.direction = "STOP"  # 現在の進行方向
