# generate_assets.py (画像生成専用スクリプト)
import pygame
import os


def create_pacman_images(output_dir: str) -> None:
    # 透明な背景のSurfaceを作成
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)

    # パックマンの真ん丸を描く
    pygame.draw.circle(surface, (255, 255, 0), (16, 16), 16)
    # 口の黒い三角を描く
    pygame.draw.polygon(surface, (0, 0, 0, 0), [(16, 16), (32, 32), (32, 0)])

    # 画像として保存
    pygame.image.save(surface, os.path.join(output_dir, "PACMAN_right_32.png"))


def create_font_upper_images(output_dir: str) -> None:
    pygame.font.init()
    # フォントを使用指定
    font = pygame.font.Font("data/font/pacmania/Pacmania.otf", 256)  # フォントサイズ256

    for char_code in range(ord('A'), ord('Z') + 1):
        char = chr(char_code)
        # 文字を画像化（黄色）
        text_surface = font.render(char, True, (255, 255, 0))
        pygame.image.save(text_surface, os.path.join(output_dir, f"PAC-FONT_{char}.png"))

    # ハイフンの文字画像を生成
    text_surface = font.render(chr(45), True, (255, 255, 0))
    pygame.image.save(text_surface, os.path.join(output_dir, "PAC-FONT_-.png"))


def create_font_lower_images(output_dir: str) -> None:
    pygame.font.init()
    # フォントを使用
    font = pygame.font.Font("data/font/pacmania/Pacmania.otf", 128)  # フォントサイズ128

    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        # 文字を画像化（黄色）
        text_surface = font.render(char, True, (255, 255, 0))
        pygame.image.save(text_surface, os.path.join(output_dir, f"PAC-FONT_{char}.png"))

    # ハイフンの文字画像を生成
    text_surface = font.render(chr(45), True, (255, 255, 0))
    pygame.image.save(text_surface, os.path.join(output_dir, "PAC-FONT_-.png"))


def create_font_misaki_images(output_dir: str) -> None:
    pygame.font.init()
    # フォントを使用。サイズ64
    font = pygame.font.Font("data/font/misaki/misaki_gothic_2nd.ttf", 24)

    # A〜Zまでの文字画像をループで一気に生成
    for char_code in range(ord('A'), ord('Z') + 1):
        char = chr(char_code)
        # 文字を画像化（黄色）
        text_surface = font.render(char, True, (255, 255, 255))
        pygame.image.save(text_surface, os.path.join(output_dir, f"misaki-FONT_{char}.png"))

    # a〜zまでの文字画像をループで一気に生成
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        # 文字を画像化（黄色）
        text_surface = font.render(char, True, (255, 255, 255))
        pygame.image.save(text_surface, os.path.join(output_dir, f"misaki-FONT_{char}.png"))

    # 0~9までの文字画像をループで一気に生成
    for char_code in range(ord('0'), ord('9') + 1):
        char = chr(char_code)
        # 文字を画像化（白色）
        text_surface = font.render(char, True, (255, 255, 255))
        pygame.image.save(text_surface, os.path.join(output_dir, f"misaki-FONT_{char}.png"))

    # ハイフンの文字画像を生成
    text_surface = font.render(chr(45), True, (255, 255, 255))
    pygame.image.save(text_surface, os.path.join(output_dir, "misaki-FONT_-.png"))

    # ドットの文字画像を生成
    text_surface = font.render(".", True, (255, 255, 255))
    pygame.image.save(text_surface, os.path.join(output_dir, "misaki-FONT_..png"))


def create_font_none_images(output_dir: str) -> None:
    pygame.font.init()
    # フォントを使用。サイズ64
    font = pygame.font.Font(None, 32)

    # A〜Zまでの文字画像をループで一気に生成
    for char_code in range(ord('A'), ord('Z') + 1):
        char = chr(char_code)
        # 文字を画像化（黄色）
        text_surface = font.render(char, True, (255, 255, 255))
        pygame.image.save(text_surface, os.path.join(output_dir, f"none-FONT_{char}.png"))

    # a〜zまでの文字画像をループで一気に生成
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        # 文字を画像化（黄色）
        text_surface = font.render(char, True, (255, 255, 255))
        pygame.image.save(text_surface, os.path.join(output_dir, f"none-FONT_{char}.png"))

    # 0~9までの文字画像をループで一気に生成
    for char_code in range(ord('0'), ord('9') + 1):
        char = chr(char_code)
        # 文字を画像化（白色）
        text_surface = font.render(char, True, (255, 255, 255))
        pygame.image.save(text_surface, os.path.join(output_dir, f"none-FONT_{char}.png"))

    # ハイフンの文字画像を生成
    text_surface = font.render(chr(45), True, (255, 255, 255))
    pygame.image.save(text_surface, os.path.join(output_dir, "none-FONT_-.png"))

    # ドットの文字画像を生成
    text_surface = font.render(".", True, (255, 255, 255))
    pygame.image.save(text_surface, os.path.join(output_dir, "none-FONT_..png"))

def create_dither_images(output_dir: str) -> pygame.Surface:
    """画面全体を覆う半透明のSurfaceを作成する。

        Args:
            width (int): Surfaceの幅。
            height (int): Surfaceの高さ。
    """
    black = (0, 0, 0, 255)  # 半透明の黒
    width, height = 1920, 1080  # 画面サイズを指定

    row_even = pygame.Surface((width, 1), pygame.SRCALPHA)
    row_odd = pygame.Surface((width, 1), pygame.SRCALPHA)
    for x in range(0, width, 2):
        row_even.set_at((x, 0), black)
    for x in range(1, width, 2):
        row_odd.set_at((x, 0), black)

    dither_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(height):
        if y % 2 == 0:
            dither_surface.blit(row_even, (0, y))
        else:
            dither_surface.blit(row_odd, (0, y))

    pygame.image.save(dither_surface, os.path.join(output_dir, "dither_surface.png"))
    return dither_surface

if __name__ == "__main__":
    # os.makedirs("data/assets/Pacman", exist_ok=True)
    # os.makedirs("data/assets/upper_256", exist_ok=True)
    # os.makedirs("data/assets/lower_128", exist_ok=True)
    # os.makedirs("data/assets/nonefont_32", exist_ok=True)
    os.makedirs("data/assets/dither_images", exist_ok=True)

    # create_pacman_images("data/assets/Pacman")
    # create_font_upper_images("data/assets/upper_256")
    # create_font_lower_images("data/assets/lower_128")
    # create_font_none_images("data/assets/nonefont_32")
    create_dither_images("data/assets/dither_images")
    print("画像の自動生成が完了しました！")
