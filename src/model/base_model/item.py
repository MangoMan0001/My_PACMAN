from src.model.base_model.entity import Entity


# --- アイテム系 (動かない) ---
class Item(Entity):
    def __init__(self, x: int, y: int, points: int) -> None:
        super().__init__(x, y)
        self.points: int = points  # 取得時のポイント
        self.is_eaten: bool = False  # 食べられているか
