from src.model.base_model.entity import Entity


# --- アイテムの基底クラス ---
class Item(Entity):
    """アイテムの基底クラス

    Attributes:
        px (int): 画面上のx座標
        py (int): 画面上のy座標
        points (int): アイテムを取得したときのポイント
        is_eaten (bool): アイテムが食べられたかどうか
    """
    def __init__(self, x: int, y: int, points: int) -> None:
        super().__init__(x, y)
        self.px: int = 0
        self.py: int = 0
        self.points: int = points  # 取得時のポイント
        self.is_eaten: bool = False  # 食べられているか
