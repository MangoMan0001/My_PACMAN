"""
Todo:
    - [ ] SCREEN_WIDTH, SCREEN_HEIGHTは共通のはずなので、そこからimportしたい。
    - [ ] 文字の大きさ等要調整。
"""
import pygame
from typing import Any

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MainMenu(Scene):

    TITLE_SIZE = 128
    INFO_SIZE = 48
    BACKGROUND_COLOR = (0, 0, 0)  # 黒
    TITLE_COLOR = (255, 255, 0)   # 黄色
    INFO_COLOR = (255, 255, 255)   # 白

    def __init__(self, config: ConfigModel):
        super().__init__(config)

        # 初期フォントの設定(これがないと文字がかけないので必要)
        self.font: dict[str, pygame.font.Font] = {
            "title": pygame.font.Font(None, self.TITLE_SIZE),
            "info": pygame.font.Font(None, self.INFO_SIZE)
        }

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """
        イベントを処理する。
        画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return ("PLAY", None)
        return None

    def _string_put(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        color: tuple[int, int, int],
        string: str,
        type: str = "info"
    ) -> None:
        # font.render(text, antialias, color, background=None) -> Surface:
        # antialiasはTrueで文字が滑らかになるが、処理が重くなる。今回は✕！
        text_surface = self.font[type].render(string, False, color)
        # surface.blit(source, dest, area=None, special_flags=0) -> Rect
        # 今回はsource=描画する元のサーフェス、dest=(x, y)
        screen.blit(text_surface, (x, y))

    def _draw_title(self, screen: pygame.Surface) -> None:
        """タイトルの描画

        Todo:
            - [ ] 中の// 2の部分なに？調整で入れたけどわからん
        """
        # タイトルの描画
        title_text = "PAC-MAN"
        # 画面全体の横の長さ - 文字の長さ // 2で横方向中央に配置
        title_x = (SCREEN_WIDTH - len(title_text) * self.TITLE_SIZE // 2) // 2
        # 画面全体の高さ // 12で縦方向に配置
        title_y = SCREEN_HEIGHT // 20
        self._string_put(
            screen, title_x, title_y, self.TITLE_COLOR, title_text, "title"
        )

    def _draw_info(self, screen: pygame.Surface) -> None:
        """タイトル下、サブタイトルの描画

        Todo:
            - [ ] 点滅可能ならさせたい。
            - [ ] // 2.5の部分は文字の大きさに応じて調整する(なんでやねん)
        """
        info_text = "Push SPACE to play"
        info_x = (SCREEN_WIDTH - len(info_text) * self.INFO_SIZE // 2.5) // 2
        info_y = SCREEN_HEIGHT // 3
        self._string_put(
            screen, info_x, info_y, self.INFO_COLOR, info_text
        )

    def _draw_score(self, screen: pygame.Surface) -> None:
        """スコアの描画

        Todo:
            - [ ] スコアを取得してハイスコア上位n件をループで描画するようにする。
            - [ ] // 3の部分は文字の大きさに応じて調整する(ほんとになんで)
        """
        score_text = "This space is for score."
        score_x = (SCREEN_WIDTH - len(score_text) * self.INFO_SIZE // 3) // 2
        score_y = SCREEN_HEIGHT // 2

        self._string_put(
            screen, score_x, score_y, self.INFO_COLOR, score_text
        )

    def draw(self, screen: pygame.Surface) -> None:
        """タイトル画面の描画。

        Todo:
            - [ ] spaceを押すとゲームが始まるようにする。
        """
        # 指定した色で画面を塗りつぶす
        screen.fill(self.BACKGROUND_COLOR)

        self._draw_title(screen)
        self._draw_info(screen)
        self._draw_score(screen)
