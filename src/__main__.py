"""Pacmanゲームを起動するためのスクリプト."""
import fire
import json
from pathlib import Path
from pydantic import ValidationError

from .game import Game
from src.model.base_model.config_model import ConfigModel


def load_config(filepath: str) -> ConfigModel:
    """config.jsonを読み込む関数.

    Args:
        filepath (str): config.jsonのパス

    Returns:
        ConfigModel: 読み込んだconfig.jsonをConfigModelに変換したオブジェクト
    """
    lines = []
    data = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped.startswith("#"):
                    lines.append(line)

        clean_json_str = "".join(lines)

        # キーの欠落
        data = json.loads(clean_json_str)
        expected_keys = set(ConfigModel.model_fields.keys())
        provided_keys = set(data.keys())
        missing_keys = expected_keys - provided_keys

        if missing_keys:
            print(f"Warning: Missing keys {missing_keys} in config. Using safe defaults for them.")

        return ConfigModel.model_validate_json(clean_json_str)

    except FileNotFoundError:
        # ファイル欠落
        print(f"Warning: Configuration file '{filepath}' not found. Using safe defaults.")
        return ConfigModel()

    except json.JSONDecodeError as e:
        # JSON構文エラー
        print(f"Warning: Failed to parse config JSON. Using safe defaults. Details: {e}")
        return ConfigModel()

    except ValidationError as e:
        # バリデーションエラー
        print(f"Warning: Invalid values found in config file. Clamping to safe defaults.{e}")
        # エラーになった項目（loc）を特定して、辞書から削除する
        for error in e.errors():
            error_keys = error.get('loc')
            if error_keys:
                invalid_key = error_keys[0]
                if invalid_key in data:
                    print(f" -> Resetting '{invalid_key}' to default.")
                    del data[invalid_key]

        return ConfigModel.model_validate(data)

    except Exception as e:
        print(f"Warning: Failed to parse config JSON. Using safe defaults. Details: {e}")
        return ConfigModel()


def main(config_path: str = 'config.json') -> None:
    """ゲームを起動する関数.

    Args:
        config_path (str, optional): config.jsonのパス. デフォルト値は 'config.json'.
    """
    path = Path(config_path)

    if not path.exists():
        print('cannot find config.json')

    config_json = load_config(config_path)

    Game(config_json).run()


if __name__ == "__main__":
    try:
        fire.Fire(main)
    except Exception as e:
        print(f"error:{e}")
