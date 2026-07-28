import pygame

from src.model.base_model.item import Item
from src.model.game_state import GameState


class ItemManager:
    def __init__(self, pacgum_count: int, pacgum_point: int,
                 super_pacgum_point: int):
        self.pacgums: list[Item] = []  # pacgumオブジェクトのリスト
        self.super_pacgums: list[Item] = []

        self.pacgum_count: int = pacgum_count
        self.pacgum_point: int = pacgum_point
        self.super_pacgum_point: int = super_pacgum_point

        self.item_map: list[list[int]] = []  # 0=通路 1=壁 2＝pacgum 3=super_pacgum

        self._generate_pacgum()

    def draw(self, screen: pygame.Surface) -> None:
        """自分が持っている全アイテムを描画"""
        for item in self.pacgums:
            item.draw(screen)

        for item in self.super_pacgums:
            item.draw(screen)

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理"""
        pass

#    Private functions

    def _generate_pacgum(self) -> None:
        pass

    def _generate_items(self) -> None:
        pass
