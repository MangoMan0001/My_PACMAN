import pygame

from src.model.base_model.entity import Entity
from model.game_state import GameState


class Map(Entity):
    def __init__(self, wall_data: list[list[int]], width) -> None:
        # 16進数や0,1などで構成された壁の配列データ
        self.width =
        self.wall_map: list[list[int]] = wall_data  # 各要素16進数で各方向の壁の有無がリストで記録される
        self.item_map: list[list[int]] = []         # 0=通路 1=壁 2＝pacgum 3=super_pacgum

    def update(self, game_state: GameState) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """mapのみを画面に描画する"""
        pass

    def is_wall(self, x: int, y: int) -> bool:
        """指定された座標が壁かどうかを判定する"""
        return True

    def _generate_items(self, gem_state: GameState) -> list[list[int]]:
        """アイテムの配置データから、PacgumやSuperPacgumのインスタンスを生成して返す"""
        return [[0]]

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理"""
        pass
