"""ゲーム情報共通クラス."""
from __future__ import annotations
import pygame
from typing import TYPE_CHECKING, Literal

from src.model.base_model.config_model import ConfigModel

if TYPE_CHECKING:
    from src.model.map import Map
    from src.model.character.pacman import Pacman
    from src.model.base_model.ghost import Ghost
    from src.model.item_manager import ItemManager

STATUS = Literal['READY', 'PLAYING', 'HIT', 'PAUSE']


# --- ゲームの状態をすべて持つデータクラス ---
class GameState:
    """ゲームの状態を保持するクラス.

    Attributes:
        config (ConfigModel): ゲームの設定を保持するConfigModelオブジェクト
        map (Map | None): ゲームのマップを管理するMapオブジェクト
        item (ItemManager | None): アイテムの管理を行うItemManagerオブジェクト
        pacman (Pacman | None): Pacmanのインスタンス
        ghosts (list[Ghost]): 4匹のGhostのインスタンスをリストで保持
        game_status (STATUS): ゲームの現在の状態（READYまたはPLAYING）
        current_level (int): ステージの現在レベル
        events (list[pygame.event.Event]): pygameのイベントリスト
        score (int): 現在のスコア
        lives (int): 残機数
        dt (float): 前回フレームからの経過時間
        game_timer (float): 進行中ゲームの経過時間
    """
    def __init__(self, config: ConfigModel):
        """GameStateクラスのコンストラクタ."""
        # === OBJECT ===
        self.config: ConfigModel = config           # configオブジェクト
        self.map: Map | None = None                 # Mapオブジェクト
        self.item: ItemManager | None = None        # Itemsオブジェクト
        self.pacman: Pacman | None = None           # Pacmanオブジェクト
        self.ghosts: list[Ghost] = []               # 4匹のGhostのインスタンスをリストで保持

        # === GAME PRAMETER ===
        self.game_status: STATUS = 'READY'          # GAMEの現在の状態
        self.current_level: int = 0                 # ステージの現在レベル
        self.events: list[pygame.event.Event] = []  # key入力情報
        self.score: int = 0                         # current score
        self.lives: int = config.lives              # 残機数

        self.dt: float = 0.0                        # 前回フレームからの経過時間
        self.game_timer: float = 0.0                # 進行中ゲームの経過時間

        # === CHEAT PRAMETER ===
        self.is_cheating: bool = False              # チートフラグ
        self.is_cheat_star: bool = False            # チートフラグ 無敵化
        self.is_cheat_skip: bool = False            # チートフラグ ステージスキップ
        self.is_cheat_frozen: bool = False          # チートフラグ ゴースト凍結
        self.is_cheat_1up: bool = False             # チートフラグ 追加ライフ
        self.is_cheat_dash: bool = False            # チートフラグ パックマンスピードアップ
