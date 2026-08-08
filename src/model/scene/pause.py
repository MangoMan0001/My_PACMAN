import pygame
from pathlib import Path

from src.model.base_model.config_model import ConfigModel
from src.model.image_font import ImageFont


class Pause:
    """ゲーム中のポーズメニューを描画するシーン。

    Attributes:
        selected_index (int): 現在選択されているメニュー項目のインデックス
        title_image (pygame.Surface): ポーズメニューのタイトル画像
        memu_items (list[str]): メニュー項目のリスト
        item_images (list[pygame.Surface]): メニュー項目の画像リスト
        life_image (pygame.Surface): カーソルとして使用する画像
        dithering_surface (pygame.Surface): 透過背景の画像
    """
    CURSOR_SPACE = 30  # カーソルとメニュー項目の間隔
    ITEM_LINE_SPACE = 0.5  # メニュー項目の行間

    def __init__(self, config: ConfigModel) -> None:
        self.config = config
        title_font = ImageFont(Path("pacfont_64"))
        memu_font = ImageFont(Path("nonefont_32"), filename_pattern="none-FONT_{char}.png")

        # メニューの選択インデックス
        self.selected_index: int = 0
        self.title_image = title_font.render_text("PAUSE")
        self.menu_items: list[str] = ["Resume", "Retry", "How to Play", "Cheat Mode", "Quit"]
        self.item_images = [memu_font.render_text(item) for item in self.menu_items]

        # カーソル、透過背景を初期化
        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        cursor_path = str(asset_root / "Pacman" / "PACMAN_right_32.png")
        self.life_image = pygame.image.load(cursor_path).convert_alpha()
        dither_path = str(asset_root / "dither_images" / "dither_surface.png")
        self.dithering_surface = pygame.image.load(dither_path).convert_alpha()

    def reset(self) -> None:
        """ポーズメニューが表示されるたびに、選択インデックスを初期化する。"""
        self.selected_index = 0

    def update(self, events: list[pygame.event.Event]) -> None | str:
        """ ポーズメニューの更新処理。
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            None | tuple[str, Any]:
                ゲームオーバーやゲームクリアなどの状態変化があれば、シーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す。
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # pキーでポーズ解除
                if event.key == pygame.K_ESCAPE:
                    return "RESUME"
                # 上、wキーでメニュー項目の選択
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (
                        self.selected_index - 1) % len(self.menu_items)
                # 下、sキーでメニュー項目の選択
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (
                        self.selected_index + 1) % len(self.menu_items)
                # エンターキーで選択中のメニュー項目をアクティブにする。
                elif event.key == pygame.K_RETURN:
                    label = self.menu_items[self.selected_index]
                    if label == "Resume":
                        return "RESUME"
                    elif label == "Retry":
                        return "RETRY"
                    elif label == "How to Play":
                        return "HOW_TO_PLAY"
                    elif label == "Cheat Mode":
                        return "CHEAT_MODE"
                    elif label == "Quit":
                        return "QUIT"
        return None

    def _title_draw(self, screen: pygame.Surface, screen_x: int, screen_y: int) -> None:
        """PAUSEのタイトルを画面中央に描画する。"""
        # PAUSEのタイトルを画面中央に描画
        title_x = (screen_x - self.title_image.get_width()) // 2
        title_y = (screen_y // 30) * 5
        screen.blit(self.title_image, (title_x, title_y))

    def _menu_item_draw(
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
        item_height = max(item.get_height() for item in self.item_images)
        # その高さに各メニュー項目の行間を加えた値を、1行の高さとして計算
        line_step = item_height + int(item_height * self.ITEM_LINE_SPACE)
        start_y = (screen_y // 30) * 15

        for index, image in enumerate(self.item_images):
            item_x = (screen_x - image.get_width()) // 2
            item_y = start_y + index * line_step
            screen.blit(image, (item_x, item_y))

            if index == self.selected_index:
                cursor_x = item_x - self.life_image.get_width() - 30
                cursor_y = item_y + (
                    image.get_height() - self.life_image.get_height()) // 2
                screen.blit(self.life_image, (cursor_x, cursor_y))

    def draw(self, screen: pygame.Surface) -> None:
        # 背景の透過画像を描画
        screen.blit(self.dithering_surface, (0, 0))
        # 画面の幅と高さを取得
        screen_width, screen_height = screen.get_size()

        self._title_draw(screen, screen_width, screen_height)
        self._menu_item_draw(screen, screen_width, screen_height)
