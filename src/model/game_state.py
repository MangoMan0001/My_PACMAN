from model.map import Map
from model.character.pacman import Pacman
from model.base_model.ghost import Ghost
from model.item_manager import ItemManager


# --- ゲームの状態をすべて持つデータクラス ---
class GameState:
    def __init__(self, lives: int, map: Map, pacman: Pacman):
        self.score = 0
        self.lives = lives
        self.map = map
        self.item = ItemManager
        self.keys: list[int] = []           # key入力情報
        self.pacman = pacman                # Pacmanのインスタンスを保持
        self.ghosts: list[Ghost] = []       # 4匹のGhostのインスタンスをリストで保持
