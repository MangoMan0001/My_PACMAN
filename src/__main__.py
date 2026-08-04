import fire
from pathlib import Path

from .game import Game
from src.model.base_model.config_model import ConfigModel


def load_config(filepath: str) -> ConfigModel:
    """config.jsonを読み込む関数。

    Args:
        filepath (str): config.jsonのパス

    Returns:
        ConfigModel: 読み込んだconfig.jsonをConfigModelに変換したオブジェクト
    """
    lines = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped.startswith("#"):
                lines.append(line)

    clean_json_str = "".join(lines)
    return ConfigModel.model_validate_json(clean_json_str)


def main(config_path: str = 'config.json') -> None:
    """ゲームを起動する関数。

    Args:
        config_path (str, optional): config.jsonのパス. デフォルト値は 'config.json'.
    """
    path = Path(config_path)

    if not path.exists():
        print('cannot find config.json')

    config_json = load_config(config_path)

    Game(config_json).run()


if __name__ == "__main__":
    # try:
    fire.Fire(main)
    # except Exception as e:
    #     print(e)
