import click

from logging import getLogger
from ..libs import ses as ses_lib
import json

logger = getLogger()


@click.group()
@click.pass_context
def ses(ctx):
    pass


@ses.command()
@click.argument("address", nargs=-1)
@click.pass_context
def desc_address(ctx, address):
    """Emailアドレスのサプレッションリスト確認"""
    if not address:
        res = ses_lib.get_all_suppressed_destinations()
        print(json.dumps(res, indent=2, ensure_ascii=False, default=str))
        return

    for email in address:
        res = ses_lib.get_suppressed_destination_details(email)
        print(json.dumps(res, indent=2, ensure_ascii=False, default=str))


@ses.command()
@click.argument("address", nargs=-1)
@click.pass_context
def remove_suppressed_address(ctx, address):
    """サプレッションリストから削除"""
    for email in address:
        res = ses_lib.delete_email_from_suppression_list(email)
        print(email, res)
