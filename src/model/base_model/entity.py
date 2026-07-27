import pygame
from abc import ABC, abstractmethod

from model.game_state import GameState


# --- すべての基底クラス (描画と状態更新のみ) ---
class Entity(ABC):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # game_stateの更新を行う
    @abstractmethod
    def update(self, game_state: GameState) -> None:
        pass

    # 画面に描画する処理（共通）
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
