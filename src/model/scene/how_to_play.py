import pygame
from typing import Any
from pathlib import Path

from src.model.base_model.config_model import ConfigModel
from src.model.base_model.scene import Scene
from src.model.image_font import ImageFont


# --- シーンの基底クラス ---
class HowToPlay(Scene):
    """ゲームのシーンの基底クラス.

    Attributes:
        config (ConfigModel): ゲームの設定を保持するオブジェクト
    """
    def __init__(self, config: ConfigModel):
        super().__init__(config)

        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        image_path = str(asset_root / "how_to_play" / "how_to_play.png")
        self.howto_image = pygame.image.load(
            str(asset_root / image_path)
        )

        info_font = ImageFont(Path("pacfont_64"))
        self.info_image = info_font.render_text("PUSH SPACE TO RETURN")

    def update(self, events: list[pygame.event.Event]) -> bool:
        """毎フレーム呼ばれる処理。イベントを処理し、必要に応じて画面遷移を行う。

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            bool: 画面遷移が必要な場合はFalse、そうでない場合はTrueを返す。
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False
        return True

    def draw(self, screen: pygame.Surface) -> None:
        """毎フレーム呼ばれる描画処理。画面に描画する。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        howto_x = (screen.get_width() - self.howto_image.get_width()) // 2
        howto_y = (screen.get_height() - self.howto_image.get_height()) // 2
        screen.blit(self.howto_image, (howto_x, howto_y))

        info_x = (screen.get_width() - self.info_image.get_width()) // 2
        info_y = (screen.get_height() // 30) * 27
        screen.blit(self.info_image, (info_x, info_y))
