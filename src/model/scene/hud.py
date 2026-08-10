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
        self.hud_font = ImageFont(Path("nonefont_32"), filename_pattern="none-FONT_{char}.png")

        # 残機表示用
        asset_root = Path(__file__).resolve().parents[3] / "data" / "assets"
        life_path = str(asset_root / "Pacman" / "PACMAN_right_32.png")
        self.life_image = pygame.image.load(life_path).convert_alpha()

        self.score = 0
        self.lives = self.config.lives
        self.remaining_time = config.level_max_time

    def update(self, game_state: Any) -> None:
        """
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す
        """
        self.score = game_state.score
        self.lives = game_state.lives
        if game_state.game_status == "PLAYING":
            self.remaining_time = game_state.config.level_max_time - game_state.game_timer
        elif game_state.game_status == "READY":
            self.remaining_time = game_state.config.level_max_time
        # 過去のハイスコアを現在プレイ中のスコアが上回った場合、ハイスコアを更新
        if self.highscore < game_state.score:
            self.highscore = game_state.score

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
        # score_text_image = self.hud_font.render_text("SCORE")
        score_x = (screen.get_width() // 30) * 10
        # screen.blit(score_text_image, (score_x, hud_text_y))
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
        # time_text_image = self.hud_font.render_text("TIME")
        time_x = (screen.get_width() // 30) * 20
        # screen.blit(time_text_image, (time_x, hud_text_y))
        time_image = self.hud_font.render_text(f"{int(self.remaining_time)}")
        screen.blit(time_image, (time_x, hud_text_y + 20))

        # 残機を描画
        for i in range(self.lives):
            life_x = (screen.get_width() // 30) * (i + 10)
            life_y = screen.get_height() - self.life_image.get_height() - 10
            screen.blit(self.life_image, (life_x, life_y))
