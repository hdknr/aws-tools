#!/bin/sh
if [ -f $1 ]; then
    export $(cat $1|grep -v "^#"|xargs)
fi
REPO=${ECR_LAMBDA}
TAG=latest

ECR=$(aws ecr describe-repositories --repository-names $REPO --region ${AWS_REGION} | jq -r ".repositories[0].repositoryUri")
aws ecr get-login-password  --region ${AWS_REGION}  | docker login --username AWS --password-stdin ${ECR}
docker tag ${REPO}:${TAG} ${ECR}:${TAG}
docker push ${ECR}:${TAG}