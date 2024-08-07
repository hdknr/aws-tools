"""

Required actions:

"Action": [
	"ec2:DescribeInstanceStatus",
	"ec2:DescribeInstances",
	"ec2:StartInstances",
	"ec2:StopInstances"
]

"""

import click

from logging import getLogger
from ..libs import ec2 as ec2_lib

logger = getLogger()


@click.group()
@click.pass_context
def ec2(ctx):
    pass


@ec2.command()
@click.argument("tags", nargs=-1)
@click.pass_context
def restart_instances(ctx, tags):
    """タグで指定されたインスタンスを再起動する"""
    instances = ec2_lib.get_instances_tags(tags)
    ec2_lib.restart_instances_all(instances)
