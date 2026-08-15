"""Pacmanゲームの基底クラスを定義するモジュール."""
import pygame
from abc import ABC, abstractmethod

from src.model.game_state import GameState


# --- すべての基底クラス (描画と状態更新のみ) ---
class Entity(ABC):
    """キャラクターやアイテムの基底クラス.

    Attributes:
        x (int): セル単位でのx座標
        y (int): セル単位でのy座標
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # game_stateをもとにオブジェクトの更新を行う
    @abstractmethod
    def update(self, game_state: GameState) -> None:
        """各オブジェクトの状態を更新する.

        Args:
            game_state (GameState): ゲームの状態を保持するオブジェクト
        """
        pass

    # 画面に描画する処理（共通）
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """各オブジェクトを画面に描画する.

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        pass
