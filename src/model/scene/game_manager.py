import pygame
from typing import List, Optional, Any

from src.model.base_model.config_model import ConfigModel
from src.model.base_model.entity import Entity
from src.model.base_model.scene import Scene
from src.model.map import Map
from src.model.item_manager import ItemManager
from src.model.game_state import GameState
from src.model.character.pacman import Pacman
from src.model.character.blinky import Blinky
from src.model.character.pinky import Pinky
from src.model.character.inky import Inky
from src.model.character.clyde import Clyde


class GameManager(Scene):
    def __init__(self, config: ConfigModel) -> None:
        super().__init__(config)
        self.game_state: GameState = GameState(config)

        self.map: Map = Map(self.game_state)
        self.game_state.map = self.map

        self.item_mageer: ItemManager = ItemManager(self.game_state)

        # self.pacman: Pacman = Pacman(32, 32, 2)

        # self.items: List[Entity] = self.game_map.generate_items(item_data)
        # self.ghosts: List[Entity] = [
        #     Blinky(128, 128, 2, "RED"),
        #     Pinky(160, 128, 2, "PINK"),
        #     Inky(192, 128, 2, "CYAN"),
        #     Clyde(224, 128, 2, "ORANGE")
        # ]

        # self.entities: List[Entity] = []
        # self.entities.extend(self.items)
        # self.entities.extend(self.ghosts)
        # self.entities.append(self.pacman)

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """毎フレーム呼ばれる処理"""

        # debug
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state.current_level += 1
                    self.map.level_up(self.game_state)

        self.map.update(self.game_state)
        self.item_mageer.update(self.game_state)
        return None
        # self.game_state.keycode = keycode

        # for entity in self.entities:
        #     entity.update(self.game_state)

        # self._check_collisions()

        # self._check_level_clear()

    def draw(self, screen: pygame.Surface) -> None:
        self.map.draw(screen)
        self.item_mageer.draw(screen)
        pass
        # self.game_map.draw(screen)

        # for entity in self.entities:
        #     entity.draw(screen)

#    Private functions

    def _check_collisions(self) -> None:
        # パックマンとゴーストの衝突判定などをここに書く
        pass

    def _check_level_clear(self) -> None:
        # 残りのガム(is_eaten == False)の数を数え、0ならマップ再生成などの処理
        pass
