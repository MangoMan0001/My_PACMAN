"""ゲームのシーンの基底クラスを定義するモジュール."""
import pygame
from abc import ABC, abstractmethod
from typing import Any

from src.model.base_model.config_model import ConfigModel


# --- シーンの基底クラス ---
class Scene(ABC):
    """ゲームのシーンの基底クラス.

    Attributes:
        config (ConfigModel): ゲームの設定を保持するオブジェクト
    """
    def __init__(self, config: ConfigModel):
        """Sceneクラスのコンストラクタ."""
        self.config = config

    @abstractmethod
    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """毎フレーム呼ばれる処理。イベントを処理し、必要に応じて画面遷移を行う.

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            None | tuple[str, Any]:
                画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す

        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """毎フレーム呼ばれる描画処理。画面に描画する.

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        pass
