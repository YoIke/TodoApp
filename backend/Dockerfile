# 使用するPythonのバージョンを指定
FROM python:3.10

# タイムゾーンを日本時間に設定
ENV TZ=Asia/Tokyo

# アプリケーションディレクトリを作成
WORKDIR /usr/src/app

# Pythonの依存関係をインストール
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Gunicornをインストール
RUN pip install gunicorn

# srcディレクトリ内のアプリケーションのソースをコピー
COPY src/ .

# アプリケーションのポートを公開
EXPOSE 8001

# Gunicornでアプリケーションを起動
CMD ["gunicorn", "-b", "0.0.0.0:8001", "app:create_app()"]
