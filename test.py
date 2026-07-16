import arcade

# 📏 ウィンドウの定数設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Test - Hello Pacman!"

class MyGame(arcade.Window):
    """ メインのゲームクラス """

    def __init__(self, width, height, title):
        # 親クラス（arcade.Window）の初期化を呼び出す
        super().__init__(width, height, title)

        # 背景色を「黒」に設定
        arcade.set_background_color(arcade.color.BLACK)

        # 🟡 キャラクターの初期座標とスピード
        self.player_x = width / 2
        self.player_y = height / 2
        self.velocity_x = 5

    def setup(self):
        """ ゲームの初期設定（リセット時などにも呼ばれる） """
        pass

    def on_draw(self):
        """ 🎨 画面の描画（1フレームごとに呼ばれる） """
        # 描画を始める前に、前のフレームの絵を消して画面をクリアする
        self.clear()

        # 黄色い円（パックマンの代わり）を描画
        # 引数：(x座標, y座標, 半径, 色)
        arcade.draw_circle_filled(self.player_x, self.player_y, 30, arcade.color.YELLOW)

    def on_update(self, delta_time):
        """ ⚙️ ロジックの更新（約1/60秒ごとに呼ばれる） """
        # キャラクターを移動させる
        self.player_x += self.velocity_x

        # 画面の端（右端・左端）にぶつかったら反転してバウンドする
        if self.player_x > SCREEN_WIDTH - 30 or self.player_x < 30:
            self.velocity_x *= -1

def main():
    """ メイン処理 """
    # ウィンドウを作成
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    # ゲームの初期セットアップ
    window.setup()
    # ゲームループを開始（ウィンドウの×ボタンが押されるまで動き続ける）
    arcade.run()

if __name__ == "__main__":
    main()
