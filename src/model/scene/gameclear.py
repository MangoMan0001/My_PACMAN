import pygame
from typing import Any

from src.model.base_model.scene import Scene


class GameClear(Scene):
    def __init__(self, config: dict[str, int | list[dict[str, int]] | Path]):
        super().__init__(config)

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass
