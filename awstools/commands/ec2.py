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


def get_id_from_items(items):
    ids = [i for i in items if i.startswith("i-")]
    tags = [i for i in items if i.find("=") > 0]

    if tags:
        response = ec2_lib.get_instances_tags(tags)
        ids = ids + ec2_lib.get_ids_from_response(response)
    return ids


@ec2.command()
@click.argument("items", nargs=-1)
@click.pass_context
def restart_instances(ctx, items):
    """ID/タグで指定されたインスタンスを再起動する"""

    ids = get_id_from_items(items)
    list(map(ec2_lib.restart, ids))


@ec2.command()
@click.argument("items", nargs=-1)
@click.pass_context
def start_instances(ctx, items):
    """ID/タグで指定されたインスタンスを起動する"""

    ids = get_id_from_items(items)
    list(map(ec2_lib.start, ids))


@ec2.command()
@click.argument("items", nargs=-1)
@click.pass_context
def stop_instances(ctx, items):
    """ID/タグで指定されたインスタンスを停止する"""

    ids = get_id_from_items(items)
    list(map(ec2_lib.stop, ids))
