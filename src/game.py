import pygame
import time

from src.model.base_model.config_model import ConfigModel
from src.model.base_model.scene import Scene
from src.model.scene.mainmenu import MainMenu
from src.model.scene.game_manager import GameManager
from src.model.scene.gameover import GameOver
from src.model.scene.gameclear import GameClear
from src.model.score_manager import ScoreManager


class Game:
    """ゲームのメインクラス。

    Attributes:
        config (ConfigModel): 設定情報を保持するConfigModelオブジェクト
        width (int): 画面の幅
        height (int): 画面の高さ
        screen (pygame.Surface): ゲーム画面のSurfaceオブジェクト
        current_scene (Scene): 現在のシーンを保持するSceneオブジェクト
        running (bool): ゲームが実行中かどうかのフラグ
        pre_time (float): 前回のフレームの時間を保持する変数
        black_bg (pygame.Surface): 黒い背景のSurfaceオブジェクト
        score_manager (ScoreManager): スコア管理を行うScoreManagerオブジェクト
    """
    def __init__(self, config: ConfigModel) -> None:
        pygame.init()
        self.config = config
        self.width = 1920
        self.height = 1080

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.current_scene: Scene

        self.running = True
        self.pre_time: float = time.time()

        self.black_bg = pygame.Surface((self.width, self.height))

        self.score_manager = ScoreManager(config)

    def run(self) -> None:
        """ゲームのメインループを実行する関数。

        ゲームのメインループを実行し、シーンの更新と描画を行う。
        """
        self.current_scene = MainMenu(self.config, self.score_manager)

        while self.running:
            dt = time.time() - self.pre_time
            if dt < 1 / 60:
                time.sleep(1 / 60 - dt)
            self.pre_time = time.time()

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            scene_request = self.current_scene.update(events)

            if scene_request is not None:
                scene_name, data = scene_request

                if scene_name == "MAIN_MENU":
                    # メインメニュー
                    self.current_scene = MainMenu(self.config, self.score_manager)

                elif scene_name == "PLAY":
                    # メニュー → プレイ画面
                    self.current_scene = GameManager(self.config, self.screen, self.score_manager)

                elif scene_name == "GAME_OVER":
                    # プレイ画面 → ゲームオーバー（スコアを渡す）
                    self.current_scene = GameOver(self.config, data, self.score_manager)

                elif scene_name == "GAME_CLEAR":
                    # プレイ画面 → ゲームクリア（スコアを渡す）
                    self.current_scene = GameClear(self.config)
            self.screen.blit(self.black_bg, (0, 0))
            self.current_scene.draw(self.screen)
            pygame.display.flip()
