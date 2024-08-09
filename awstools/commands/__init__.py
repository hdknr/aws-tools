#!/usr/bin/env python
import os
import boto3
import click
from logging import getLogger
from .ec2 import ec2
from .rds import rds


logger = getLogger()


def setup_boto3():
    keys = {
        "profile_name": "AWS_PROFILE",
        "region_name": "AWS_REGION",
        "aws_access_key_id": "AWS_ACCESS_KEY_ID",
        "aws_secret_access_key": "AWS_SECRET_ACCESS_KEY",
    }
    params = dict((k, os.environ[v]) for k, v in keys.items() if v in os.environ)
    boto3.setup_default_session(**params)


@click.group()
@click.option("--tf_output", "-to", default=None)
@click.pass_context
def main(ctx, tf_output):
    ctx.ensure_object(dict)
    setup_boto3()


main.add_command(ec2)
main.add_command(rds)
