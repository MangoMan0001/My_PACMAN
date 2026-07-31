import pygame
from pathlib import Path


class ImageFont:
    def __init__(
        self,
        image_dir: Path,
        filename_pattern: str = "PAC-FONT_{char}.png",
        spcae_width: int = 64,
        letter_spacing: int = 10
    ) -> None:
        self.image_dir = image_dir
        self.filename_pattern = filename_pattern
        self.space_width = spcae_width
        self.letter_spacing = letter_spacing
        self._cache: dict[str, pygame.Surface | None] = {}

    def _load_char_image(self, char: str) -> pygame.Surface | None:
        if char in self._cache:
            return self._cache[char]

        filename = self.filename_pattern.format(char=char)
        image_path = self.image_dir / filename
        if not image_path.exists():
            self._cache[char] = None
            return None

        image = pygame.image.load(str(image_path)).convert_alpha()
        self._cache[char] = image
        return image

    def render_text(self, text: str) -> pygame.Surface:
        pieces: list[tuple[pygame.Surface | None, int]] = []
        for char in text:
            if char == " ":
                pieces.append((None, self.space_width))
                continue
            image = self._load_char_image(char)
            if image is None:
                pieces.append((None, self.space_width))
            else:
                pieces.append((image, image.get_width()))
        total_width = sum(width for _, width in pieces)
        if len(pieces) > 1:
            total_width += self.letter_spacing * (len(pieces) - 1)
        height = 0
        for image, _ in pieces:
            if image is not None:
                height = max(height, image.get_height())
        total_width = max(total_width, 1)
        height = max(height, 1)

        text_image = pygame.Surface((total_width, height), pygame.SRCALPHA)

        cursor_x = 0
        for image, width in pieces:
            if image is not None:
                text_image.blit(image, (cursor_x, 0))
            cursor_x += width + self.letter_spacing
        return text_image
