# generate_assets.py
import pygame
import os


def create_pacman_sprites(output_dir: str) -> None:
    pygame.init()
    size = 24  # 🌟 32から24に変更！
    center = (size // 2, size // 2)  # (12, 12)
    radius = size // 2               # 12

    # 1. 口が閉じたパックマン（ただの黄色い丸）
    surface_closed = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surface_closed, (255, 255, 0), center, radius)
    pygame.image.save(surface_closed, os.path.join(output_dir, "pacman_closed.png"))

    # 2. 口が開いたパックマン（各方向）
    # 24x24のサイズに合わせてポリゴンの端を調整
    directions = {
        "RIGHT": [(size, 3), (size, size - 3)],
        "LEFT":  [(0, 3), (0, size - 3)],
        "UP":    [(3, 0), (size - 3, 0)],
        "DOWN":  [(3, size), (size - 3, size)]
    }

    for dir_name, (p1, p2) in directions.items():
        surface_open = pygame.Surface((size, size), pygame.SRCALPHA)
        # 黄色い丸を描く
        pygame.draw.circle(surface_open, (255, 255, 0), center, radius)
        # 黒（透明）の三角形を描いて口をくり抜く
        pygame.draw.polygon(surface_open, (0, 0, 0, 0), [center, p1, p2])

        pygame.image.save(surface_open, os.path.join(output_dir, f"pacman_open_{dir_name.lower()}.png"))


if __name__ == "__main__":
    os.makedirs("assets/pacman", exist_ok=True)
    create_pacman_sprites("assets/pacman")
    print("24x24のパックマン画像を生成しました！")
