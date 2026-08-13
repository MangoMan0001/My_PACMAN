#!/bin/bash

# エラーが起きたら途中でスクリプトを止める
set -e

# 古いビルドデータを削除
echo "removing old build files..."
rm -rf build dist

echo "start packaging..."

# 1. 古いビルドの掃除と、.specファイルを使ったビルドの実行
echo "building by pyinstaller..."
uv run pyinstaller PacMan.spec --clean -y

# 2. 必要な外部ファイルのコピー
echo "copying external files..."
cp config.json dist/PacMan/
cp how_to_play.txt dist/PacMan/

# 3. Itch.io提出用のZipファイルを作成
echo "creating zip file..."
cd dist
zip -r PacMan-Release.zip PacMan/
cd ..

# 使用しないビルドデータを削除
echo "removing build files..."
rm -rf build

echo "✅ Complet Packaging."
