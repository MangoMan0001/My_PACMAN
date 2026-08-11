"""
- [ ] 現在updateのfor event in events:の中と、Pauseシーンのupdateの両方でPause/Resumeの処理を行っている
Pause中のEnterがデバッグのEnterに吸われてしまうので、削除したらfor event ループの中でPause/Resumeの処理を行うようにする
"""

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
from src.model.item.super_pacgum import SuperPacgum
from src.model.base_model.ghost import GhostMode
from src.model.score_manager import ScoreManager


class GameManager(Scene):
    """ゲームの進行を管理するクラス。

    Attributes:
        game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        map (Map): ゲームのマップを管理するMapオブジェクト
        item_mageer (ItemManager): アイテムの管理を行うItemManagerオブジェクト
        character_manager (CharacterManager): キャラクターの管理を行うCharacterManagerオブジェクト
        pre_time (float): 前回のフレームの時間を保持する変数
        max_time (float): ゲームの最大時間を保持する変数
        pause_scene (Pause): ポーズシーンを管理するPauseオブジェクト
        paused (bool): ゲームがポーズ中かどうかを示すフラグ
        pause_start_time (float): ポーズ開始時刻を保持する変数
        hud (HUD): ヘッドアップディスプレイを管理するHUDオブジェクト
        is_invincible (bool): 無敵状態かどうかを示すフラグ
    """

    def __init__(
        self, config: ConfigModel, screen: pygame.Surface, score_manager: ScoreManager
    ) -> None:
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
        self.pause_scene: Pause = Pause()

        # HUDの初期化
        self.hud: HUD = HUD(config, score_manager.get_highscore())

        # ゲームの経過時間を管理する変数の初期化
        self.pre_time = time.time()
        self.max_time = self.game_state.config.level_max_time

        # チートフラグ
        self.is_invincible: bool = False

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
        if self.game_state.game_status != "PAUSE":
            self.game_state.game_timer += self.game_state.dt

        # ======== READY ========
        if self.game_state.game_status == "READY":
            scene_request = self._update_ready(self.game_state)

        # ======== PLAYING ========
        if self.game_state.game_status == "PLAYING":
            scene_request = self._update_playing(self.game_state)

        # ======== HIT ========
        if self.game_state.game_status == "HIT":
            scene_request = self._update_hit(self.game_state)

        # ======== PAUSE ========
        if self.game_state.game_status == "PAUSE":
            scene_request = self._update_pause(self.game_state)
            return scene_request

        # -------- key event --------
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state.is_cheating = True
                    print("cheating")
                if self.game_state.is_cheating:
                    if event.key == pygame.K_1:
                        print("star")
                        self.game_state.is_cheat_star = (
                            not self.game_state.is_cheat_star
                        )
                    if event.key == pygame.K_2:
                        print("skip")
                        self.game_state.is_cheat_skip = True
                    if event.key == pygame.K_3:
                        print("froze")
                        self.game_state.is_cheat_frozen = (
                            not self.game_state.is_cheat_frozen
                        )
                    if event.key == pygame.K_4:
                        print("1up")
                        self.game_state.is_cheat_1up = True
                    if event.key == pygame.K_5:
                        print("dash")
                        self.game_state.is_cheat_dash = (
                            not self.game_state.is_cheat_dash
                        )

                # Escapeが押された時PLAYING<->PAUSEを切り替える
                if event.key == pygame.K_ESCAPE:
                    if self.game_state.game_status == "PLAYING":
                        self.game_state.game_status = "PAUSE"

        # -------- cheating --------
        if self.game_state.is_cheating:
            self._cheating()

        # -------- all object update --------
        # 各オブジェクトのUpdate実行
        self.map.update(self.game_state)
        self.item_manager.update(self.game_state)
        self.character_manager.update(self.game_state)
        self.hud.update(self.game_state)
        return scene_request

    def draw(self, screen: pygame.Surface) -> None:
        """ゲームの状態を描画する関数。

        Args:
            screen (pygame.Surface): 描画先のpygame.Surfaceオブジェクト。
        """
        self.map.draw(screen)
        self.item_manager.draw(screen)
        self.character_manager.draw(screen)
        self.hud.draw(screen)
        if self.game_state.game_status == "PAUSE":
            self.pause_scene.draw(screen)

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
            if game_state.is_cheating:
                return ("GAME_OVER", 0)
            return ("GAME_OVER", self.game_state.score)

        # ゲーム状態の時間管理　3秒間開始しない
        if 3 < self.game_state.game_timer:
            self.game_state.game_status = "PLAYING"
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
            self.game_state.lives -= 1
            self.game_state.game_status = "HIT"
            self.character_manager.hit(self.game_state)

        # ゲームオーバー処理 残ライフ
        if self.game_state.lives < 0:
            if game_state.is_cheating:
                return ("GAME_OVER", 0)
            return ("GAME_OVER", self.game_state.score)

        # パックガムの取得処理
        item = self.item_manager.try_eat(self.game_state)
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
                if not self.is_invincible:
                    self.game_state.lives -= 1
                    self.game_state.game_status = "HIT"
                    self.character_manager.hit(self.game_state)
            # 捕食時
            elif ghost.current_mode == GhostMode.SCARED:
                time.sleep(0.5)
                self.game_state.score += self.game_state.config.points_per_ghost
                ghost.be_eaten()

        # level_up条件処理
        if self.item_manager.is_get_all_items():
            self._level_up()

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
            self.game_state.game_status = "READY"
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
        action = self.pause_scene.update(game_state.events)
        if action == "RESUME":
            self.game_state.game_status = "PLAYING"
            return None
        elif action == "RETRY":
            return ("PLAY", None)
        elif action == "QUIT":
            return ("MAIN_MENU", None)
        return None

    def _cheating(self) -> None:
        """チートモードの処理を行う関数。"""
        # 無敵
        self.is_invincible = self.game_state.is_cheat_star

        # ステージスキップ
        if self.game_state.is_cheat_skip:
            self._level_up()
            self.game_state.is_cheat_skip = False

        # ゴーストの凍結
        self.character_manager.is_frozen = self.game_state.is_cheat_frozen

        # 追加ライフ
        if self.game_state.is_cheat_1up:
            if self.game_state.lives < 5:
                self.game_state.lives += 1
            self.game_state.is_cheat_1up = False

        # スピードアップ
        if self.game_state.is_cheat_dash:
            self.character_manager.pacman.dash()
        elif not self.game_state.is_cheat_dash:
            self.character_manager.pacman.walk()

    def _level_up(self) -> None:
        """レベルアップ処理を行う関数。"""
        self.game_state.current_level += 1
        self.map.level_up(self.game_state)
        self.item_manager.level_up(self.game_state)
        self.character_manager.level_up(self.game_state)
        self.game_state.game_status = "READY"
        self.game_state.game_timer = 0.0
