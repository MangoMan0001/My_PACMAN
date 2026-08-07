import pygame
import time
from typing import Any

from src.model.base_model.config_model import ConfigModel
from src.model.base_model.scene import Scene
from src.model.map import Map
from src.model.item_manager import ItemManager
from src.model.character_manager import CharacterManager
from src.model.game_state import GameState
from src.model.item.super_pacgum import SuperPacgum


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

        self.map: Map = Map(self.game_state, screen)
        self.game_state.map = self.map

        self.item_mageer: ItemManager = ItemManager(self.game_state)
        self.game_state.item = self.item_mageer

        self.character_manager: CharacterManager = CharacterManager(self.game_state)
        self.game_state.pacman = self.character_manager.pacman
        self.game_state.ghosts = self.character_manager.ghosts

        self.time = time.time()
        self.start_time = time.time()

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
        self.game_state.events = events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state.current_level += 1
                    self.map.level_up(self.game_state)
                    self.item_mageer.level_up(self.game_state)
                    self.character_manager.level_up(self.game_state)
                    self.game_state.game_status = 'READY'
                    self.time = time.time()
                    self.start_time = time.time()

        # ゲーム状態のフラグ管理　3秒間開始しない
        current_time = time.time()
        if 3 < current_time - self.time:
            self.game_state.game_status = 'PLAYING'

        # 時間制限処理
        if self.game_state.config.level_max_time < current_time - self.start_time:
            return ("GAME_OVER", None)

        # パックガムの取得処理
        item = self.item_mageer.try_eat(self.game_state)
        if item is not None:
            self.game_state.score += item.points
            # SuperPacgum取得時　ゴーストをいじけモードへ
            if type(item) is SuperPacgum:
                self.character_manager.be_scared()

        # Ghostとの衝突判定処理
        if self.character_manager.is_hit(self.game_state):
            # 捕食時
            if self.character_manager.is_eaten():
                self.game_state.score += self.game_state.config.points_per_ghost
            # 通常時
            elif:
                self.character_manager.hit(self.game_state)
                self.game_state.lives -= 1
                self.game_state.game_status = 'READY'
                self.time = time.time()
                self.start_time = time.time()

        # ゲームオーバー処理 残ライフ
        if self.game_state.lives < 0:
            return ("GAME_OVER", self.game_state.score)

        # level_up条件処理
        if self.item_mageer.is_get_all_items():
            self.game_state.current_level += 1
            self.map.level_up(self.game_state)
            self.item_mageer.level_up(self.game_state)
            self.character_manager.level_up(self.game_state)
            self.game_state.game_status = 'READY'
            self.start_time = time.time()
            self.time = time.time()

        # 各オブジェクトのUpdate実行
        self.map.update(self.game_state)
        self.item_mageer.update(self.game_state)
        self.character_manager.update(self.game_state)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """ゲームの状態を描画する関数。

        Args:
            screen (pygame.Surface): 描画先のpygame.Surfaceオブジェクト。
        """
        self.map.draw(screen)
        self.item_mageer.draw(screen)
        self.character_manager.draw(screen)

#    Private functions
