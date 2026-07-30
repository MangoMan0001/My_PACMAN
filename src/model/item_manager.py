import pygame

from src.model.base_model.item import Item
from src.model.game_state import GameState
from src.model.item.pacgum import Pacgum
from src.model.item.super_pacgum import SuperPacgum


class ItemManager:
    def __init__(self, game_state: GameState):
        self.pacgum_count: int = game_state.config.pacgum
        self.pacgum_point: int = game_state.config.points_per_pacgum
        self.super_pacgum_point: int = game_state.config.points_per_super_pacgum

        self.pacgums: list[Pacgum] = self._generate_pacgum()
        self.super_pacgums: list[SuperPacgum] = self._generate_super_pacgum()
        self.item_map: list[list[int]] = self._generate_map()  # 0=通路 1=壁 2＝pacgum 3=super_pacgum

    def update(self, game_state: GameState) -> None:
        pass

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

    def _generate_pacgum(self) -> list[Pacgum]:
        return []

    def _generate_super_pacgum(self) -> list[SuperPacgum]:
        return []

    def _generate_map(self) -> list[list[int]]:
        return []
