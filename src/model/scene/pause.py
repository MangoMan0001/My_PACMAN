import pygame
from typing import Any

from src.model.base_model.scene import Scene
from src.model.base_model.config_model import ConfigModel


class Pause:
    def __init__(self, config: ConfigModel) -> None:
        self.selected_index: int = 0  # メニューの選択インデックス
        self.start_time: float = 0.0
        self.memu_items: list[str] = ["Resume", "Retry", "How to Play", "Quit"]

    def update(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """
        イベントを処理する。画面遷移が必要な場合はシーン名と受け渡すデータをタプルで返す。
        何もなければNoneを返す
        """
        pass

    def draw(self, screen: pygame.Surface, game_state: Any) -> None:
        pass

    def _resume(self) -> None:
        """ゲームを再開するための処理。

        ポーズ中に経過した時間を計算し、ゲームの開始時間を調整する。
        """
        # 現在時刻からポーズ開始時刻を引いた時間 = ポーズ中に経過した時間
        pause_duration = time.time() - self.pause_start_time
        # ゲームの開始時間と経過時間にポーズ中に経過した時間を加算する
        self.start_time += pause_duration
        self.time += pause_duration
        # ポーズを解除
        self.paused = False

    def updata_pause_memu(self, events: list[pygame.event.Event]) -> None | tuple[str, Any]:
        """ポーズメニューの更新処理。

        Args:
            events (list[pygame.event.Event]): pygameのイベントリスト。

        Returns:
            None | tuple[str, Any]:
                ゲームオーバーやゲームクリアなどの状態変化があれば、シーン名と受け渡すデータをタプルで返す。
                何もなければNoneを返す。
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 上、wキーでメニュー項目の選択
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (
                        self.selected_index - 1) % len(self.pause_memu)
                # 下、sキーでメニュー項目の選択
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (
                        self.selected_index + 1) % len(self.pause_memu)
                # エンターキーで選択中のメニュー項目をアクティブにする。
                elif event.key == pygame.K_RETURN:
                    label = self.pause_memu[self.selected_index]
                    if label == "Resume":
                        self._resume()
                    elif label == "Retry":
                        return ("PLAY", None)
                    elif label == "Quit":
                        return ("MAIN_MENU", None)
