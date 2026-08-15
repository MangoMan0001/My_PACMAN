"""data/assetsから文字画像を読み込んで文字列を描画するためのクラス.

描画する文字のフォントファイル名は"*{char}*.png"である必要がある。
imagefont(ディレクトリ名、ファイル名のパターン)で初期化し、render_text(文字列)で
文字列を描画したSurfaceを返す。
例:
    font = ImageFont(Path("pacfont_64"), "PAC-FONT_{char}.png")
    text_image = font.render_text("HELLO")
    pygame.Surface.blit(text_image, (x, y))で描画する。
"""
import pygame
from pathlib import Path


class ImageFont:
    """文字画像を読み込み、文字列を1枚の画像(Surface)として合成するクラス.

    文字画像は、事前に大きさ、色、フォント等を調整しdata/assetsに置いておく必要がある。
    読み込んだ画像はキャッシュし、存在しない文字は空白幅の画像を入れる。

    Attributes:
        image_dir (Path): 文字画像が格納されているディレクトリ
        filename_pattern (str): 文字画像のファイル名のパターン。{char}が文字に置き換えられる。
        space_width (int): 空白文字の幅
        letter_spacing (int): 文字間のスペース幅
        _cache (dict[str, pygame.Surface | None]): 文字画像のキャッシュ
    """

    def __init__(
        self,
        image_dir: Path,
        filename_pattern: str = "PAC-FONT_{char}.png",
        space_width: int = 16,
        letter_spacing: int = 10,
    ) -> None:
        """image_fontクラスのコンストラクタ."""
        asset_root = Path(__file__).resolve().parents[2] / "data" / "assets"
        self.image_dir = asset_root / image_dir
        self.filename_pattern = filename_pattern
        self.space_width = space_width
        self.letter_spacing = letter_spacing
        self._cache: dict[str, pygame.Surface | None] = {}

    def _load_char_image(self, char: str) -> pygame.Surface | None:
        """1文字の画像を読み込み、キャッシュする.

        mlx_png_file_to_image()相当の処理。
        convert_alphaは事前にset_mode()でディスプレイが初期化されていないとエラーになる。

        Args:
            char (str): 読み込む対象の文字。

        Returns:
            pygame.Surface | None: 文字画像。文字画像が存在しない場合はNoneを返す。
        """
        # キャッシュがあれば即時に返す。
        if char in self._cache:
            return self._cache[char]

        # デフォルトで"PAC-FONT_{char}.png"を読み込む。
        filename = self.filename_pattern.format(char=char)
        image_path = self.image_dir / filename
        if not image_path.exists():
            self._cache[char] = None
            return None

        # convert_alpha()を使ってmlxと同じく透過情報を持つSurfaceに変換する。
        image = pygame.image.load(str(image_path)).convert_alpha()
        # キャッシュに保存してから返す。
        self._cache[char] = image
        return image

    def render_text(self, text: str) -> pygame.Surface:
        """文字列を1枚の画像(Surface)として合成する.

        受け取ったテキストの各文字を横に並べる。
        スペースと存在しない文字はspace_width分の空白を入れる。
        実行時に色、サイズ、フォントの変更はできないため、事前に文字画像を作成しておく必要がある。

        mlx_new_image()、mlx_image_to_window()相当の処理。
        pygame.SRCALPHAは(R, G, B, A)の4番目のアルファ値(透明度)を持つSurfaceを作成するためのフラグ。
        Surface全体の透明度とは別に個々のピクセルの透明度を変えられるらしい。

        Args:
            text (str): 描画する文字列。

        Returns:
            pygame.Surface: 文字列を描画した画像(Surface)。
        """
        # 文字画像かNoneと横幅のタプルのリストを作成する。
        pieces: list[tuple[pygame.Surface | None, int]] = []
        for char in text:
            # スペースは空白幅を入れる。
            if char == " ":
                pieces.append((None, self.space_width))
                continue
            # 文字画像の取得
            image = self._load_char_image(char)
            # 文字画像がなければ空白幅を入れる。
            if image is None:
                pieces.append((None, self.space_width))
            # 文字画像があればその幅を入れる。
            else:
                pieces.append((image, image.get_width()))

        # 全体の幅の合計を計算。
        total_width = sum(width for _, width in pieces)
        # 文字間隔を加算する。文字数が1文字以下の場合は加算しない。
        if len(pieces) > 1:
            total_width += self.letter_spacing * (len(pieces) - 1)

        # 文字画像の高さで一番高い高さを全体の高さとしてする。
        height = 0
        for image, _ in pieces:
            if image is not None:
                height = max(height, image.get_height())

        # 空文字の場合でも1x1の透明画像を返す。
        total_width = max(total_width, 1)
        height = max(height, 1)

        # 文字列を描画するためのSurface(土台)を作成する。
        text_image = pygame.Surface((total_width, height), pygame.SRCALPHA)
        # 左の文字から順に土台に文字画像を貼り付けていく。
        cursor_x = 0
        for image, width in pieces:
            if image is not None:
                text_image.blit(image, (cursor_x, 0))
            cursor_x += width + self.letter_spacing

        return text_image
