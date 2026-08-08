from src.model.base_model.item import Item


class Pacgum(Item):
    """パックガムのクラス"""
    def __init__(self, x: int, y: int, points: int, color: tuple[int, int, int], size: int) -> None:
        super().__init__(x, y, points, color, size)
