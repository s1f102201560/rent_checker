# ベースイメージ
FROM python:3.12

# 環境変数の設定
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONPATH=/code/src

# 作業ディレクトリの設定
WORKDIR /code

# 必要なパッケージのインストール
RUN apt-get update 
RUN apt-get install -y ca-certificates curl gnupg
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update
RUN apt-get install nodejs -y

# Python依存パッケージのインストール
COPY ./django/requirements.txt /code/django/
RUN pip install -r /code/django/requirements.txt

# ソースコードのコピー
COPY ./src /code/src
COPY ./django/entrypoint.sh /code/django/entrypoint.sh

# 実行権限を付与
RUN chmod +x /code/django/entrypoint.sh

# ポートの公開
EXPOSE 8000

# エントリーポイントの設定
ENTRYPOINT ["/code/django/entrypoint.sh"]

# サーバーの起動
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
