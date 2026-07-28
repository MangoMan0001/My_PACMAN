import pygame
from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path


class Scene(ABC):
    def __init__(self, config: dict[str, int | list[dict[str, int]] | Path]):
        self.config = config

    @abstractmethod
    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す
        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
