*This project has been created as part of the 42 curriculum by ayhirose.*

# PACMAN against the machine

### Description
代表的な2Dゲーム「PACMAN」の実装とリリース。

**個人目標**
- CPU単独での高速な回答


**使用したパッケージ**
>パッケージ管理は`python uv`を使用しています
```
flake8>=7.3.0
flake8-bugbear>=25.11.29
flake8-pyproject
mypy>=1.19.1
pep8-naming>=0.15.1
pydantic>=2.12.5
flake8-docstrings
```


**ディレクトリ構成**
```
.
├── Makefile
├── README.md             # 英語ドキュメント (要件指定)
├── README_JP.md          # 日本語ドキュメント
├── pyproject.toml        # 依存ライブラリやリンター(flake8, mypy)の設定
├── uv.lock               # uvの依存関係ロックファイル
├── .gitignore
├── .python-version
│
├── src/
│   ├── __main__.py   # 実行時のモジュールエントリーポイント
│   ├── __init__.py
│   ├── cli.py        # CLIコマンドの定義 (Fire)
│   └── core/         # PACMANシステムのコアロジック
│        ├── answer.py     # 回答生成モジュール (llama.cpp)
│        ├── evaluater.py  # 評価モジュール
│        ├── indexer.py    # チャンク化・インデックス作成モジュール
│        ├── models.py     # Pydanticを用いたデータモデル定義
│        └── searcher.py   # BM25を用いた検索モジュール
│
├── data/                 # データ格納ディレクトリ
│   ├── setting/          # ゲームの各種設定ファイルを格納
│   ├── score/            # ゲームのスコアリングを格納(永続保存 or Playfab)
│   └── map/              # マップを生成するジェネレータと生成物を格納
└── docs_management/      # プロジェクトの
```

### Instructions

このプログラムは Python 3.10以上 での実行が前提です。パッケージ管理には uv を使用しています。

1. **インストール**
```bash
make install
```
仮想環境（.venv）を構築し、必要な依存関係をインストールします。\
課題で必須になる、mazegenerator-00001-py3-none-any.whlのインストールも同時に行います。(`data/map`)


2. **実行**
```bash
make run
```
メインプログラムのヘルプが表示されます。\
実行方法は多岐に渡るためrunコマンドではヘルプが表示されます。
>**注意**\
プログラムは依存関係のないグローバル環境では必ずしも正しく実行されるとは限りません。\
先に`make install`にてインストールした`.venv`上にて実行してください。\
実行方法
`uv run <実行プログラム>`


3. **他の `Makefile` コマンド**
```bash
make lint
make lint-strict
```
flake8 と mypy による静的型解析を実行します。

```bash
make debug
```
pdb を使用したデバッグモードで実行します。

```bash
make clean
```
キャッシュファイルを削除します。
仮想環境の削除も含むfcleanも同様に使用できます。


## Additional sections


### Resources

AI
- 制約付きデコーディングにおけるLogits操作のアルゴリズム設計とデバッグの壁打ち。
- `flake8` および `mypy` のエラーログ解析と `pyproject.toml` の最適化。
- DocstringおよびREADMEの英訳、構成支援。

`python uv`公式ドキュメント、公式AI\
`langchain`公式ドキュメント、公式AI\
`llama-cpp-python`公式ドキュメント、公式AI
