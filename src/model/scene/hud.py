import pygame
from typing import Any
from pathlib import Path

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel
from src.model.image_font import ImageFont


class HUD(Scene):
    def __init__(self, config: ConfigModel):
        super().__init__(config)

        self.hud_font = ImageFont(Path("nonefont_64"))
        highscore_text = "High Score:"

        self.score_image = self.hud_

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す
        """
        pass

    def draw(self, screen: pygame.Surface, game_state: Any) -> None:
        pass
