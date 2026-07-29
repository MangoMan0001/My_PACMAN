from __future__ import annotations
import pygame
from typing import TYPE_CHECKING


from src.model.base_model.config_model import ConfigModel

if TYPE_CHECKING:
    from src.model.map import Map
    from src.model.character.pacman import Pacman
    from src.model.base_model.ghost import Ghost
    from src.model.item_manager import ItemManager


# --- ゲームの状態をすべて持つデータクラス ---
class GameState:
    def __init__(self, config: ConfigModel):

        # === OBJECT ===
        self.config: ConfigModel = config           # configオブジェクト
        self.map: Map | None = None                 # Mapオブジェクト
        self.item: ItemManager                      # Itemsオブジェクト
        self.pacman: Pacman                         # Pacmanオブジェクト
        self.ghosts: list[Ghost] = []               # 4匹のGhostのインスタンスをリストで保持
        self.screen: pygame.Surface | None = None

        # === GAME STATUS ===
        self.current_level: int = 0                 # ステージの現在レベル
        self.keys: list[int] = []                   # key入力情報
        self.score: int = 0                         # current score
