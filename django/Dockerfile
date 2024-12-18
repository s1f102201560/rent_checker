# ベースイメージ
FROM python:3.12-slim

# 環境変数の設定
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings \
    PYTHONPATH=/code/src

# 作業ディレクトリの設定
WORKDIR /code

# 必要なパッケージのインストールとキャッシュの削除
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        tesseract-ocr \
        tesseract-ocr-jpn && \
    rm -rf /var/lib/apt/lists/*

# Node.jsのインストール
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# Python依存パッケージのインストール
COPY ./django/requirements.txt /code/django/
RUN pip install --no-cache-dir -r /code/django/requirements.txt

# ソースコードとエントリーポイントのコピー
COPY ./src /code/src
COPY ./django/entrypoint.sh /code/django/entrypoint.sh

# 実行権限を付与
RUN chmod +x /code/django/entrypoint.sh

# ポートの公開
EXPOSE 8000

# エントリーポイントの設定
ENTRYPOINT ["/code/django/entrypoint.sh"]

# サーバーの起動
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
