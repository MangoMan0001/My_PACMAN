"""キャラクターマネージャークラス."""
import pygame

from src.model.base_model.ghost import Ghost, GhostMode
from src.model.map import Map
from src.model.game_state import GameState
from src.model.character.pacman import Pacman
from src.model.character.blinky import Blinky
from src.model.character.inky import Inky
from src.model.character.clyde import Clyde
from src.model.character.pinky import Pinky


class CharacterManager:
    """ゲーム内のキャラクターを管理するクラス.

    Attributes:
        pacman (Pacman): Pacmanのインスタンス
        ghosts (list[Ghost]): ゴーストのインスタンスのリスト
        pacman_blinking_time (float): Pacmanが点滅している時間
        is_pacman_drawable (bool): Pacmanが描画可能かどうかのフラグ
        is_frozen (bool): ゴーストが凍結しているかどうかのフラグ
    """
    def __init__(self, game_state: GameState):
        """characer_managerクラスのコンストラクタ."""
        assert game_state.map is not None
        map: Map = game_state.map
        speed = 2
        x, y = map.init_area_pacman()
        px, py = map.cell_center(x, y)

        self.pacman: Pacman = Pacman(x, y, px, py, speed)

        bx, by = map.cell_center(0, 0)
        px, py = map.cell_center(map.x - 1, 0)
        ix, iy = map.cell_center(0, map.y - 1)
        cx, cy = map.cell_center(map.x - 1, map.y - 1)

        self.ghosts: list[Ghost] = [
            Blinky(0, 0, bx, by, speed, (255, 0, 0), game_state.config.points_per_ghost),
            Pinky(map.x - 1, 0, px, py, speed, (255, 182, 193), game_state.config.points_per_ghost),
            Inky(0, map.y - 1, ix, iy, speed, (0, 255, 255), game_state.config.points_per_ghost),
            Clyde(map.x - 1, map.y - 1, cx, cy, speed, (255, 165, 0), game_state.config.points_per_ghost),
        ]

        self.pacman_blinking_time: float = 0
        self.is_pacman_drawable: bool = True

        # チートフラグ
        self.is_frozen: bool = False

    def update(self, game_state: GameState) -> None:
        """自分が持っている全キャラクターを更新する.

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        # pacman点滅処理
        if 0 < self.pacman_blinking_time:
            self.pacman_blinking_time -= game_state.dt
            if int(self.pacman_blinking_time * 10) % 2 == 0:
                self.is_pacman_drawable = False
            else:
                self.is_pacman_drawable = True
            if self.pacman_blinking_time <= 0:
                self.is_pacman_drawable = True

        # ゲーム待機時はキャラクターの更新を止める
        if game_state.game_status in ('READY', 'HIT'):
            return

        self.pacman.update(game_state)

        # チート ゴースト凍結 「マヒャド！」 「ブリザガ！」
        if self.is_frozen:
            return

        for ghost in self.ghosts:
            ghost.update(game_state)

    def draw(self, screen: pygame.Surface) -> None:
        """自分が持っている全キャラクターを描画する.

        Args:
            screen (pygame.Surface): 描画対象のSurfaceオブジェクト
        """
        if self.is_pacman_drawable:
            self.pacman.draw(screen)

        for ghost in self.ghosts:
            ghost.draw(screen)

    def level_up(self, game_state: GameState) -> None:
        """クリア後のレベルアップ処理.

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        self.pacman.level_up(game_state)

        for ghost in self.ghosts:
            ghost.level_up(game_state)

    def get_pos_pacman_cell(self) -> tuple[int, int]:
        """Pacmanの現在のセル座標を取得する.

        Returns:
            tuple[int, int]: _description_
        """
        return self.pacman.get_pos_cell()

    def get_pos_pacman_pixel(self) -> tuple[int, int]:
        """Pacmanの現在のピクセル座標を取得する.

        Returns:
            tuple[int, int]: _description_
        """
        return self.pacman.get_pos_pixel()

    def is_hit(self, game_state: GameState) -> None | Ghost:
        """Pacmanがゴーストに当たったか判定する.

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト

        Returns:
            Optional[Ghost]: 当たったゴーストを返す。衝突していない場合はNoneを返す。
        """
        pacman: Pacman = self.pacman

        px, py = pacman.px, pacman.py

        pacman_coords = [
            (px - pacman.size // 3, py),
            (px + pacman.size // 3, py),
            (px, py - pacman.size // 3),
            (px, py + pacman.size // 3),
            ]

        for ghost in self.ghosts:
            gx, gy = ghost.px, ghost.py
            top = gy - ghost.size // 3
            right = gx + ghost.size // 3
            bottom = gy + ghost.size // 3
            left = gx - ghost.size // 3
            for px, py in pacman_coords:
                if py == gy and left <= px <= right:
                    return ghost
                if px == gx and top <= py <= bottom:
                    return ghost
        return None

    def hit(self, game_state: GameState) -> None:
        """Pacmanがゴーストに当たった場合の処理.

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        self.pacman_blinking_time = 1.5

    def reset(self, game_state: GameState) -> None:
        """ゲームの状態をリセットする.

        Args:
            game_state (GameState): ゲームの状態を保持するGameStateオブジェクト
        """
        self.pacman.level_up(game_state)

        for ghost in self.ghosts:
            ghost.level_up(game_state)

    def be_scared(self) -> None:
        """ゴーストをいじけ状態にする関数."""
        for ghost in self.ghosts:
            if ghost.current_mode not in (GhostMode.EATEN, GhostMode.READY):
                ghost.be_scared()

    def is_eaten(self) -> bool:
        """ゴーストが全て捕食後状態か判定する.

        Returns:
            bool: ゴーストが全て捕食後状態の場合はTrue、そうでない場合はFalse
        """
        if self.ghosts[0].current_mode == GhostMode.SCARED:
            for ghost in self.ghosts:
                ghost.current_mode = GhostMode.EATEN
            return True
        return False

#    Private functions
