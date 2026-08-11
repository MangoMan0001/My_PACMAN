"""ゲーム中のポーズメニューを描画するクラス。

GameManagerクラスの中でのみ使用されるため、Sceneクラスを継承していない。

"""

import pygame
from pathlib import Path

from src.model.image_font import ImageFont
from src.model.scene.how_to_play import HowToPlay


class Pause:
    """ゲーム中のポーズメニューを描画するシーン。

    Attributes:
        title_image (pygame.Surface): ポーズメニューのタイトル画像
        menu_items (list[str]): メニュー項目のリスト
        menu_images (list[pygame.Surface]): メニュー項目の画像リスト
        selected_index (int): 現在選択されているメニュー項目のインデックス
        cursor_image (pygame.Surface): カーソルとして使用する画像
        dithering_surface (pygame.Surface): 透過背景の画像
        how_to_play_scene (HowToPlay): How to Playのシーン
        showing_how_to_play (bool): How to Playのシーンが表示中かどうかのフラグ
    """

    CURSOR_SPACE = 30  # カーソルとメニュー項目の間隔
    ITEM_LINE_SPACE = 0.5  # メニュー項目の行間

    def __init__(self) -> None:
        # ポーズの文字列画像
        title_font = ImageFont(Path("pacfont_128"))
        title_text = "PAUSE"
        self.title_image = title_font.render_text(title_text)

        # メニューの文字列画像
        menu_font = ImageFont(
            Path("nonefont_64"), filename_pattern="none-FONT_{char}.png"
        )
        self.menu_items: list[str] = ["Resume", "Retry", "How to Play", "Quit"]
        self.menu_images = [menu_font.render_text(item) for item in self.menu_items]

        # 選択中のメニュー項目のインデックスを初期化
        self.selected_index: int = 0
        # カーソルの画像を初期化
        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        cursor_path = str(asset_root / "pacman" / "pacman_open_right.png")
        # convert_alpha()を使ってmlxと同じく透過情報を持つSurfaceに変換する。
        self.cursor_image = pygame.image.load(cursor_path).convert_alpha()

        # 透過背景を初期化
        dither_path = str(asset_root / "dither_images" / "dither_surface.png")
        self.dithering_surface = pygame.image.load(dither_path).convert_alpha()

        # How to Playのシーンを初期化
        self.how_to_play_scene = HowToPlay()
        self.showing_how_to_play = False

    def reset(self) -> None:
        """ポーズメニューが表示されるたびに、選択インデックスを初期化する。"""
        self.selected_index = 0

    def update(self, events: list[pygame.event.Event]) -> None | str:
        """ポーズメニューの更新処理。
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            None | tuple[str, Any]:
                ゲームオーバーやゲームクリアなどの状態変化があれば、シーン名を返す。
                何もなければNoneを返す。
        """
        if self.showing_how_to_play:
            self.showing_how_to_play = self.how_to_play_scene.update(events)
            return None

        for event in events:
            if event.type == pygame.KEYDOWN:
                # pキーでポーズ解除
                if event.key == pygame.K_ESCAPE:
                    return "RESUME"

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
                    if label == "Resume":
                        return "RESUME"
                    elif label == "Retry":
                        return "RETRY"
                    elif label == "How to Play":
                        self.showing_how_to_play = True
                        return None
                    elif label == "Quit":
                        return "QUIT"
        return None

    def _draw_title(self, screen: pygame.Surface, screen_x: int, screen_y: int) -> None:
        """PAUSEのタイトルを画面中央に描画する。"""
        # PAUSEのタイトルを画面中央に描画
        title_x = (screen_x - self.title_image.get_width()) // 2
        title_y = (screen_y // 30) * 5
        screen.blit(self.title_image, (title_x, title_y))

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
        # その高さに各メニュー項目の行間を加えた値を、1行の高さとして計算
        line_step = item_height + int(item_height * self.ITEM_LINE_SPACE)
        start_y = (screen_y // 30) * 11

        for index, image in enumerate(self.menu_images):
            item_x = (screen_x - image.get_width()) // 2
            item_y = start_y + index * line_step
            screen.blit(image, (item_x, item_y))

            if index == self.selected_index:
                cursor_x = item_x - self.cursor_image.get_width() - 30
                cursor_y = (
                    item_y + (image.get_height() - self.cursor_image.get_height()) // 2
                )
                screen.blit(self.cursor_image, (cursor_x, cursor_y))

    def draw(self, screen: pygame.Surface) -> None:
        """ポーズ画面の描画。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        # How to Playのシーンが表示中の場合は、早期リターン
        if self.showing_how_to_play:
            self.how_to_play_scene.draw(screen)
            return None

        # 背景の透過画像を描画
        screen.blit(self.dithering_surface, (0, 0))
        # 画面の幅と高さを取得
        screen_x, screen_y = screen.get_size()

        self._draw_title(screen, screen_x, screen_y)
        self._draw_menu_item(screen, screen_x, screen_y)
