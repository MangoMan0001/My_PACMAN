from mazegenerator import MazeGenerator
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
import fire
import pygame


class LevelModel(BaseModel):
    width: int = Field(ge=0,
                       le=100,
                       default=20,
                       description='map_width')
    height: int = Field(ge=0,
                        le=100,
                        default=15,
                        description='map_height')


DEFAULT_LEVELS = [
    LevelModel(width=15, height=15),   # レベル1
    LevelModel(width=21, height=21),   # レベル2
    LevelModel(width=25, height=25),   # レベル3
    LevelModel(width=31, height=31),   # レベル4
    LevelModel(width=35, height=35),   # レベル5
    LevelModel(width=41, height=41),   # レベル6
    LevelModel(width=45, height=45),   # レベル7
    LevelModel(width=51, height=51),   # レベル8
    LevelModel(width=55, height=55),   # レベル9
    LevelModel(width=61, height=61),   # レベル10
]


class ConfigModel(BaseModel):
    """MazeGeneratorの設定値を保持・検証するデータクラス.

    Pydanticを使用して、型チェックと値の範囲を検証する。

    Attributes:
        width (int): 迷路の幅（0〜42）。デフォルト(20)
        height (int): 迷路の高さ（0〜42）。デフォルト(15)
        entry (tuple): スタート地点の座標 (x, y)。デフォルト(0, 0)
    """
    highscore_filename: Path = Field(default=Path("scores.txt"),
                                     description="highscore_filename")

    level: list[LevelModel] = Field(default_factory=list,
                                    description='map_levels')

    lives: int = Field(ge=0,
                       le=42,
                       default=3,
                       description="game_live")
    pacgum: int = Field(ge=0,
                        le=1000,
                        default=42,
                        description="pacgum_count")
    points_per_pacgum: int = Field(ge=0,
                                   le=42,
                                   default=10,
                                   description="points_of_pucgum")
    points_per_super_pacgum: int = Field(ge=0,
                                         le=1000,
                                         default=50,
                                         description="points_of_super_pucgum")
    points_per_ghost: int = Field(ge=0,
                                  le=1000,
                                  default=200,
                                  description="points_of_ghost")
    seed: int = Field(ge=0,
                      le=1000,
                      default=42,
                      description="random_seed")
    level_max_time: int = Field(ge=0,
                                le=1000,
                                default=90,
                                description="level_of_timelimits")

    # .インスタンス作成前に実行されるためclassmethodが必要
    @field_validator('highscore_filename')  # .何も書かないとafterになる
    @classmethod
    def _validate_file_name(cls, v: Path) -> Path:
        """出力ファイル名の妥当性を検証/修正する.

        - 拡張子 '.txt' がなければ付与
        - 同名のディレクトリが存在しないか確認
        - ファイルへの書き込み権限があるかテスト

        Args:
            v (Any): 入力されたファイルパス。

        Returns:
            Any: 検証・修正済みのPathオブジェクト。

        Raises:
            ValueError: ディレクトリと同名の場合や書き込み権限がない場合。
        """
        if v.suffix != '.txt':
            v = v.with_suffix('.txt')

        if v.exists() and v.is_dir():
            raise ValueError(f"A directory named {v.name} already exists.")

        try:
            if v.exists():
                with open(v, 'a'):
                    pass
            else:
                with open(v, 'x'):
                    pass
                v.unlink()
        except OSError as e:
            raise ValueError(f"File_NameError: {e}")
        return v

    @field_validator('level')
    @classmethod
    def ensure_ten_levels(cls, v: list[LevelModel]) -> list[LevelModel]:
        target_length = 10

        if len(v) < target_length:
            # vが3つなら、DEFAULT_LEVELS[3:10] (レベル4〜10) が補充される
            v.extend(DEFAULT_LEVELS[len(v):target_length])

        return v


def load_config(filepath: str) -> ConfigModel:
    lines = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped.startswith("#"):
                lines.append(line)

    clean_json_str = "".join(lines)
    return ConfigModel.model_validate_json(clean_json_str)


TILE_SIZE = 32


def print_window(config_json: ConfigModel) -> None:
    # ウィンドウサイズ = マス目の数 × 1マスのピクセル数
    screen_width = config_json.level[0].width * TILE_SIZE
    screen_height = config_json.level[0].height * TILE_SIZE

    # Pygameの初期化
    pygame.init()

    # 画面の作成とタイトルの設定
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("My Pac-Man")

    # ゲームループ
    running = True
    while running:
        # イベント（キー入力や閉じるボタンなど）の処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # ウィンドウの×ボタンが押されたら
                running = False

        # 画面を黒 (R:0, G:0, B:0) で塗りつぶす
        screen.fill((0, 0, 0))

        # 描画内容を画面に反映
        pygame.display.flip()

    # ループを抜けたらPygameを終了してプログラムを終わる
    pygame.quit()


def main(config_path: str = 'config.json') -> None:
    path = Path(config_path)

    if not path.exists():
        print('naiyo error config.json')

    config_json = load_config(config_path)
    print(config_json.model_dump_json(indent=4))
    generator = MazeGenerator(size=(config_json.level[0].width, config_json.level[0].height),
                              seed=config_json.seed,
                              perfect=False)
    generator.generate()
    print_window(config_json)


if __name__ == "__main__":
    fire.Fire(main)
