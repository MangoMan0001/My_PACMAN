# generate_assets.py (画像生成専用スクリプト)
import pygame
import os


def create_pacman_images(output_dir: str) -> None:
    # 透明な背景のSurfaceを作成
    surface = pygame.Surface((128, 128), pygame.SRCALPHA)

    # ここならPygameの図形描画が使い放題！
    # パックマンの真ん丸を描く
    pygame.draw.circle(surface, (255, 255, 0), (64, 64), 64)
    # 口の黒い三角を描く
    pygame.draw.polygon(surface, (0, 0, 0, 0), [(64, 64), (96, 64), (32, 96)])

    # 画像として保存
    pygame.image.save(surface, os.path.join(output_dir, "PACMAN_right.png"))


def create_font_images(output_dir: str) -> None:
    pygame.font.init()
    # OSに入っている標準フォントを使用
    font = pygame.font.Font("data/font/PAC-FONT.TTF", 128)  # フォントサイズ128

    # A〜Zまでの文字画像をループで一気に生成！
    for char_code in range(ord('A'), ord('Z') + 1):
        char = chr(char_code)
        # 文字を画像化（白色）
        text_surface = font.render(char, True, (255, 255, 0))
        pygame.image.save(text_surface, os.path.join(output_dir, f"PAC-FONT_{char}.png"))


if __name__ == "__main__":
    os.makedirs("data/assets", exist_ok=True)
    create_pacman_images("data/assets")
    create_font_images("data/assets")
    print("画像の自動生成が完了しました！")
