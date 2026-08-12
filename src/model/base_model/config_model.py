from pydantic import BaseModel, Field, field_validator
from pathlib import Path


class LevelModel(BaseModel):
    """ゲームのレベル設定を保持するデータクラス.

    Attributes:
        width (int): レベルの幅（5〜25）。デフォルト(20)
        height (int): レベルの高さ（5〜25）。デフォルト(15)
    """
    width: int = Field(ge=5,
                       le=25,
                       default=20,
                       description='map_width')
    height: int = Field(ge=5,
                        le=25,
                        default=15,
                        description='map_height')


DEFAULT_LEVELS = [
    LevelModel(width=7, height=7),   # レベル1
    LevelModel(width=11, height=11),   # レベル2
    LevelModel(width=11, height=7),   # レベル3
    LevelModel(width=7, height=15),   # レベル4
    LevelModel(width=5, height=5),   # レベル5
    LevelModel(width=15, height=15),   # レベル6
    LevelModel(width=5, height=7),   # レベル7
    LevelModel(width=7, height=5),   # レベル8
    LevelModel(width=25, height=5),   # レベル9
    LevelModel(width=25, height=25)   # レベル10
]


class ConfigModel(BaseModel):
    """ゲームの設定を保持するデータクラス.

    Attributes:
        highscore_filename (Path): ハイスコアを保存するJSONファイルのパス
        display_width (int): ゲーム画面の幅（1920〜3840）。デフォルト(1920)
        display_height (int): ゲーム画面の高さ（1080〜2160）。デフォルト(1080)
        level (list[LevelModel]): レベル設定のリスト。最大10レベルまで。
        lives (int): プレイヤーの初期ライフ数（0〜5）。デフォルト(3)
        pacgum (int): 1レベルあたりの通常パックガムの数（0〜100）。デフォルト(42)
        points_per_pacgum (int): 通常パックガム1個あたりの得点（0〜100）。デフォルト(10)
        points_per_super_pacgum (int): スーパー・パックガム1個あたりの得点（0〜500）。デフォルト(50)
        points_per_ghost (int): ゴースト1体あたりの得点（0〜1000）。デフォルト(200)
        seed (int): 乱数生成のシード値（0〜1000）。デフォルト(42)
        level_max_time (int): 1レベルあたりの制限時間（30〜600秒）。デフォルト(90)
    """
    highscore_filename: Path = Field(default=Path("scores.json"),
                                     description="highscore_filename")

    level: list[LevelModel] = Field(default_factory=lambda: list(DEFAULT_LEVELS),
                                    description='map_levels')

    lives: int = Field(ge=0,
                       le=5,
                       default=3,
                       description="game_live")
    pacgum: int = Field(ge=0,
                        le=100,
                        default=42,
                        description="pacgum_count")
    points_per_pacgum: int = Field(ge=0,
                                   le=100,
                                   default=10,
                                   description="points_of_pucgum")
    points_per_super_pacgum: int = Field(ge=0,
                                         le=500,
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
    level_max_time: int = Field(ge=30,
                                le=600,
                                default=90,
                                description="level_of_timelimits")

    # .インスタンス作成前に実行されるためclassmethodが必要
    @field_validator('highscore_filename')  # .何も書かないとafterになる
    @classmethod
    def _validate_file_name(cls, v: Path) -> Path:
        """ハイスコアのファイル名を検証する.

        Args:
            v (Path): ハイスコアのファイル名

        Returns:
            Path: 検証済みのハイスコアのファイル名

        Raises:
            ValueError: ファイル名が不正な場合
        """
        # .jsonでないのなら.jsonを加える
        if v.suffix != '.json':
            v = v.with_suffix('.json')

        # ディレクトリ指定は禁止（ファイル名のみ許可）
        if v.parent != Path('.'):
            raise ValueError("highscore_filename must be a filename without directories.")

        # 同名のディレクトリが存在するか
        if v.exists() and v.is_dir():
            raise ValueError(f"A directory named {v.name} already exists.")

        # ファイル名に禁止文字が含まれているか、実際に開けるか
        try:
            # ファイルが存在する場合追記モードでopen
            if v.exists():
                with open(v, 'a'):
                    pass
            # ファイルが存在しない場合新規作成モードでopen
            else:
                with open(v, 'x'):
                    pass
                v.unlink()  # ファイル削除
        except OSError as e:
            raise ValueError(f"File_NameError: {e}")
        return v

    @field_validator('level')
    @classmethod
    def ensure_ten_levels(cls, v: list[LevelModel]) -> list[LevelModel]:
        """レベル設定のリストが10レベル未満の場合、デフォルトのレベル設定で補充する.

        Args:
            v (list[LevelModel]): レベル設定のリスト

        Returns:
            list[LevelModel]: 10レベルに補充されたレベル設定のリスト
        """
        target_length = 10

        if len(v) < target_length:
            # vが3つなら、DEFAULT_LEVELS[3:10] (レベル4〜10) が補充される
            v.extend(DEFAULT_LEVELS[len(v):target_length])
        elif target_length < len(v):
            print('Warning: More than 10 levels provided. Only the first 10 levels will be used.')

        return v[:10]
