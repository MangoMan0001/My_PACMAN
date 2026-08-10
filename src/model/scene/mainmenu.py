"""ゲーム開始後、ゲーム中の特定の動作で表示するタイトル画面のシーン。

Todo:
    - [ ] 隠しコマンドの実装。
"""
import pygame
import json
from typing import Any
from pathlib import Path

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel
from src.model.image_font import ImageFont
from src.model.score_manager import ScoreManager


class MainMenu(Scene):
    """タイトル画面のシーン。

    Args:
        config (ConfigModel): 設定モデル。
        score_manager (ScoreManager): スコア管理を行うオブジェクト。

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

    def __init__(self, config: ConfigModel, score_manager: ScoreManager) -> None:
        super().__init__(config)
        self.score_maneger = score_manager
        self.scores = self.score_maneger.get_sorted_score()

        title_font = ImageFont(Path("pacfont_256"))
        info_font = ImageFont(Path("pacfont_128"))
        menu_font = ImageFont(Path("pacfont_64"))
        self.number_font = ImageFont(
            Path("nonefont_32"), filename_pattern="none-FONT_{char}.png"
        )

        title_text = "PAC-MAN"
        info_text = "PUSH SPACE TO PLAY"
        score_text = "HIGH SCORE RANKING"
        self.menu_text = ["HOW TO PLAY", "QUIT"]

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
                    if label == "HOW TO PLAY":
                        return ("PLAY", None)
                    elif label == "QUIT":
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
        return None

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
        score_y = (y // 30) * 9
        screen.blit(self.score_image, (score_x, score_y))

        base_x = score_x + 50
        name_offset = 100
        score_offset = 400
        pts_offset = 650

        for i, data in enumerate(self.scores):
            ranking = i + 1
            # 上位10位まで表示する
            if ranking > 10:
                break
            row_y = (y // 32) * (i + 13)

            ranking_images = self.number_font.render_text(f"{ranking}.")
            name_images = self.number_font.render_text(str(data['name']))
            score_images = self.number_font.render_text(f" - {str(data['score'])}")
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
        start_y = (screen_y // 30) * 21

        for index, image in enumerate(self.item_images):
            item_x = (screen_x - image.get_width()) // 2
            item_y = start_y + index * item_height
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

        # タイトルは画面の中央かつ一番上に表示する
        title_x = (screen_x - self.title_image.get_width()) // 2
        title_y = 0
        screen.blit(self.title_image, (title_x, title_y))

        # Push SPACE TO PLAYのインフォは画面の中央かつ下に表示する
        info_x = (screen_x - self.info_image.get_width()) // 2
        info_y = (screen_y // 30) * 25
        screen.blit(self.info_image, (info_x, info_y))

        # 上位10件のスコアを描画
        self._draw_score(screen, screen_x, screen_y)
        # 選択できるメニュー項目の描画
        self._menu_item_draw(screen, screen_x, screen_y)
