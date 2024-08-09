#!/bin/sh
if [ -f $1 ]; then
    export $(cat $1|grep -v "^#"|xargs)
fi
#
DOCKERFILE=lambda/Dockerfile
REPO=${ECR_LAMBDA}
#
CONTEXT_DIR=.
TAG=latest

docker build -t ${REPO} --no-cache -f ${DOCKERFILE} ${CONTEXT_DIR}