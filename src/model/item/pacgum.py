import pygame

from model.game_state import GameState
from src.model.base_model.item import Item


class Pacgum(Item):
    def update(self, game_state: GameState) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_eaten:
            return
