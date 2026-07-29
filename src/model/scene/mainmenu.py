import pygame
from typing import Any

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MainMenu(Scene):

    FONT_SIZE = 128
    BACKGROUND_COLOR = (0, 0, 0)  # 黒
    TITLE_COLOR = (255, 255, 0)   # 黄色
    MENU_COLOR = (255, 255, 255)   # 白

    def __init__(self, config: ConfigModel):
        super().__init__(config)

        # 初期フォントの設定(これがないと文字がかけないので必要)
        self.font = pygame.font.Font(None, self.FONT_SIZE)

    def _string_put(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        color: tuple[int, int, int],
        string: str
    ) -> None:
        # font.render(text, antialias, color, background=None) -> Surface:
        # antialiasはTrueで文字が滑らかになるが、処理が重くなる。今回は✕！
        text_surface = self.font.render(string, True, color)
        # surface.blit(source, dest, area=None, special_flags=0) -> Rect
        # 今回はsource=描画する元のサーフェス、dest=(x, y)
        screen.blit(text_surface, (x, y))

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す
        """
        # ===== "PLAY"から"MAIN_MENU"に変更してます。 =====
        return ("MAIN_MENU", None)

    def draw(self, screen: pygame.Surface) -> None:
        # 指定した色で画面を塗りつぶす
        screen.fill(self.BACKGROUND_COLOR)

        # タイトルの描画
        title_text = "PAC-MAN"
        # 画面全体の横の長さ - 文字の長さ // 2で横方向中央に配置
        title_x = (SCREEN_WIDTH - len(title_text) * self.FONT_SIZE // 2) // 2
        # 画面全体の高さ // 12で縦方向に配置
        title_y = SCREEN_HEIGHT // 12

        self._string_put(
            screen, title_x, title_y, self.TITLE_COLOR, title_text
        )
