"""MainMenu、Pauseで「HOW TO PLAY」を選択したときに表示されるシーン。"""
import pygame
from pathlib import Path

from src.model.image_font import ImageFont


class HowToPlay:
    """MainMenu、Pauseの「HOW TO PLAY」を選択したときに表示されるシーン。

    Attributes:
        howto_image (pygame.Surface): How to Playの画像。
        info_image (pygame.Surface): インフォメーションの画像。
    """
    def __init__(self) -> None:
        # How to Playの画像を読み込む
        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        image_path = Path("how_to_play") / "how_to_play.png"
        self.howto_image = pygame.image.load(
            str(asset_root / image_path)
        )

        # 画面下部に表示するインフォメーションの画像
        info_font = ImageFont(Path("pacfont_64"))
        self.info_image = info_font.render_text("PUSH ESC TO RETURN")

    def update(self, events: list[pygame.event.Event]) -> bool:
        """毎フレーム呼ばれる処理。イベントを処理し、必要に応じて画面遷移を行う。

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            bool: 画面遷移が必要な場合はFalse、そうでない場合はTrueを返す。
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
