"""
Todo:
    - [ ] SCREEN_WIDTH, SCREEN_HEIGHTは共通のはずなので、そこからimportしたい。
    - [ ] 文字の大きさ等要調整。
    - [ ] 隠しコマンドの実装。
    _draw_title:
        - [ ] 中の// 2の部分なに？調整で入れたけどわからん
    _draw_info:
        - [ ] 点滅可能ならさせたい。 -> 後回し
        - [ ] // 2.5の部分は文字の大きさに応じて調整する(なんでやねん)
        - [ ] * 25でちょうど下のいい位置にくる。上に描画する場合は要検討。
    _draw_score:
        - [x] スコアを取得してハイスコア上位n件をループで描画するようにする。
        - [x] // 3の部分は文字の大きさに応じて調整する(ほんとになんで)
        - [x] ハイスコアファイルを受け取ってtmp_scoresと入れ替える。
    draw:
        - [x] spaceを押すとゲームが始まるようにする。
"""
import pygame
import json
from typing import Any

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel

PAC_FONT = {
    chr(i): pygame.image.load(f"data/assets/PAC-FONT_{chr(i)}.png")
    for i in range(ord('A'), ord('Z') + 1)
}

class MainMenu(Scene):
    """タイトル画面のシーン。

    Attributes:
        TITLE_SIZE (int): タイトルの文字サイズ。
        INFO_SIZE (int): インフォの文字サイズ。
        BACKGROUND_COLOR (tuple[int, int, int]): 背景色(RGB)
        TITLE_COLOR (tuple[int, int, int]): タイトルの文字色(RGB)
        INFO_COLOR (tuple[int, int, int]): インフォの文字色(RGB)

        scores (dict[str, int] | None):
            ハイスコアの辞書。キーはプレイヤー名、値はスコア。
        font (dict[str, pygame.font.Font]):
            フォントの辞書。キーはフォント名、値はpygame.font.Fontオブジェクト。
    """

    TITLE_SIZE = 256
    INFO_SIZE = 64

    BACKGROUND_COLOR = (0, 0, 0)  # 黒
    TITLE_COLOR = (255, 255, 0)   # 黄色
    INFO_COLOR = (255, 255, 255)   # 白

    def __init__(self, config: ConfigModel) -> None:
        super().__init__(config)

        # のちのちハイスコアの表示に使う。
        self.scores: dict[str, int] | None = None
        # 初期フォントの設定(これがないと文字がかけないので必要)。
        self.font: dict[str, pygame.font.Font] = {
            "title": pygame.font.Font(None, self.TITLE_SIZE),
            "info": pygame.font.Font(None, self.INFO_SIZE)
        }

    def update(
        self, events: list[pygame.event.Event]
    ) -> None | tuple[str, Any]:
        """イベントを処理する。

        SPACEキーが押されたら、ゲームを開始するために"PLAY"を返す。

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            None | tuple[str, Any]:
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
        x: int | float,
        y: int | float,
        color: tuple[int, int, int],
        string: str,
        font_key: str = "info"
    ) -> None:
        """minilibxのmlx_string_putの代替関数。

        pygame.font.Font.render、Pygame.Surface.blitを使用。

        Args:
            screen (pygame.Surface): 描画先のSurface。
            x (int | float): 描画する文字列の左上のx座標
            y (int | float): 描画する文字列の左上のy座標
            color (tuple[int, int, int]): 描画する文字列の色(RGB)
            string (str): 描画する文字列
            font_key (str, optional):
                使用するフォントのキー。デフォルトは"info"。
        """
        # font.render(text, antialias, color, background=None) -> Surface:
        # antialiasはTrueで文字が滑らかになるが、処理が重くなる。今回は✕！
        text_surface = self.font[font_key].render(string, False, color)
        # surface.blit(source, dest, area=None, special_flags=0) -> Rect
        # 今回はsource=描画する元のサーフェス、dest=(x, y)
        screen.blit(text_surface, (x, y))

    def _draw_title(
        self, screen: pygame.Surface, x: int, y: int
    ) -> None:
        """タイトルの描画

        Args:
            screen (pygame.Surface): 描画先のSurface。
            x (int): 画面の幅
            y (int): 画面の高さ
        """
        title_text = "PAC-MAN"
        title_x = (x - len(title_text) * self.TITLE_SIZE // 2) // 2
        title_y = (y // 30) * 5
        self._string_put(
            screen, title_x, title_y, self.TITLE_COLOR, title_text, "title"
        )

    def _draw_info(
        self, screen: pygame.Surface, x: int, y: int
    ) -> None:
        """インフォの描画

        Args:
            screen (pygame.Surface): 描画先のSurface。
            x (int): 画面の幅
            y (int): 画面の高さ
        """
        # ======== テキスト、x座標、y座標を計算して描画する一連の流れ ========
        info_text = "Push  SPACE  to  play"
        info_x = (x - len(info_text) * self.INFO_SIZE // 2.5) // 2
        info_y = (y // 30) * 25
        self._string_put(
            screen, info_x, info_y, self.INFO_COLOR, info_text
        )

    def _set_highscore(self) -> dict[str, int]:
        """
        コンフィグからハイスコアの辞書を取得。
        ランキング順にソートして返す。

        Returns:
            dict[str, int]: ハイスコアの辞書。キーはプレイヤー名、値はスコア。
        """
        # ======== テキスト、x座標、y座標を計算して描画する一連の流れ ========
        with open(self.config.highscore_filename, "r", encoding="utf-8") as f:
            scores = json.load(f)
        scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        return scores

    def _draw_score(
        self, screen: pygame.Surface, x: int, y: int
    ) -> None:
        """スコアの描画

        Args:
            screen (pygame.Surface): 描画先のSurface。
            x (int): 画面の幅
            y (int): 画面の高さ
        """
        # ======== テキスト、x座標、y座標を計算して描画する一連の流れ ========
        score_text = "High Score Ranking  "
        score_x = (x - len(score_text) * self.INFO_SIZE // 2.5) // 2
        score_y = (y // 30) * 10
        self._string_put(
            screen, score_x, score_y, self.INFO_COLOR, score_text
        )

        scores: dict[str, int] = self._set_highscore()
        if self.scores is None or self.scores is not scores:
            self.scores = scores

        for i, (name, score) in enumerate(self.scores.items()):
            ranking = i + 1
            if ranking > 10:
                break

            # ====== テキスト、x座標、y座標を計算して描画する一連の流れ ======
            highscore_text = f"{ranking}. {name} - {score} pts"
            highscore_x = (x - len(highscore_text) * self.INFO_SIZE // 2.5) // 2
            highscore_y = (y // 30) * (i + 12)
            self._string_put(
                screen, highscore_x, highscore_y, self.INFO_COLOR, highscore_text
            )

    def draw(self, screen: pygame.Surface) -> None:
        """タイトル画面の描画。

        タイトル、インフォ、スコアを描画する。
        スペースキーが押されたらゲームを開始する。
        pygame.Surface.fill, pygame.Surface.get_sizeを使用。

        Args:
            screen (pygame.Surface): 描画先のSurface。
        """
        # 指定した色で画面を塗りつぶす
        screen.fill(self.BACKGROUND_COLOR)
        width, height = screen.get_size()

        self._draw_title(screen, width, height)
        self._draw_info(screen, width, height)
        self._draw_score(screen, width, height)
