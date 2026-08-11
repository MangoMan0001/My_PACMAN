import pygame
from typing import Any
from pathlib import Path

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel
from src.model.image_font import ImageFont
from src.model.score_manager import ScoreManager


class GameOver(Scene):
    """ゲームオーバー画面を管理するクラス。

    Attributes:
        score (int): プレイヤーのスコア
        score_manager (ScoreManager): スコアの管理を行うScoreManagerオブジェクト
        max_name_len (int): プレイヤー名の最大文字数
        name_str (str): プレイヤー名の文字列
        is_shift (bool): Shiftキーが押されているかどうかのフラグ
        is_save (bool): スコアが保存されたかどうかのフラグ
        game_over_img (pygame.Surface): "GAME-OVER"のテキスト画像
        score_img (pygame.Surface): スコアのテキスト画像
        save_img (pygame.Surface): "Please input your name. Press Enter to save."のテキスト画像
        main_menu_img (pygame.Surface): "Press Enter to MainMenu"のテキスト画像
        name_img (pygame.Surface): プレイヤー名のテキスト画像
    """
    def __init__(self, config: ConfigModel, score: int, score_manager: ScoreManager):
        super().__init__(config)
        self.score: int = score
        self.score_manager: ScoreManager = score_manager

        self.max_name_len: int = 10
        self.name_str: str = ""

        self.is_shift: bool = False
        self.is_save: bool = False

        title_font = ImageFont(Path("pacfont_256"))
        self.sub_title_font = ImageFont(Path("nonefont_128"), filename_pattern="none-FONT_{char}.png")
        self.mini_title_font = ImageFont(Path("nonefont_64"), filename_pattern="none-FONT_{char}.png")

        game_over_text = "GAME-OVER"
        score_text = "SCORE " + str(score)
        save_text = "Please input your name. Press Enter to save."
        main_menu_text = "Press Enter to MainMenu"

        self.game_over_img = title_font.render_text(game_over_text)
        self.score_img = self.sub_title_font.render_text(score_text)
        self.save_img = self.mini_title_font.render_text(save_text)
        self.main_menu_img = self.sub_title_font.render_text(main_menu_text)

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """ゲームオーバー画面の状態を更新する関数。

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            None | tuple[str, Any]:
                メインメニューに戻る場合は、シーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す。
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.is_shift = True

                if event.key == pygame.K_RETURN:
                    if self.is_save:
                        return ('MAIN_MENU', None)
                    self.is_save = True
                    self.score_manager.save_score(self.name_str, self.score)

                elif event.key == pygame.K_BACKSPACE:
                    self.name_str = self.name_str[:-1]
                else:
                    char = self._unicode(event.key, self.is_shift)

                    if char and len(self.name_str) < self.max_name_len:
                        self.name_str += char

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.is_shift = False

        return None

    def draw(self, screen: pygame.Surface) -> None:
        """ゲームオーバー画面を描画する関数。

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト。
        """
        width = screen.get_width()
        height = screen.get_height()

        cx, cy = width // 2, height // 2
        _, ty = cx // 2, cy // 2
        _, zy = cx // 3, cy // 3
        title_x = cx - self.game_over_img.get_width() // 2
        title_y = cy - self.game_over_img.get_height() // 2

        self.name_img = self.sub_title_font.render_text(self.name_str)

        space_y = 80
        score_width = self.score_img.get_width()
        save_width = self.save_img.get_width()
        save_height = self.save_img.get_height()
        main_menu_width = self.main_menu_img.get_width()
        name_width = self.name_img.get_width()

        screen.blit(self.game_over_img, (title_x, title_y - ty))
        if not self.is_save:
            screen.blit(self.score_img, (cx - score_width // 2, cy))
            screen.blit(self.save_img, (cx - save_width // 2, height - save_height - space_y))
            screen.blit(self.name_img, (cx - name_width // 2, cy + zy))
        else:
            screen.blit(self.main_menu_img, (cx - main_menu_width // 2, cy + ty))

#    Private Methods

    def _unicode(self, key_code: int, is_shift: bool) -> str:
        """キーコードを文字に変換する関数。

        Args:
            key_code (int): pygameのキーコード。
            is_shift (bool): Shiftキーが押されているかどうかのフラグ。

        Returns:
            str: 変換された文字。変換できない場合は空文字を返す。
        """
        if pygame.K_a <= key_code <= pygame.K_z:
            char = chr(key_code)
            return char.lower() if not is_shift else char.upper()

        if pygame.K_0 <= key_code <= pygame.K_9:
            return chr(key_code)

        if pygame.K_SPACE == key_code:
            return " "

        return ""
