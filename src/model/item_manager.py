import pygame
import random
from enum import IntEnum
from typing import Optional

from src.model.base_model.item import Item
from src.model.map import Map
from src.model.game_state import GameState
from src.model.item.pacgum import Pacgum
from src.model.item.super_pacgum import SuperPacgum
from src.model.character.pacman import Pacman


class CellType(IntEnum):
    """セルの種類を表す列挙型。

    Attributes:
        PATH (int): 通路を表す値（0）
        PACGUM (int): パックガムを表す値（1）
        SUPER_PACGUM (int): スーパー・パックガムを表す値（2）
        BAN (int): 不可侵エリアを表す値（3）
    """
    PATH = 0
    PACGUM = 1
    SUPER_PACGUM = 2
    BAN = 3  # 不可侵エリア


class ItemManager:
    """ゲーム内のアイテムを管理するクラス。

    Attributes:
        pacgum_count (int): パックガムの数
        pacgum_point (int): パックガムの得点
        super_pacgum_point (int): スーパー・パックガムの得点
        item_map (list[list[Optional[Item]]]): アイテムの配置を表す2次元リスト
        pacgums (list[Pacgum]): パックガムのリスト
        super_pacgums (list[SuperPacgum]): スーパー・パックガムのリスト
    """
    def __init__(self, game_state: GameState):
        self.pacgum_count: int = game_state.config.pacgum
        self.pacgum_point: int = game_state.config.points_per_pacgum
        self.super_pacgum_point: int = game_state.config.points_per_super_pacgum

        # 0=通路 1=pacgum 2＝super_pacgum 3=不可侵エリア
        self.item_map: list[list[Optional[Item]]] = self._generate_map(game_state)
        self.pacgums: list[Pacgum] = self._generate_pacgum()
        self.super_pacgums: list[SuperPacgum] = self._generate_super_pacgum()

    def update(self, game_state: GameState) -> None:
        """自分が持っている全アイテムを更新

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        for item in self.pacgums:
            item.update(game_state)

        for item in self.super_pacgums:
            item.update(game_state)
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """自分が持っている全アイテムを描画

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        for item in self.pacgums:
            item.draw(screen)

        for item in self.super_pacgums:
            item.draw(screen)

    def level_up(self, game_state: GameState) -> None:
        """レベルアップ時にアイテムをリセットする

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        self.item_map: list[list[Optional[Item]]] = self._generate_map(game_state)
        self.pacgums: list[Pacgum] = self._generate_pacgum()
        self.super_pacgums: list[SuperPacgum] = self._generate_super_pacgum()

    def try_eat(self, game_state: GameState) -> None | Item:
        """Pacmanがアイテムを取得できるか判定し、取得できる場合はアイテムを取得する。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト

        Returns:
            Optional[Item]: 取得したアイテムを返す。取得できなかった場合はNoneを返す。
        """
        assert game_state.map is not None
        assert game_state.pacman is not None
        map: Map = game_state.map
        pacman: Pacman = game_state.pacman

        px, py = pacman.px, pacman.py
        x, y = map.get_cell(px, py)
        item = self.item_map[y][x]
        if item is None:
            return None

        coords = [
            (px - pacman.size // 3, py),
            (px + pacman.size // 3, py),
            (px, py - pacman.size // 3),
            (px, py + pacman.size // 3),
            ]

        if (item.px, item.py) in coords:
            item.is_eaten = True
            self.item_map[y][x] = None
        return item

    def is_get_all_items(self) -> bool:
        """全てのアイテムを取得したか判定する。

        Returns:
            bool: 全てのアイテムを取得した場合はTrue、そうでない場合はFalse
        """
        for pacgum in self.pacgums:
            if not pacgum.is_eaten:
                return False
        for super_pacgum in self.super_pacgums:
            if not super_pacgum.is_eaten:
                return False
        return True

#    Private functions

    def _generate_map(self, game_state: GameState) -> list[list[Optional[Item]]]:
        """アイテムの配置を生成する。

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト

        Returns:
            list[list[Optional[Item]]]: アイテムの配置を表す2次元リスト
        """
        random.seed(game_state.config.seed)

        assert game_state.map is not None
        map: Map = game_state.map

        # 各オブジェクトの座標リストを初期化
        temp_map = [[CellType.PATH] * map.x for _ in range(map.y)]
        item_map: list[list[Optional[Item]]] = [[None] * map.x for _ in range(map.y)]

        # SuperPacgumのみ四隅に配置
        temp_map[0][0] = CellType.SUPER_PACGUM
        temp_map[0][map.x - 1] = CellType.SUPER_PACGUM
        temp_map[map.y - 1][0] = CellType.SUPER_PACGUM
        temp_map[map.y - 1][map.x - 1] = CellType.SUPER_PACGUM

        # 42を除外
        for y, line in enumerate(map.wall_map):
            for x, cell in enumerate(line):
                if cell == 15:
                    temp_map[y][x] = CellType.BAN

        # pacmanの出現位置を除外
        x, y = map.init_area_pacman()
        temp_map[y][x] = CellType.BAN

        # リストに座標を入力
        path_list: list[tuple[int, int]] = []
        for y, line in enumerate(temp_map):
            for x, cell in enumerate(line):
                if cell == CellType.PATH:
                    path_list.append((x, y))

        # パックガムの生成位置をランダムに選択
        gum_count = min(game_state.config.pacgum, len(path_list))
        gum_list = random.sample(path_list, gum_count)
        for x, y in gum_list:
            temp_map[y][x] = CellType.PACGUM

        # 座標リストをもとに各オブジェクトの生成
        for y, line in enumerate(temp_map):
            for x, cell in enumerate(line):
                if cell == CellType.PACGUM:
                    item_map[y][x] = Pacgum(x, y, game_state.config.points_per_pacgum)
                elif cell == CellType.SUPER_PACGUM:
                    item_map[y][x] = SuperPacgum(x, y, game_state.config.points_per_super_pacgum)

        return item_map

    def _generate_pacgum(self) -> list[Pacgum]:
        """パックガムのリストを生成する。

        Returns:
            list[Pacgum]: パックガムのリスト
        """
        pacgum_list: list[Pacgum] = []

        for y, line in enumerate(self.item_map):
            for x, cell in enumerate(line):
                if type(cell) is Pacgum:
                    gum = self.item_map[y][x]
                    assert isinstance(gum, Pacgum)
                    pacgum_list.append(gum)
        return pacgum_list

    def _generate_super_pacgum(self) -> list[SuperPacgum]:
        """スーパー・パックガムのリストを生成する。

        Returns:
            list[SuperPacgum]: スーパー・パックガムのリスト
        """
        super_pacgum_list: list[SuperPacgum] = []

        for y, line in enumerate(self.item_map):
            for x, cell in enumerate(line):
                if type(cell) is SuperPacgum:
                    gum = self.item_map[y][x]
                    assert isinstance(gum, SuperPacgum)
                    super_pacgum_list.append(gum)
        return super_pacgum_list
