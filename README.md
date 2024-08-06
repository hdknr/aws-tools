# aws-tools

## docker

### ローカルコマンド実行

```bash
docker compose run --rm tool bin/app.py ec2 hello test
```

### lambda ローカルテスト

公式イメージを pull するので AWS にログインしておくこと

```bash
AWS_PROFILE=your_profile aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

```bash
docker compose up  lambda -d
```

```bash
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"args": ["ec2", "hello", "test"]}'
```
