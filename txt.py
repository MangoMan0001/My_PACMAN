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
    font = pygame.font.Font(None, 128)

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


def _safe_font(path: str, size: int) -> pygame.font.Font:
    """指定パスのフォントを読み込む。存在しなければpygame既定フォントにフォールバックする。

    Args:
        path (str): フォントファイルのパス。
        size (int): フォントサイズ。

    Returns:
        pygame.font.Font: 読み込んだフォント(失敗時は既定フォント)。
    """
    try:
        return pygame.font.Font(path, size)
    except OSError:
        return pygame.font.Font(None, size)


def create_how_to_play_image(output_dir: str) -> None:
    """How to Play画面用の1枚絵(1920x1080)を生成する。

    黒背景の中央やや上に「白地・灰色縁の角丸四角」を置き、その中に操作方法を描く。
    四角の下(画面下部)には戻り方の文字("PRESS ESC TO BACK")を配置する。
    生成物: <output_dir>/how_to_play.png

    Args:
        output_dir (str): 画像の出力先ディレクトリ。
    """
    pygame.font.init()

    # ---- 色定義(白地でも読める濃さに調整) ----
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (150, 150, 150)
    title_color = (25, 25, 90)
    heading_color = (40, 40, 120)
    body_color = (30, 30, 30)
    bottom_color = (255, 255, 0)
    ghost_colors = {
        "blinky": (208, 0, 0),      # 赤
        "pinky": (222, 90, 160),    # ピンク
        "inky": (0, 160, 185),      # 水色
        "clyde": (225, 135, 0),     # オレンジ
    }

    # ---- 画面と角丸ボックス ----
    width, height = 1920, 1080
    screen = pygame.Surface((width, height))
    screen.fill(black)

    # 下に戻り方テキストの余白を残すため、四角は中央やや上に置く
    box_x, box_y = 230, 70
    box_w, box_h = 1460, 900
    box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
    pygame.draw.rect(screen, white, box_rect, border_radius=40)
    pygame.draw.rect(screen, gray, box_rect, width=6, border_radius=40)

    center_x = box_x + box_w // 2   # 画面中央(=960)
    inner_x = box_x + 90            # 本文の左端

    # ---- フォント(タイトルはPac風、本文は既定の読みやすいフォント) ----
    title_font = _safe_font("data/font/pacmania/Pacmania.otf", 90)
    heading_font = pygame.font.Font(None, 64)
    body_font = pygame.font.Font(None, 46)
    ghost_font = pygame.font.Font(None, 46)
    bottom_font = _safe_font("data/font/pacmania/Pacmania.otf", 54)

    def blit_center(image: pygame.Surface, top_y: int) -> None:
        """画像をボックス中央に横中央寄せで貼る。"""
        screen.blit(image, (center_x - image.get_width() // 2, top_y))

    def blit_text(text: str, font: pygame.font.Font,
                  color: tuple[int, int, int], x: int, top_y: int) -> int:
        """左寄せで文字列を描画し、描画した画像の幅を返す。"""
        image = font.render(text, True, color)
        screen.blit(image, (x, top_y))
        return image.get_width()

    # ---- タイトル ----
    title_image = title_font.render("HOW TO PLAY", True, title_color)
    blit_center(title_image, box_y + 45)
    y = box_y + 45 + title_image.get_height() + 30

    # ---- CONTROLS ----
    blit_text("CONTROLS", heading_font, heading_color, inner_x, y)
    y += 68
    blit_text("Move : Arrow Keys  or  W / A / S / D",
              body_font, body_color, inner_x + 20, y)
    y += 80

    # ---- RULES ----
    blit_text("RULES", heading_font, heading_color, inner_x, y)
    y += 68
    blit_text("Eat all Pac-Gum to clear the stage.",
              body_font, body_color, inner_x + 20, y)
    y += 56
    blit_text("Grab a Super Pac-Gum to eat ghosts for a short time!",
              body_font, body_color, inner_x + 20, y)
    y += 80

    # ---- GHOSTS ----
    blit_text("GHOSTS", heading_font, heading_color, inner_x, y)
    y += 70

    ghost_lines = [
        ("blinky", "Blinky", "chases Pac-Man directly."),
        ("pinky", "Pinky", "aims a few tiles ahead of you."),
        ("inky", "Inky", "ambushes together with Blinky."),
        ("clyde", "Clyde", "wanders, but runs away when you get close."),
    ]
    icon_size = 64
    for key, name, desc in ghost_lines:
        text_x = inner_x + 20
        # ゴーストのスプライトをアイコンとして左に貼る(無ければ文字だけ)
        icon_path = os.path.join(
            "data", "assets", "ghost", f"ghost_{key}_right_0.png")
        if os.path.exists(icon_path):
            icon = pygame.image.load(icon_path)
            icon = pygame.transform.scale(icon, (icon_size, icon_size))
            screen.blit(icon, (inner_x + 20, y - 8))
            text_x = inner_x + 20 + icon_size + 24
        # 「名前(ゴースト色)」＋「説明(黒)」を横に並べる
        name_width = blit_text(
            f"{name} : ", ghost_font, ghost_colors[key], text_x, y)
        blit_text(desc, ghost_font, body_color, text_x + name_width, y)
        y += icon_size + 10

    # ---- 保存 ----
    pygame.image.save(screen, os.path.join(output_dir, "how_to_play.png"))


if __name__ == "__main__":
    # os.makedirs("data/assets/Pacman", exist_ok=True)
    # os.makedirs("data/assets/upper_256", exist_ok=True)
    # os.makedirs("data/assets/lower_128", exist_ok=True)
    # os.makedirs("data/assets/nonefont_32", exist_ok=True)
    os.makedirs("data/assets/dither_images", exist_ok=True)
    os.makedirs("data/assets/how_to_play", exist_ok=True)

    # create_pacman_images("data/assets/Pacman")
    # create_font_upper_images("data/assets/upper_256")
    # create_font_lower_images("data/assets/lower_128")
    # create_font_none_images("data/assets/nonefont_32")
    create_dither_images("data/assets/dither_images")
    create_how_to_play_image("data/assets/how_to_play")
    print("画像の自動生成が完了しました！")
