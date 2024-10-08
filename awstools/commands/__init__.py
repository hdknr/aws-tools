#!/usr/bin/env python
import os
import boto3
import click
from logging import getLogger
from .ec2 import ec2
from .rds import rds
from .ecs import ecs
from .cloudfront import cloudfront


logger = getLogger()


@click.group()
@click.option("--tf_output", "-to", default=None)
@click.pass_context
def main(ctx, tf_output):
    ctx.ensure_object(dict)


main.add_command(ec2)
main.add_command(rds)
main.add_command(ecs)
main.add_command(cloudfront)
