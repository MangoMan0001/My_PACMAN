"""ゲーム開始後、ゲーム中の特定の動作で表示するタイトル画面のシーン。

Todo:
    - [x] 文字列を画像に置き換える。
    - [ ] 文字の大きさ等要調整。
    - [ ] 隠しコマンドの実装。
    - [ ] カーソルの移動、決定を実装したい。 -> 何を選択したいか考えとく。
        - [ ] カーソルの点滅をさせる。
    - [ ] タイトルとインフォの文字列を可能なら点滅させたい。 -> 後回し
    - [ ] 毎回ハイスコアを読み込むのは重いのでハイスコアの更新があったときだけ読み込むようにしたい。
    - [ ] 名前の文字数制限15文字。
    - [ ] docstring書く。
    _draw_score:
        - [x] スコアを取得してハイスコア上位n件をループで描画するようにする。
        - [x] ハイスコアファイルを受け取ってtmp_scoresと入れ替える。
    draw:
        - [x] spaceを押すとゲームが始まるようにする。
"""
import pygame
import json
from typing import Any
from pathlib import Path

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel
from src.model.image_font import ImageFont


class MainMenu(Scene):
    """タイトル画面のシーン。

    Args:
        config (ConfigModel): 設定モデル。

    Attributes:
        BACKGROUND_COLOR (tuple[int, int, int]): 背景色(RGB)
        CURSOR_SPACE (int): カーソルとメニュー項目の間隔
        ITEM_LINE_SPACE (float): メニュー項目の行間

        number_font (ImageFont): 数字用のフォント。
        menu_text (list[str]): メニュー項目の文字列リスト。
        cursor_image (pygame.Surface): カーソル画像。
        title_image (pygame.Surface): タイトル画像。
        info_image (list[pygame.Surface]): ゲームスタートのインフォ画像。
        score_image (pygame.Surface): スコア画像。
        item_images (list[pygame.Surface]): メニュー項目の画像リスト。
        selected_index (int): 選択中のメニュー項目のインデックス。
        scores (dict[str, int]): ハイスコアの辞書。キーはプレイヤー名、値はスコア。
    """

    BACKGROUND_COLOR = (0, 0, 0)  # 黒
    CURSOR_SPACE = 30  # カーソルとメニュー項目の間隔
    ITEM_LINE_SPACE = 0.5  # メニュー項目の行間

    def __init__(self, config: ConfigModel) -> None:
        super().__init__(config)

        title_font = ImageFont(Path("pacfont_256"))
        info_font = ImageFont(Path("pacfont_128"))
        menu_font = ImageFont(Path("pacfont_64"))
        self.number_font = ImageFont(
            Path("nonefont_32"), filename_pattern="none-FONT_{char}.png"
        )

        title_text = "PAC-MAN"
        info_text = "PUSH SPACE TO PLAY"
        score_text = "HIGH SCORE RANKING"
        self.menu_text = ["PLAY", "QUIT"]

        # cursor用に使用。
        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        cursor_path = str(asset_root / "Pacman" / "PACMAN_right_32.png")

        # convert_alpha()を使ってmlxと同じく透過情報を持つSurfaceに変換する。
        self.cursor_image = pygame.image.load(cursor_path).convert_alpha()
        self.title_image = title_font.render_text(title_text)
        self.info_image = info_font.render_text(info_text)
        self.score_image = menu_font.render_text(score_text)
        self.item_images = [
            menu_font.render_text(label) for label in self.menu_text
        ]

        # 選択中のメニュー項目のインデックスを初期化
        self.selected_index = 0

        # のちのちハイスコアの表示に使う。 -> 必要なくなったかも
        self.scores: dict[str, int] = self._set_highscore()

    def update(
        self, events: list[pygame.event.Event]
    ) -> None | tuple[str, Any]:
        """選択されたメニュー項目をアクティブにする。

        - SPACEキーでゲーム開始
        - 上下(w, s)キーでメニュー項目の選択
        - Enterキーで選択中のメニュー項目をアクティブにする。

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            None | tuple[str, Any]:
                画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 上、wキーでメニュー項目の選択
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (
                        self.selected_index - 1) % len(self.menu_text)
                # 下、sキーでメニュー項目の選択
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (
                        self.selected_index + 1) % len(self.menu_text)
                # スペースキーでゲーム開始
                elif event.key == pygame.K_SPACE:
                    return ("PLAY", None)
                # エンターキーで選択中のメニュー項目をアクティブにする。
                elif event.key == pygame.K_RETURN:
                    label = self.menu_text[self.selected_index]
                    if label == "PLAY":
                        return ("PLAY", None)
                    elif label == "QUIT":
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
        return None

    def _set_highscore(self) -> dict[str, int]:
        """
        コンフィグからハイスコアの辞書を取得。
        ランキング順にソートして返す。

        Returns:
            dict[str, int]: ハイスコアの辞書。キーはプレイヤー名、値はスコア。
        """
        try:
            with open(self.config.highscore_filename, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = {}
        return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

    def _draw_score(
        self, screen: pygame.Surface, x: int, y: int
    ) -> None:
        """スコアの描画

        Args:
            screen (pygame.Surface): 描画先のSurface。
            x (int): 画面の幅
            y (int): 画面の高さ
        """
        score_x = (x - self.score_image.get_width()) // 2
        score_y = (y // 30) * 8
        screen.blit(self.score_image, (score_x, score_y))

        base_x = score_x
        name_offset = 100
        score_offset = 500
        pts_offset = 800

        for i, (name, score) in enumerate(self.scores.items()):
            ranking = i + 1
            # 上位10位まで表示する
            if ranking > 10:
                break
            row_y = (y // 30) * (i + 11)

            ranking_images = self.number_font.render_text(f"{ranking}.")
            name_images = self.number_font.render_text(name)
            score_images = self.number_font.render_text(f" - {score}")
            pts_images = self.number_font.render_text(" pts")

            screen.blit(ranking_images, (base_x, row_y))
            screen.blit(name_images, (base_x + name_offset, row_y))
            screen.blit(score_images, (base_x + score_offset, row_y))
            screen.blit(pts_images, (base_x + pts_offset, row_y))

    def _menu_item_draw(
        self, screen: pygame.Surface, screen_x: int, screen_y: int
    ) -> None:
        """メニュー項目の描画
        """
        item_height = max(item.get_height() for item in self.item_images)
        line_step = item_height + int(item_height * self.ITEM_LINE_SPACE)
        start_y = (screen_y // 30) * 21

        for index, image in enumerate(self.item_images):
            item_x = (screen_x - image.get_width()) // 2
            item_y = start_y + index * line_step
            screen.blit(image, (item_x, item_y))

            if index == self.selected_index:
                cursor_x = item_x - self.cursor_image.get_width() - 30
                cursor_y = item_y + (
                    image.get_height() - self.cursor_image.get_height()) // 2
                screen.blit(self.cursor_image, (cursor_x, cursor_y))

    def draw(self, screen: pygame.Surface) -> None:
        """タイトル画面の描画。

        タイトル、インフォ、スコアを描画する。
        スペースキーが押されたらゲームを開始する。

        Args:
            screen (pygame.Surface): 描画先のSurface。
        """
        # 黒色で画面を塗りつぶす
        screen.fill(self.BACKGROUND_COLOR)

        screen_x, screen_y = screen.get_size()

        # ======== テキスト、x座標、y座標を計算して描画する一連の流れ ========
        # -> 関数に分離する？
        title_x = (screen_x - self.title_image.get_width()) // 2
        title_y = (screen_y // 30) * 1
        screen.blit(self.title_image, (title_x, title_y))

        # ======== テキスト、x座標、y座標を計算して描画する一連の流れ ========
        # -> 関数に分離する？
        info_x = (screen_x - self.info_image.get_width()) // 2
        info_y = (screen_y // 30) * 25
        screen.blit(self.info_image, (info_x, info_y))

        # ハイスコアの描画
        self._draw_score(screen, screen_x, screen_y)
        # 選択できるメニュー項目の描画
        self._menu_item_draw(screen, screen_x, screen_y)
