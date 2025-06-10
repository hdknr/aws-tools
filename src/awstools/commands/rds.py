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

    ids = items
    list(map(rds_lib.start, ids))


@rds.command()
@click.argument("items", nargs=-1)
@click.pass_context
def stop_rds(ctx, items):
    """ID/タグで指定されたインスタンスを停止する"""

    ids = items
    list(map(rds_lib.stop, ids))


@rds.command()
@click.argument("items", nargs=-1)
@click.pass_context
def start_cluster(ctx, items):
    """ID/タグで指定されたクラスターを起動する"""

    ids = items
    list(map(rds_lib.start_cluster, ids))


@rds.command()
@click.argument("items", nargs=-1)
@click.pass_context
def stop_cluster(ctx, items):
    """ID/タグで指定されたクラスターを停止する"""

    ids = items
    list(map(rds_lib.stop_cluster, ids))
