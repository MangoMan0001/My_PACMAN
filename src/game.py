import pygame

from src.model.base_model.config_model import ConfigModel
from src.model.base_model.scene import Scene
from src.model.scene.mainmenu import MainMenu
from src.model.scene.game_manager import GameManager
from src.model.scene.gameover import GameOver
from src.model.scene.gameclear import GameClear
from src.model.scene.pause import Pause


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

        self.current_scene: Scene

        self.running = True

    def run(self, config: ConfigModel) -> None:
        self.current_scene = MainMenu(config)

        while self.running:
            events = pygame.event.get()
            print(type(events))
            import sys
            sys.exit(1)

            scene_request = self.current_scene.update(events)

            if scene_request is not None:
                scene_name, data = scene_request

                if scene_name == "MAIN_MENU":
                    # メインメニュー
                    self.current_scene = MainMenu(config)

                elif scene_name == "PLAY":
                    # メニュー → プレイ画面
                    self.current_scene = GameManager(config)

                elif scene_name == "GAME_OVER":
                    # プレイ画面 → ゲームオーバー（スコアを渡す）
                    self.current_scene = GameOver(config, score=data)

                elif scene_name == "PAUSE":
                    # プレイ画面 → ゲームポーズ
                    self.current_scene = Pause(config)

                elif scene_name == "GAME_CLEAR":
                    # プレイ画面 → ゲームクリア（スコアを渡す）
                    self.current_scene = GameClear(config)

            self.current_scene.draw(self.screen)
            pygame.display.flip()
