from src.model.base_model.config_model import ConfigModel
from src.model.base_model.result_scene import ResultScene
from src.model.score_manager import ScoreManager


class GameOver(ResultScene):
    """ゲームオーバー画面のクラス。

    Attributes:
        score (int): プレイヤーのスコア
        score_manager (ScoreManager): スコアの管理を行うScoreManagerオブジェクト
    """
    def __init__(self, config: ConfigModel, score: int, score_manager: ScoreManager):
        super().__init__(config, score, score_manager, title="GAME_OVER")
        pass
