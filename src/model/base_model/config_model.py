from pydantic import BaseModel, Field, field_validator
from pathlib import Path


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
    LevelModel(width=11, height=11),   # レベル1
    LevelModel(width=15, height=15),   # レベル2
    LevelModel(width=21, height=21),   # レベル3
    LevelModel(width=25, height=25),   # レベル4
    LevelModel(width=31, height=31),   # レベル5
    LevelModel(width=35, height=35),   # レベル6
    LevelModel(width=41, height=41),   # レベル7
    LevelModel(width=45, height=45),   # レベル8
    LevelModel(width=51, height=51),   # レベル9
    LevelModel(width=55, height=55),   # レベル10
]


class ConfigModel(BaseModel):
    """MazeGeneratorの設定値を保持・検証するデータクラス.

    Pydanticを使用して、型チェックと値の範囲を検証する。

    Attributes:
        width (int): 迷路の幅（0〜42）。デフォルト(20)
        height (int): 迷路の高さ（0〜42）。デフォルト(15)
        entry (tuple): スタート地点の座標 (x, y)。デフォルト(0, 0)
    """
    highscore_filename: Path = Field(default=Path("scores.json"),
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
        if v.suffix != '.json':
            v = v.with_suffix('.json')

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
