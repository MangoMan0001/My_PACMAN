import pygame


class Game:
    def __init__(self, config: dict[str, int | list[dict[str, int]] | str]):
        """ゲームの初期化"""
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((config["width"], config["height"]))
        self.clock = pygame.time.Clock()
        self.is_running = True

        # ゲームの「状態」をまとめたオブジェクトを作成
        self.state = GameState(maze_data=[...])

        # インスタンスを生成して state に登録
        self.state.pacman = Pacman(x=10, y=10, speed=2)
        self.state.ghosts.append(Blinky(x=1, y=1, speed=2, color="red"))
        self.state.ghosts.append(Inky(x=2, y=1, speed=2, color="cyan"))
        # (アイテム類の生成と登録...)

    def run(self) -> None:
        while self.is_running:
            # 1. 入力の取得
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            # 2. 状態の更新 (GameStateを丸ごと渡すのがミソ！)
            self.state.pacman.update(self.state, keys)
            for ghost in self.state.ghosts:
                ghost.update(self.state)

            # 3. 全体の判定処理 (パックマンがアイテムを食べたか、ゴーストとぶつかったか等)
            self._check_collisions()

            # 4. 描画
            self.screen.fill((0, 0, 0)) # 画面クリア
            # mazeを描画...
            for item in self.state.items:
                if not item.is_eaten:
                    item.draw(self.screen)
            self.state.pacman.draw(self.screen)
            for ghost in self.state.ghosts:
                ghost.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60) # 60FPS

    def _check_collisions(self):
        # ここで「自作の当たり判定」を行う
        # 例: パックマンとゴーストの座標が同じマスなら lives を減らすなど
        pass

class Game:
    def __init__(self, config):
        # 1. 外部ツールからマップデータを生成（ダミー配列）
        maze_data = generate_maze(...)

        # 2. 最初に Maze クラスを作る
        self.maze = Maze(maze_data)

        # 3. Maze に座標を聞いて、Pacman を作る
        px, py = self.maze.get_pacman_spawn()
        self.pacman = Pacman(x=px, y=py, speed=2)

        # 4. Maze に四隅の座標を聞いて、Ghost を作る
        gx, gy = self.maze.get_ghost_spawns()
        self.ghosts = [
            Blinky(x=gx[0], y=gy[0], speed=2, color="red"),
            # 他のゴーストも同様に...
        ]
