import pygame
import time
from typing import Any

from src.model.base_model.config_model import ConfigModel
from src.model.base_model.scene import Scene
from src.model.map import Map
from src.model.item_manager import ItemManager
from src.model.character_manager import CharacterManager
from src.model.game_state import GameState
from src.model.scene.pause import Pause
from src.model.scene.hud import HUD


class GameManager(Scene):
    """ゲームの進行を管理するクラス。

    Attributes:
        game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        map (Map): ゲームのマップを管理するMapオブジェクト
        item_manager (ItemManager): アイテムの管理を行うItemManagerオブジェクト
        character_manager (CharacterManager): キャラクターの管理を行うCharacterManagerオブジェクト
        time (float): ゲームの経過時間を保持する変数
        start_time (float): ゲームの開始時間を保持する変数
    """
    def __init__(self, config: ConfigModel, screen: pygame.Surface) -> None:
        super().__init__(config)
        self.game_state: GameState = GameState(config)

        # Mapの初期化、GameStateにセット
        self.map: Map = Map(self.game_state, screen)
        self.game_state.map = self.map

        # ItemManagerの初期化、GameStateにセット
        self.item_manager: ItemManager = ItemManager(self.game_state)
        self.game_state.item = self.item_manager

        # CharacterManagerの初期化、GameStateにセット
        self.character_manager: CharacterManager = CharacterManager(self.game_state)
        self.game_state.pacman = self.character_manager.pacman
        self.game_state.ghosts = self.character_manager.ghosts

        # Pauseシーンの初期化
        self.pause_scene: Pause = Pause(config)
        self.paused: bool = False
        self.pause_start_time: float = 0.0  # ポーズ開始時刻を保持する変数

        # HUDの初期化
        # highscoreにどっかからhighscoreを取得する処理いれる
        # self.hud: HUD = HUD(highscore)
        self.hud: HUD = HUD(100)  # 仮のハイスコアを設定

        # ゲームの経過時間を管理する変数の初期化
        self.time = time.time()
        self.start_time = time.time()
        self.max_time = self.game_state.config.level_max_time

    def _resume(self) -> None:
        """ゲームを再開するための処理。

        GameStateに時間が保持されたら破棄できるかも
        """
        # pause_start_timeを使って経過時間を調整する
        pause_duration = time.time() - self.pause_start_time
        self.start_time += pause_duration
        self.time += pause_duration
        self.paused = False

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """ゲームの状態を更新する関数。

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            None | tuple[str, Any]:
                ゲームオーバーやゲームクリアなどの状態変化があれば、シーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す。
        """
        # debug
        # debugに実際の処理を追加してます。
        self.game_state.events = events

        # ポーズ中の処理を優先して行う
        if self.paused:
            action = self.pause_scene.update(events)
            if action == "RESUME":
                self._resume()
                return None
            elif action == "RETRY":
                return ("PLAY", None)
            elif action == "HOW_TO_PLAY":
                # How to Playのシーンに遷移する処理をここに追加する
                pass
            elif action == "CHEAT_MODE":
                # Cheat ModeのフラグをここでON？HUDの表示も変える
                pass
            elif action == "QUIT":
                return ("MAIN_MENU", None)
            return None

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.paused:
                        self._resume()
                    else:
                        self.paused = True
                        self.pause_start_time = time.time()
                        self.pause_scene.reset()
                elif event.key == pygame.K_RETURN:
                    self.game_state.current_level += 1
                    self.map.level_up(self.game_state)
                    self.item_manager.level_up(self.game_state)
                    self.character_manager.level_up(self.game_state)
                    self.game_state.game_status = 'READY'
                    self.time = time.time()
                    self.start_time = time.time()

        # ゲーム状態のフラグ管理　3秒間開始しない
        current_time = time.time()
        if 3 < current_time - self.time:
            self.game_state.game_status = 'PLAYING'

        # 時間制限処理
        if self.max_time < current_time - self.start_time:
            return ("GAME_OVER", None)

        # パックガムの取得処理
        item = self.item_manager.try_eat(self.game_state)
        if item is not None:
            self.game_state.score += item.points
            print(self.game_state.score)

        # Ghostとの衝突判定処理
        if self.character_manager.is_hit(self.game_state):
            self.character_manager.hit(self.game_state)
            self.game_state.lives -= 1
            print(self.game_state.lives)
            self.game_state.game_status = 'READY'
            self.time = time.time()
            self.start_time = time.time()

        if self.game_state.lives < 0:
            return ("GAME_OVER", None)

        # level_up条件処理
        if self.item_manager.is_get_all_items():
            self.game_state.current_level += 1
            self.map.level_up(self.game_state)
            self.item_manager.level_up(self.game_state)
            self.character_manager.level_up(self.game_state)
            self.game_state.game_status = 'READY'
            self.start_time = time.time()
            self.time = time.time()

        # 各オブジェクトのUpdate実行
        self.map.update(self.game_state)
        self.item_manager.update(self.game_state)
        self.character_manager.update(self.game_state)
        # GameStateのマージに合わせて、remaining_timeを削除する予定
        self.hud.update(self.game_state, self.max_time - (current_time - self.start_time))
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """ゲームの状態を描画する関数。

        Args:
            screen (pygame.Surface): 描画先のpygame.Surfaceオブジェクト。
        """
        self.map.draw(screen)
        self.item_manager.draw(screen)
        self.character_manager.draw(screen)
        self.hud.draw(screen)
        if self.paused:
            self.pause_scene.draw(screen)
