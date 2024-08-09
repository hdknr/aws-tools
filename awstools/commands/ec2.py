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
@click.argument("items", nargs=-1)
@click.pass_context
def restart_instances(ctx, items):
    """ID/タグで指定されたインスタンスを再起動する"""
    tags = [i for i in items if i.find("=") > 0]
    if tags:
        instances = ec2_lib.get_instances_tags(tags)
        ec2_lib.restart_instances_all(instances)
    ids = [i for i in items if i.startswith("i-")]
    list(map(ec2_lib.restart, ids))
