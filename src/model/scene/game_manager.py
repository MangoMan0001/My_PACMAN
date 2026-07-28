import pygame
from typing import List, Optional

from src.model.base_model.config_model import ConfigModel
from src.model.base_model.entity import Entity
from src.model.base_model.scene import Scene
from src.model.map import Map
from src.model.game_state import GameState
from src.model.character.pacman import Pacman
from src.model.character.blinky import Blinky
from src.model.character.pinky import Pinky
from src.model.character.inky import Inky
from src.model.character.clyde import Clyde


class GameManager(Scene):
    def __init__(self, config: ConfigModel) -> None:
        super().__init__(config)
        # 1. マップの生成
        self.game_map: Map = Map(level=config.level, seed=config.seed)

        # 2. パックマンの生成
        self.pacman: Pacman = Pacman(32, 32, 2)

        # 3. GameStateの生成 (全員に配る共通情報)
        self.game_state: GameState = GameState(self.game_map, self.pacman)

        # 4. アイテムとゴーストの生成
        self.items: List[Entity] = self.game_map.generate_items(item_data)
        self.ghosts: List[Entity] = [
            Blinky(128, 128, 2, "RED"),
            Pinky(160, 128, 2, "PINK"),
            Inky(192, 128, 2, "CYAN"),
            Clyde(224, 128, 2, "ORANGE")
        ]

        # 🌟 超重要：すべてのEntityを1つのリストにまとめる！ 🌟
        # 描画したい順（アイテム → ゴースト → パックマンが一番上）に追加します
        self.entities: List[Entity] = []
        self.entities.extend(self.items)
        self.entities.extend(self.ghosts)
        self.entities.append(self.pacman)

    def update(self, keycode: Optional[int]) -> None:
        """毎フレーム呼ばれる処理"""
        # 今のキー入力をGameStateにセット
        self.game_state.keycode = keycode

        # 全Entityのupdateを一気に呼び出す！ (各自がGameStateを見て勝手に動く)
        for entity in self.entities:
            entity.update(self.game_state)

        # ここで当たり判定（ガムを食べたか、ゴーストに当たったか）の処理を行う
        self._check_collisions()

        # レベルクリア判定
        self._check_level_clear()

    def _check_collisions(self) -> None:
        # パックマンとゴーストの衝突判定などをここに書く
        pass

    def _check_level_clear(self) -> None:
        # 残りのガム(is_eaten == False)の数を数え、0ならマップ再生成などの処理
        pass

    def draw(self, screen: pygame.Surface) -> None:
        # 1. 一番下に壁を描く
        self.game_map.draw(screen)

        # 2. その上に全Entityを一気に描画する！
        for entity in self.entities:
            entity.draw(screen)
