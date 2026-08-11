"""ゲーム開始後、ゲーム中の特定の動作で表示するタイトル画面のシーン。

Todo:
    - [ ] 隠しコマンドの実装。
"""

import pygame
from typing import Any
from pathlib import Path

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel
from src.model.image_font import ImageFont
from src.model.score_manager import ScoreManager
from src.model.scene.how_to_play import HowToPlay


class MainMenu(Scene):
    """タイトル画面のシーン。

    Args:
        config (ConfigModel): 設定モデル。
        score_manager (ScoreManager): スコア管理を行うオブジェクト。

    Attributes:
        BACKGROUND_COLOR (tuple[int, int, int]): 背景色(RGB)
        CURSOR_SPACE (int): カーソルとメニュー項目の間隔

        number_font (ImageFont): 数字用のフォント。
        menu_items (list[str]): メニュー項目の文字列リスト。
        cursor_image (pygame.Surface): カーソル画像。
        title_image (pygame.Surface): タイトル画像。
        info_image (list[pygame.Surface]): ゲームスタートのインフォ画像。
        score_image (pygame.Surface): スコア画像。
        item_images (list[pygame.Surface]): メニュー項目の画像リスト。
        selected_index (int): 選択中のメニュー項目のインデックス。
        scores (list[dict[str, int]]): ハイスコアのリスト。各要素はプレイヤー名とスコアの辞書。

        how_to_play_scene (HowToPlay): How to Playのシーン。
        showing_how_to_play (bool): How to Playのシーンが表示中かどうかのフラグ。
    """

    BACKGROUND_COLOR = (0, 0, 0)  # 黒
    CURSOR_SPACE = 30  # カーソルとメニュー項目の間隔

    def __init__(self, config: ConfigModel, score_manager: ScoreManager) -> None:
        super().__init__(config)
        self.score_manager = score_manager
        self.scores = self.score_manager.get_sorted_score()

        # タイトルの文字列画像
        title_font = ImageFont(Path("pacfont_256"))
        title_text = "PAC-MAN"
        self.title_image = title_font.render_text(title_text)

        # ゲームスタートのインフォ画像
        info_font = ImageFont(Path("pacfont_128"))
        info_text = "PUSH SPACE TO PLAY"
        self.info_image = info_font.render_text(info_text)

        # スコアランキングの文字列画像
        menu_font = ImageFont(Path("pacfont_64"))
        score_text = "HIGH SCORE RANKING"
        self.score_image = menu_font.render_text(score_text)
        # スコアランキングの数字用のフォントを初期化
        self.number_font = ImageFont(
            Path("nonefont_32"), filename_pattern="none-FONT_{char}.png"
        )

        # 選択中のメニュー項目のインデックスを初期化
        self.selected_index: int = 0
        # カーソルの画像を初期化
        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        cursor_path = str(asset_root / "pacman" / "pacman_open_right.png")
        # convert_alpha()を使ってmlxと同じく透過情報を持つSurfaceに変換する。
        self.cursor_image = pygame.image.load(cursor_path).convert_alpha()
        # メニューの文字列画像
        self.menu_items = ["HOW TO PLAY", "QUIT"]
        self.menu_images = [menu_font.render_text(item) for item in self.menu_items]

        # How to Playのシーンを初期化
        self.how_to_play_scene = HowToPlay()
        self.showing_how_to_play = False

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
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
        if self.showing_how_to_play:
            self.showing_how_to_play = self.how_to_play_scene.update(events)
            return None

        for event in events:
            if event.type == pygame.KEYDOWN:
                # スペースキーでゲーム開始
                if event.key == pygame.K_SPACE:
                    return ("PLAY", None)

                # 上、wキーでメニュー項目の選択
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (self.selected_index - 1) % len(
                        self.menu_items
                    )
                # 下、sキーでメニュー項目の選択
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (self.selected_index + 1) % len(
                        self.menu_items
                    )
                # エンターキーで選択中のメニュー項目をアクティブにする
                elif event.key == pygame.K_RETURN:
                    label = self.menu_items[self.selected_index]
                    if label == "HOW TO PLAY":
                        self.showing_how_to_play = True
                    elif label == "QUIT":
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

        return None

    def _draw_title(self, screen: pygame.Surface, screen_x: int) -> None:
        """タイトルは画面の中央かつ一番上に表示する"""
        title_x = (screen_x - self.title_image.get_width()) // 2
        title_y = 0
        screen.blit(self.title_image, (title_x, title_y))

    def _draw_info(self, screen: pygame.Surface, screen_x: int, screen_y: int) -> None:
        """Push SPACE TO PLAYのインフォは画面の中央かつ下に表示する"""
        info_x = (screen_x - self.info_image.get_width()) // 2
        info_y = (screen_y // 30) * 25
        screen.blit(self.info_image, (info_x, info_y))

    def _draw_score(self, screen: pygame.Surface, x: int, y: int) -> None:
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
            name_images = self.number_font.render_text(str(data["name"]))
            score_images = self.number_font.render_text(f" - {str(data['score'])}")
            pts_images = self.number_font.render_text(" pts")

            screen.blit(ranking_images, (base_x, row_y))
            screen.blit(name_images, (base_x + name_offset, row_y))
            screen.blit(score_images, (base_x + score_offset, row_y))
            screen.blit(pts_images, (base_x + pts_offset, row_y))

    def _draw_menu_item(
        self, screen: pygame.Surface, screen_x: int, screen_y: int
    ) -> None:
        """メニュー項目の描画。

        画面の中央にメニュー項目を描画し、選択中の項目にはカーソルを表示する。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
            screen_x (int): 画面の幅
            screen_y (int): 画面の高さ
        """
        # 表示するメニュー項目から一番高い画像の高さを取得
        item_height = max(item.get_height() for item in self.menu_images)
        start_y = (screen_y // 30) * 21

        for index, image in enumerate(self.menu_images):
            item_x = (screen_x - image.get_width()) // 2
            item_y = start_y + index * item_height
            screen.blit(image, (item_x, item_y))

            if index == self.selected_index:
                cursor_x = item_x - self.cursor_image.get_width() - 30
                cursor_y = (
                    item_y + (image.get_height() - self.cursor_image.get_height()) // 2
                )
                screen.blit(self.cursor_image, (cursor_x, cursor_y))

    def draw(self, screen: pygame.Surface) -> None:
        """タイトル画面の描画。

        タイトル、インフォ、スコアを描画する。
        スペースキーが押されたらゲームを開始する。

        Args:
            screen (pygame.Surface): 描画先のSurface。
        """
        # How to Playのシーンが表示中の場合は、早期リターン
        if self.showing_how_to_play:
            self.how_to_play_scene.draw(screen)
            return None

        # 黒色で画面を塗りつぶす
        screen.fill(self.BACKGROUND_COLOR)
        # 画面の幅と高さを取得
        screen_x, screen_y = screen.get_size()

        # タイトルを描画
        self._draw_title(screen, screen_x)
        # インフォを描画
        self._draw_info(screen, screen_x, screen_y)
        # 上位10件のスコアを描画
        self._draw_score(screen, screen_x, screen_y)
        # 選択できるメニュー項目の描画
        self._draw_menu_item(screen, screen_x, screen_y)
