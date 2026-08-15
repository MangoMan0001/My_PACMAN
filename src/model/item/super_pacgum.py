"""スーパーパックガムのクラス."""
from src.model.base_model.item import Item


class SuperPacgum(Item):
    """スーパー・パックガムのクラス."""
    def __init__(self, x: int, y: int, points: int, color: tuple[int, int, int], size: int) -> None:
        """SuperPacgumクラスのコンストラクタ."""
        super().__init__(x, y, points, color, size)
