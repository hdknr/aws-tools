#!/bin/sh
if [ -f $1 ]; then
    export $(cat $1|grep -v "^#"|xargs)
fi

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws