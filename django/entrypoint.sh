#!/bin/sh

# Djangoのマイグレーションを実行
python3 src/manage.py migrate

# 静的ファイルを収集
python3 src/manage.py collectstatic --noinput

# サーバーの起動
exec "$@"
