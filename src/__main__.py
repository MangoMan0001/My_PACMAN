import fire
# import pygame
from pathlib import Path

from .game import Game
from src.model.base_model.config_model import ConfigModel


TILE_SIZE = 32


# def print_window(config_json: ConfigModel) -> None:
#     # ウィンドウサイズ = マス目の数 × 1マスのピクセル数
#     screen_width = config_json.level[0].width * TILE_SIZE
#     screen_height = config_json.level[0].height * TILE_SIZE

#     # Pygameの初期化
#     pygame.init()

#     # 画面の作成とタイトルの設定
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     pygame.display.set_caption("My Pac-Man")

#     # ゲームループ
#     running = True
#     while running:
#         # イベント（キー入力や閉じるボタンなど）の処理
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:  # ウィンドウの×ボタンが押されたら
#                 running = False

#         # 画面を黒 (R:0, G:0, B:0) で塗りつぶす
#         screen.fill((0, 0, 0))

#         # 描画内容を画面に反映
#         pygame.display.flip()

#     # ループを抜けたらPygameを終了してプログラムを終わる
#     pygame.quit()


def load_config(filepath: str) -> ConfigModel:
    lines = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped.startswith("#"):
                lines.append(line)

    clean_json_str = "".join(lines)
    return ConfigModel.model_validate_json(clean_json_str)


def main(config_path: str = 'config.json') -> None:
    path = Path(config_path)

    if not path.exists():
        print('naiyo error config.json')

    config_json = load_config(config_path)
    # print(config_json.model_dump_json(indent=4))

    Game().run(config_json)

    # print_window(config_json)


if __name__ == "__main__":
    fire.Fire(main)
