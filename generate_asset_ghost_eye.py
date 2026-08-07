import pygame
import os


def generate_ghost_eyes() -> None:
    # 画面を表示せずにPygameをバックグラウンドで初期化
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.HIDDEN)

    # 保存先ディレクトリの作成（プロジェクトの構成に合わせて変更してください）
    output_dir = "assets/eyes"
    os.makedirs(output_dir, exist_ok=True)

    SIZE = 24
    WHITE = (255, 255, 255)
    BLUE = (33, 33, 255) # パックマンらしい少し明るめの青
    TRANSPARENT = (0, 0, 0, 0)

    # 瞳のずらし幅 (dx, dy)
    # 24ピクセルの中で絶妙に視線が変わるようにオフセットを調整しています
    offsets = {
        "up": (0, -2),
        "down": (0, 2),
        "left": (-1, 0),
        "right": (1, 0)
    }

    for direction, (dx, dy) in offsets.items():
        # 透明な24x24のキャンバスを作成
        surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        surface.fill(TRANSPARENT)

        # --- 白目の描画 (x, y, width, height) ---
        # 左目 (キャンバスの左側)
        pygame.draw.ellipse(surface, WHITE, (4, 6, 6, 10))
        # 右目 (キャンバスの右側)
        pygame.draw.ellipse(surface, WHITE, (14, 6, 6, 10))

        # --- 瞳(青)の描画 ---
        # ベースの中心座標 (左目:x=5, y=9 / 右目:x=15, y=9) に dx, dy を足して視線を動かす
        pygame.draw.ellipse(surface, BLUE, (5 + dx, 9 + dy, 4, 4))
        pygame.draw.ellipse(surface, BLUE, (15 + dx, 9 + dy, 4, 4))

        # 画像として保存
        file_path = os.path.join(output_dir, f"eye_{direction}.png")
        pygame.image.save(surface, file_path)
        print(f"Generated: {file_path}")

    pygame.quit()

if __name__ == "__main__":
    generate_ghost_eyes()
