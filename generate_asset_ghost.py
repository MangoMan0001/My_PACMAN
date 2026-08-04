import pygame
import os


def create_ghost_sprites(output_dir: str) -> None:
    pygame.init()
    size = 24
    colors = {
        "blinky": (255, 0, 0),      # 赤 (Blinky)
        "pinky":  (255, 182, 193),  # ピンク (Pinky)
        "inky":   (0, 255, 255),    # 水色 (Inky)
        "clyde":  (255, 165, 0)     # オレンジ (Clyde)
    }

    # 1. 方向ごとの「顔（白目＋黒目）全体」のシフト量 (dx, dy)
    # これにより、白目ごとそっちの方向に移動するため「顔ごと向いている」表現になります
    face_offsets = {
        "up":    (0, -2),
        "down":  (0, 2),
        "left":  (-2, 0),
        "right": (2, 0)
    }

    for name, color in colors.items():
        for direction, (dx, dy) in face_offsets.items():
            for anim_frame in [0, 1]:
                surface = pygame.Surface((size, size), pygame.SRCALPHA)

                # 頭と胴体を描画
                pygame.draw.circle(surface, color, (12, 10), 9)
                pygame.draw.rect(surface, color, (3, 10, 18, 9))

                # 足のパタパタアニメーション
                if anim_frame == 1:
                    pygame.draw.polygon(surface, (0, 0, 0, 0), [(3, 19), (7, 19), (5, 15)])
                    pygame.draw.polygon(surface, (0, 0, 0, 0), [(11, 19), (15, 19), (13, 15)])
                    pygame.draw.polygon(surface, (0, 0, 0, 0), [(19, 19), (21, 19), (20, 15)])
                else:
                    pygame.draw.polygon(surface, (0, 0, 0, 0), [(3, 19), (9, 19), (6, 15)])
                    pygame.draw.polygon(surface, (0, 0, 0, 0), [(13, 19), (19, 19), (16, 15)])

                # 白目の基準位置に方向ごとのオフセットを適用
                base_left_eye = (8, 9)
                base_right_eye = (16, 9)

                left_eye_center = (base_left_eye[0] + dx, base_left_eye[1] + dy)
                right_eye_center = (base_right_eye[0] + dx, base_right_eye[1] + dy)

                # 白目描画
                pygame.draw.circle(surface, (255, 255, 255), left_eye_center, 3)
                pygame.draw.circle(surface, (255, 255, 255), right_eye_center, 3)

                # 黒目描画（白目の中心からさらに少しだけズラすとより生き生きします）
                left_pupil = (left_eye_center[0] + (1 if dx > 0 else -1 if dx < 0 else 0),
                              left_eye_center[1] + (1 if dy > 0 else -1 if dy < 0 else 0))
                right_pupil = (right_eye_center[0] + (1 if dx > 0 else -1 if dx < 0 else 0),
                               right_eye_center[1] + (1 if dy > 0 else -1 if dy < 0 else 0))

                pygame.draw.circle(surface, (0, 0, 255), left_pupil, 1)
                pygame.draw.circle(surface, (0, 0, 255), right_pupil, 1)

                filename = f"ghost_{name}_{direction}_{anim_frame}.png"
                pygame.image.save(surface, os.path.join(output_dir, filename))

    # 2. いじけモード（Scared Mode）の画像生成
    # パワークッキー取得時の青いゴースト（2フレーム分のパタパタ付き）
    scared_color = (30, 144, 255)  # 鮮やかな青
    for anim_frame in [1, 2]:
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surface, scared_color, (12, 10), 9)
        pygame.draw.rect(surface, scared_color, (3, 10, 18, 9))

        if anim_frame == 1:
            pygame.draw.polygon(surface, (0, 0, 0, 0), [(3, 19), (7, 19), (5, 15)])
            pygame.draw.polygon(surface, (0, 0, 0, 0), [(11, 19), (15, 19), (13, 15)])
            pygame.draw.polygon(surface, (0, 0, 0, 0), [(19, 19), (21, 19), (20, 15)])
        else:
            pygame.draw.polygon(surface, (0, 0, 0, 0), [(3, 19), (9, 19), (6, 15)])
            pygame.draw.polygon(surface, (0, 0, 0, 0), [(13, 19), (19, 19), (16, 15)])

        # いじけ中の怯えた目（小さめの白い目＋ピンクの瞳）
        pygame.draw.circle(surface, (255, 255, 255), (8, 9), 2)
        pygame.draw.circle(surface, (255, 255, 255), (16, 9), 2)
        pygame.draw.circle(surface, (255, 182, 193), (8, 9), 1)
        pygame.draw.circle(surface, (255, 182, 193), (16, 9), 1)

        filename = f"ghost_scared_{anim_frame}.png"
        pygame.image.save(surface, os.path.join(output_dir, filename))


if __name__ == "__main__":
    os.makedirs("assets/ghost", exist_ok=True)
    create_ghost_sprites("assets/ghost")
    print("ゴーストの全方向（顔向き調整済）＆いじけモード画像を生成しました！")
