import pygame

from src.model.base_model.ghost import Ghost
from src.model.map import Map
from src.model.game_state import GameState
from src.model.character.pacman import Pacman
from src.model.character.blinky import Blinky
from src.model.character.inky import Inky
from src.model.character.clyde import Clyde
from src.model.character.pinky import Pinky


class CharacterManager:
    def __init__(self, game_state: GameState):
        assert game_state.map is not None
        map: Map = game_state.map
        speed = 2
        x, y = map.init_area_pacman()
        px, py = map.area_center(x, y)

        self.pacman: Pacman = Pacman(x, y, px, py, speed)

        bx, by = map.area_center(0, 0)
        px, py = map.area_center(map.x - 1, 0)
        ix, iy = map.area_center(0, map.y - 1)
        cx, cy = map.area_center(map.x - 1, map.y - 1)

        self.ghosts: list[Ghost] = [
            Blinky(0, 0, bx, by, speed, (255, 0, 0), game_state.config.points_per_ghost),
            Pinky(map.x - 1, 0, px, py, speed, (255, 182, 193), game_state.config.points_per_ghost),
            Inky(0, map.y - 1, ix, iy, speed, (0, 255, 255), game_state.config.points_per_ghost),
            Clyde(map.x - 1, map.y - 1, cx, cy, speed, (255, 165, 0), game_state.config.points_per_ghost),
        ]

    def update(self, game_state: GameState) -> None:
        if game_state.game_status == 'READY':
            return
        self.pacman.update(game_state)

        for ghost in self.ghosts:
            ghost.update(game_state)

    def draw(self, screen: pygame.Surface) -> None:
        """自分が持っている全アイテムを描画"""
        self.pacman.draw(screen)

        for ghost in self.ghosts:
            ghost.draw(screen)

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理"""
        self.pacman.level_up(game_state)

        for ghost in self.ghosts:
            ghost.level_up(game_state)


#    Private functions
