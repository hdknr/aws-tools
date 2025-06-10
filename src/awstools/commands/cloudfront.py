"""

Required actions:

"Action": [
      ]

"""

import click

from logging import getLogger
from ..libs import cloudfront as cloudfront_lib
import re

logger = getLogger()


@click.group()
@click.pass_context
def cloudfront(ctx):
    pass


def get_params_from_item(item):
    """
    cluser/service/desired_count
    """
    ma = re.search(r"^([^/]+)/([^/]+)/([^/]+)$", item)
    return ma and ma.groups()


@cloudfront.command()
@click.argument("dist_id")
@click.argument("new_origin_id")
@click.argument("path_pats", nargs=-1)
@click.pass_context
def update_origin(ctx, dist_id, new_origin_id, path_pats):
    """cloudfrontのビヘイビアのオリジンを変更する"""
    cloudfront_lib.update_origin(dist_id, new_origin_id, *path_pats)
