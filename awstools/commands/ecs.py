"""

Required actions:

"Action": [
      ""ecs:UpdateService",
      ]

"""

import click

from logging import getLogger
from ..libs import ecs as ecs_lib
import re

logger = getLogger()


@click.group()
@click.pass_context
def ecs(ctx):
    pass


def get_params_from_item(item):
    """
    cluser/service/desired_count
    """
    ma = re.search(r"^([^/]+)/([^/]+)/([^/]+)$", item)
    return ma and ma.groups()


@ecs.command()
@click.argument("items", nargs=-1)
@click.pass_context
def set_desired_count(ctx, items):
    """ECSのタスク数を変更する"""
    params = filter(lambda i: i is not None, map(get_params_from_item, items))
    for param in params:
        ecs_lib.update_desired_count(*param)
