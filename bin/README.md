# スクリプト

## ECRにプッシュ

.envファイルを用意:

```ini
AWS_ACCESS_KEY_ID=*****
AWS_SECRET_ACCESS_KEY=*****
AWS_REGION=ap-northeast-1
ECR_LAMBDA=sample-devel-tool
```

ビルドとプッシュ:

```bash
bin/ecr_login.bash  .env.sample
bin/ecr_build.bash  .env.sample
bin/ecr_push.bash  .env.sample
```
