"""スコアの管理を行うモジュール."""
import os
import json
from pathlib import Path
from pydantic import BaseModel, ValidationError
from typing import Any

from src.model.base_model.config_model import ConfigModel


class ScoreModel(BaseModel):
    """スコアのデータモデル.

    Attributes:
        name (str): プレイヤーの名前
        score (int): プレイヤーのスコア
    """
    name: str
    score: int


class ScoreManager():
    """スコアの管理を行うクラス.

    Attributes:
        file_path (Path): スコアを保存するファイルのパス
        scores (list[dict[str, str | int]]): スコアのリスト
    """
    def __init__(self, config: ConfigModel):
        """ScoreManagerのコンストラクタ."""
        self.score_root = Path(__file__).resolve().parents[2] / "data" / "score"
        self.file_path: Path = Path(self.score_root) / config.highscore_filename.name
        self.scores: list[dict[str, str | int]] = [{'name': 'No One', 'score': 0}]

        # 既にファイルがある場合読み込む
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    temp_score = json.load(f)
                    if temp_score == []:
                        pass
                    elif self._validate_score(temp_score):
                        self.scores = temp_score
                    self._save_file()

            except OSError as e:
                print('file read error:', e)
            except json.JSONDecodeError as e:
                print('file read error:', e)

        # 既にファイルがない場合生成後書き込む
        else:
            self._save_file()

    def save_score(self, name: str, score: int) -> None:
        """スコアを保存するメソッド.

        Args:
            name (str): プレイヤーの名前
            score (int): プレイヤーのスコア
        """
        if name.strip() == '':
            name = 'No One'
        self.scores.append({'name': name, 'score': score})
        self._save_file()

    def get_highscore(self) -> int:
        """ハイスコアを取得するメソッド.

        Returns:
            int: ハイスコア
        """
        return int(max(self.scores, key=lambda x: x['score'])['score'])

    def get_sorted_score(self) -> list[dict[str, str | int]]:
        """スコアを降順にソートして返すメソッド.

        Returns:
            list[dict[str, str | int]]: スコアを降順にソートしたリスト
        """
        return sorted(self.scores, key=lambda x: x['score'], reverse=True)

#    Private Method

    def _save_file(self) -> None:
        """スコアをファイルに保存するメソッド.

        Raises:
            OSError: ファイルの保存に失敗した場合
        """
        try:
            # data/scoreフォルダを生成
            os.makedirs(self.score_root, exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, indent=4)
        except OSError as e:
            print('file save error:', e)

    def _validate_score(self, temp_score: Any) -> bool:
        """スコアのデータを検証するメソッド.

        Args:
            temp_score (Any): 検証するスコアのデータ

        Returns:
            bool: スコアのデータが有効な場合はTrue、無効な場合はFalse

        Raises:
            ValidationError: スコアのデータが無効な場合
        """
        try:
            if not isinstance(temp_score, list):
                return False
            _ = [ScoreModel(**param) for param in temp_score]
            return True
        except (ValidationError, TypeError) as e:
            print('score validation error:', e)
            print('reset score to default')
            return False
