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
from src.model.base_model.ghost import GhostMode


class GameManager(Scene):
    """ゲームの進行を管理するクラス。

    Attributes:
        game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        map (Map): ゲームのマップを管理するMapオブジェクト
        item_mageer (ItemManager): アイテムの管理を行うItemManagerオブジェクト
        character_manager (CharacterManager): キャラクターの管理を行うCharacterManagerオブジェクト
        pre_time (float): 前回のフレームの時間を保持する変数
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

        self.pre_time = time.time()

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """ゲームの状態を更新する関数。

        各状態（READY、PLAYING、HIT、PAUSE）に応じてゲームの進行を管理し、必要に応じてシーンの変更を要求する。

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            None | tuple[str, Any]:
                ゲームオーバーやゲームクリアなどの状態変化があれば、シーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す。
        """
        # -------- init --------
        self.game_state.events = events
        current_time = time.time()
        self.game_state.dt = current_time - self.pre_time
        self.pre_time = current_time
        scene_request = None

        # pause時は時間経過を止める
        if not self.game_state.game_status == 'PAUSE':
            self.game_state.game_timer += self.game_state.dt

        # debug
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state.current_level += 1
                    self.map.level_up(self.game_state)
                    self.item_mageer.level_up(self.game_state)
                    self.character_manager.level_up(self.game_state)
                    self.game_state.game_status = 'READY'
                    self.game_state.game_timer = 0.0
                if event.key == pygame.K_ESCAPE:
                    self.game_state.game_status = 'PAUSE'

        # ======== PAUSE ========
        if self.game_state.game_status == 'PAUSE':
            scene_request = self._update_pause(self.game_state)

        # ======== READY ========
        if self.game_state.game_status == 'READY':
            scene_request = self._update_ready(self.game_state)

        # ======== PLAYING ========
        if self.game_state.game_status == 'PLAYING':
            scene_request = self._update_playing(self.game_state)

        # ======== HIT ========
        if self.game_state.game_status == 'HIT':
            scene_request = self._update_hit(self.game_state)

        # -------- all object update --------

        # 各オブジェクトのUpdate実行
        self.map.update(self.game_state)
        self.item_mageer.update(self.game_state)
        self.character_manager.update(self.game_state)
        return scene_request

    def draw(self, screen: pygame.Surface) -> None:
        """ゲームの状態を描画する関数。

        Args:
            screen (pygame.Surface): 描画先のpygame.Surfaceオブジェクト。
        """
        self.map.draw(screen)
        self.item_mageer.draw(screen)
        self.character_manager.draw(screen)

#    Private functions

    def _update_ready(self, game_state: GameState) -> None | tuple[str, Any]:
        """READY状態のゲーム進行を管理する関数。

        3秒間の待機後、PLAYING状態に遷移する。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト

        Returns:
            None | tuple[str, Any]: ゲームオーバーやゲームクリアなどの状態変化があれば、シーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す。
        """
        # ゲームオーバー処理 残ライフ
        if self.game_state.lives < 0:
            return ("GAME_OVER", self.game_state.score)

        # ゲーム状態の時間管理　3秒間開始しない
        if 3 < self.game_state.game_timer:
            self.game_state.game_status = 'PLAYING'
            self.game_state.game_timer = 0.0

        return None

    def _update_playing(self, game_state: GameState) -> None | tuple[str, Any]:
        """PLAYING状態のゲーム進行を管理する関数。

        pacmanの移動、ゴーストの移動、アイテムの取得、衝突判定などを行い、必要に応じてシーンの変更を要求する。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト

        Returns:
            None | tuple[str, Any]: ゲームオーバーやゲームクリアなどの状態変化があれば、シーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す。
        """
        # 時間制限処理
        if self.game_state.config.level_max_time < self.game_state.game_timer:
            return ("GAME_OVER", None)

        # ゲームオーバー処理 残ライフ
        if self.game_state.lives < 0:
            return ("GAME_OVER", self.game_state.score)

        # パックガムの取得処理
        item = self.item_mageer.try_eat(self.game_state)
        if item is not None:
            self.game_state.score += item.points
            # SuperPacgum取得時　ゴーストをいじけモードへ
            if type(item) is SuperPacgum:
                self.character_manager.be_scared()

        # Ghostとの衝突判定処理
        ghost = self.character_manager.is_hit(self.game_state)
        if ghost is not None:
            # 通常時
            if ghost.current_mode in (GhostMode.CHASE, GhostMode.SCATTER):
                if not game_state.is_cheat_star:
                    self.game_state.lives -= 1
                    self.game_state.game_status = 'HIT'
                    self.character_manager.hit(self.game_state)
            # 捕食時
            elif ghost.current_mode == GhostMode.SCARED:
                time.sleep(0.5)
                self.game_state.score += self.game_state.config.points_per_ghost
                ghost.be_eaten()

        # level_up条件処理
        if self.item_mageer.is_get_all_items():
            self.game_state.current_level += 1
            self.map.level_up(self.game_state)
            self.item_mageer.level_up(self.game_state)
            self.character_manager.level_up(self.game_state)
            self.game_state.game_status = 'READY'
            self.game_state.game_timer = 0.0

        return None

    def _update_hit(self, game_state: GameState) -> None | tuple[str, Any]:
        """HIT状態のゲーム進行を管理する関数。
        Pacmanがゴーストに当たった後の処理を行い、必要に応じてシーンの変更を要求する。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト

        Returns:
            None | tuple[str, Any]: ゲームオーバーやゲームクリアなどの状態変化があれば、シーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す。
        """
        # ゲーム状態の時間管理　HIT時の点滅処理
        if self.character_manager.pacman_blinking_time <= 0:
            self.character_manager.reset(self.game_state)
            self.game_state.game_status = 'READY'
            self.game_state.game_timer = 0.0

        return None

    def _update_pause(self, game_state: GameState) -> None | tuple[str, Any]:
        """PAUSE状態のゲーム進行を管理する関数。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト

        Returns:
            None | tuple[str, Any]: ゲームオーバーやゲームクリアなどの状態変化があれば、シーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す。
        """
        return None
