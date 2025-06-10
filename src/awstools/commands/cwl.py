"""
cloudwatch logs
"""

import click
import pandas as pd

from logging import getLogger
from ..libs import cwl as cwl_lib

logger = getLogger()


@click.group()
@click.pass_context
def cwl(ctx):
    pass


@cwl.command()
@click.option("--prefix", "-p", default=None)
@click.pass_context
def list_groups(ctx, prefix):
    """ロググループ一覧"""
    client = cwl_lib.get_client()
    limit = 50
    next_token = None
    #
    params = {"limit": limit}
    if prefix:
        params["logGroupNamePrefix"] = prefix
    if next_token:
        params["nextToken"] = next_token
    response = client.describe_log_groups(**params)
    log_groups = response["logGroups"]

    print(pd.DataFrame(log_groups)[["logGroupName"]].to_csv(index=False))


@cwl.command()
@click.argument("log_group_name")
@click.option("--stream_count", "-c", default=10)
@click.pass_context
def list_streams(ctx, log_group_name, stream_count):
    """ストリーム一覧"""
    client = cwl_lib.get_client()

    next_token = None
    log_stream_name_prefix = None
    limit = 50
    order_by = "LastEventTime"

    params = {
        "logGroupName": log_group_name,
        "limit": limit,
        "orderBy": order_by,
        "descending": True,  # 最新のログストリームから取得する場合に True に設定
    }
    if log_stream_name_prefix:
        params["logStreamNamePrefix"] = log_stream_name_prefix
    if next_token:
        params["nextToken"] = next_token

    response = client.describe_log_streams(**params)

    log_streams = response["logStreams"]
    df = pd.DataFrame(log_streams)
    df["lastEventTimestamp"] = (
        pd.to_datetime(df["lastEventTimestamp"], unit="ms", errors="coerce")
        .dt.tz_localize("UTC")
        .dt.tz_convert("Asia/Tokyo")
    )
    print(df[["logStreamName", "lastEventTimestamp"]].to_csv(index=False))


@cwl.command()
@click.argument("log_group_name")
@click.argument("log_stream_name")
@click.option("--out", "-o", default=None)
@click.pass_context
def fetch_streams(ctx, log_group_name, log_stream_name, out):
    """ストリームダウンロード"""
    out = out or "/tmp/event.csv"
    events = cwl_lib.fech_stream_events(log_group_name, log_stream_name)

    df = pd.DataFrame(events)
    for i in ["timestamp", "ingestionTime"]:
        df[i] = pd.to_datetime(df[i], unit="ms", errors="coerce").dt.tz_localize("UTC").dt.tz_convert("Asia/Tokyo")
    df.to_csv(out, index=False)
