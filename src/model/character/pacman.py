import pygame

from src.model.game_state import GameState
from src.model.base_model.character import Character


# --- パックマン ---
class Pacman(Character):
    def update(self, game_state: GameState) -> None:
        # game-state内のkeys入力を受けて、game_state.maze と照らし合わせて移動判定
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass
