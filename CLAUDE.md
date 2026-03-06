# aws-tools

AWS 操作用 CLI ツール (Python/Click)。

## プロジェクト構成

- `src/awstools/commands/` - CLI コマンド定義 (click グループ: ec2, rds, ecs, cloudfront, cwl, ses)
- `src/awstools/libs/` - 各サービスのビジネスロジック
- `src/awstools/commands/__init__.py` - エントリポイント (`awstools` コマンド)
- `lambda/` - Lambda ハンドラー & Dockerfile
- `bin/` - シェルスクリプト (ECR ログイン/ビルド/プッシュ等)
- `Dockerfile` - ローカル実行用コンテナ (ARM64, python:3, uv, aws-cli, opentofu)
- `docker-compose.yml` - local サービスと lambda サービス

## 開発コマンド

```bash
# CLI 実行
uv run awstools --help

# フォーマット & リント
uv run ruff format .
uv run ruff check . --fix

# Docker ローカル実行
docker compose --env-file .env.test run --rm local bin/app.py ec2 --help

# Docker イメージビルド
docker build --platform linux/arm64 --build-arg BASE=/home/tool -t aws-tools:latest .
```

## 技術スタック

- Python 3.12, uv (パッケージ管理)
- Click (CLI フレームワーク), boto3 (AWS SDK), pandas
- hatchling (ビルドシステム)
- ruff (フォーマッター & リンター)
