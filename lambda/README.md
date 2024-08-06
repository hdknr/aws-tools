# lambda

## AWS

- https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html

## Build

```bash
AWS_PROFILE=connect aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

```bash
docker build  -f lambda/Dockerfile -t awstool_lambda --no-cache .
```
