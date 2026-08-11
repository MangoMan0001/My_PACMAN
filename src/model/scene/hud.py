"""ゲーム中、画面に情報を表示するHUDを描画するモジュール。"""
import pygame
from typing import Any
from pathlib import Path

from src.model.base_model.config_model import ConfigModel
from src.model.image_font import ImageFont


class HUD:
    """ゲーム中のHUD(スコア、ハイスコア、残機、レベル、残り時間)を描画するシーン。

    Attributes:
        highscore (int): ハイスコア。
        hud_font (ImageFont): HUD描画用のフォント。
        life_image (pygame.Surface): 残機描画用の画像。
    """

    def __init__(self, config: ConfigModel, highscore: int) -> None:
        """HUDの初期化。

        Args:
            config (ConfigModel): 設定モデル。
            highscore (int): ハイスコア。
        """
        self.config = config
        self.highscore = highscore
        self.hud_font = ImageFont(
            Path("nonefont_32"), filename_pattern="none-FONT_{char}.png"
        )

        # 残機表示用
        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        life_path = str(asset_root / "Pacman" / "PACMAN_right_32.png")
        self.life_image = pygame.image.load(life_path).convert_alpha()

        self.score = 0
        self.level = 1
        self.lives = self.config.lives
        self.remaining_time = self.config.level_max_time

        # チートフラグ
        self.is_cheating: bool = False
        # チートフラグ描画用テキスト画像
        cheat_font = ImageFont(Path("pacfont_64"))
        self.cheat_image = cheat_font.render_text("CHEAT")

        # 各チートの状態
        self.cheat_dict = {
            "star": False,
            "skip": False,
            "frozen": False,
            "1up": False,
            "dash": False,
        }
        # 各チートの状態表示用フォント
        self.cheat_on_font = ImageFont(Path("pacfont_32"))
        self.cheat_off_font = ImageFont(Path("pacfont_32_gray"))

    def update(self, game_state: Any) -> None:
        """
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す
        """
        if game_state.is_cheating:
            self.is_cheating = True
            for cheat in self.cheat_dict.keys():
                self.cheat_dict[cheat] = getattr(game_state, f"is_cheat_{cheat}")
        # 過去のハイスコアを現在プレイ中のスコアが上回った場合、ハイスコアを更新
        self.highscore = max(self.highscore, game_state.score)
        self.score = game_state.score
        self.level = game_state.current_level
        self.lives = game_state.lives
        if game_state.game_status == "PLAYING":
            self.remaining_time = (
                game_state.config.level_max_time - game_state.game_timer
            )
        elif game_state.game_status == "READY":
            self.remaining_time = game_state.config.level_max_time

    def draw(self, screen: pygame.Surface) -> None:
        """HUDを描画する。

        画面の上部にSCORE、HIGHSCORE、TIMEを描画し、画面の下部に残機を描画する。
        現在画面サイズから描画位置を計算しているが、get_width()/get_height()の使用は確認。
        画面サイズが変わってHUDとマップが被る場合、調整必須。

        Args:
            screen (pygame.Surface): 描画先のSurface。
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト。
            remaining_time (float): 残り時間。
        """
        # HUDのテキストの高さを計算(SCORE, HIGHSCORE, TIMEは共通)
        hud_text_y = (screen.get_height() // 30) * 2

        # 現在のスコアを描画
        score_x = (screen.get_width() // 30) * 10
        score_image = self.hud_font.render_text(f"{self.score}")
        screen.blit(score_image, (score_x, hud_text_y + 20))

        # ハイスコアを描画
        highscore_text_image = self.hud_font.render_text("HIGHSCORE")
        highscore_x = (screen.get_width() - highscore_text_image.get_width()) // 2
        screen.blit(highscore_text_image, (highscore_x, hud_text_y))
        highscore_image = self.hud_font.render_text(f"{self.highscore}")
        highscore_x = (screen.get_width() - highscore_image.get_width()) // 2
        screen.blit(highscore_image, (highscore_x, hud_text_y + 20))

        # 残り時間を描画
        time_x = (screen.get_width() // 30) * 20
        time_image = self.hud_font.render_text(f"{int(self.remaining_time)}")
        screen.blit(time_image, (time_x, hud_text_y + 20))

        # レベルを描画
        level_image = self.hud_font.render_text(f"{self.level}")
        level_x = (screen.get_width() // 30) * 21
        level_y = screen.get_height() - level_image.get_height() - 30
        screen.blit(level_image, (level_x, level_y))

        # 残機を描画
        for i in range(self.lives):
            life_x = (screen.get_width() // 30) * (i + 9)
            life_y = screen.get_height() - self.life_image.get_height() - 30
            screen.blit(self.life_image, (life_x, life_y))

        # チートフラグが有効な場合、画面右上にCHEATと各チートの状態を描画
        if self.is_cheating:
            cheat_x = (screen.get_width() - self.cheat_image.get_width()) - 100
            cheat_y = (screen.get_height() // 30) * 2
            screen.blit(self.cheat_image, (cheat_x, cheat_y))
            for i, (cheat_name, flag) in enumerate(self.cheat_dict.items()):
                cheat_name = cheat_name.upper()
                if flag:
                    cheat_name_image = self.cheat_on_font.render_text(cheat_name)
                else:
                    cheat_name_image = self.cheat_off_font.render_text(cheat_name)
                cheat_name_x = (screen.get_width() - cheat_name_image.get_width()) - 100
                cheat_name_y = (screen.get_height() // 30) * (5 + i)
                screen.blit(cheat_name_image, (cheat_name_x, cheat_name_y))
