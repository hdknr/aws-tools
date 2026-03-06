"""

Required actions:

"Action": [
      "rds:StopDBInstance",
      "rds:StartDBInstance",
      "rds:StopDBCluster",
      "rds:StartDBCluster",
      ]

"""

import click

from logging import getLogger
from ..libs import rds as rds_lib

logger = getLogger()


@click.group()
@click.pass_context
def rds(ctx):
    pass


@rds.command()
@click.argument("items", nargs=-1)
@click.pass_context
def start_rds(ctx, items):
    """ID/タグで指定されたインスタンスを起動する"""

    for i in items:
        rds_lib.start(i)


@rds.command()
@click.argument("items", nargs=-1)
@click.pass_context
def stop_rds(ctx, items):
    """ID/タグで指定されたインスタンスを停止する"""

    for i in items:
        rds_lib.stop(i)


@rds.command()
@click.argument("items", nargs=-1)
@click.pass_context
def start_cluster(ctx, items):
    """ID/タグで指定されたクラスターを起動する"""

    for i in items:
        rds_lib.start_cluster(i)


@rds.command()
@click.argument("items", nargs=-1)
@click.pass_context
def stop_cluster(ctx, items):
    """ID/タグで指定されたクラスターを停止する"""

    for i in items:
        rds_lib.stop_cluster(i)
