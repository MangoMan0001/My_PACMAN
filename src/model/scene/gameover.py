import pygame
from typing import Any
from pathlib import Path

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel
from src.model.image_font import ImageFont


class GameOver(Scene):
    def __init__(self, config: ConfigModel, score: int):
        super().__init__(config)
        self.score: int = score
        self.width: int = 0
        self.hight: int = 0

        game_over_font = ImageFont(Path("pacfont_256"))
        your_score_font = ImageFont(Path("misakifont_64"))
        # self.number_font = ImageFont(
        #     Path("nonefont_32"), filename_pattern="none-FONT_{char}.png"
        # )

        game_over_text = "GAME-OVER"
        score_text = "SCORE"
        raw_score_text = str(score)
        # self.menu_text = ["PLAY", "QUIT"]

        # # cursor用に使用。
        # asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        # cursor_path = str(asset_root / "Pacman" / "PACMAN_right_32.png")

        # convert_alpha()を使ってmlxと同じく透過情報を持つSurfaceに変換する。
        # self.cursor_image = pygame.image.load(cursor_path).convert_alpha()
        self.game_over_img = game_over_font.render_text(game_over_text)
        self.score_img = your_score_font.render_text(score_text)
        self.raw_socre_img = your_score_font.render_text(raw_score_text)
        # self.item_images = [
        #     menu_font.render_text(label) for label in self.menu_text
        # ]

        # # 選択中のメニュー項目のインデックスを初期化
        # self.selected_index = 0

        # # のちのちハイスコアの表示に使う。 -> 必要なくなったかも
        # self.scores: dict[str, int] = self._set_highscore()

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す
        """

        pass

    def draw(self, screen: pygame.Surface) -> None:
        width = screen.get_width()
        height = screen.get_height()

        cx, cy = width // 2, height // 2
        tx, ty = cx // 2, cy // 2
        base_x = cx - self.game_over_img.get_width() // 2
        base_y = cy - self.game_over_img.get_height() // 2

        screen.blit(self.game_over_img, (base_x, base_y - ty))
        screen.blit(self.score_img, (cx, cy))
        # screen.blit(self.game_over_img, (base_x, base_y - ty))
        print(self.score_img.get_width())
        import sys
        sys.exit(1)
