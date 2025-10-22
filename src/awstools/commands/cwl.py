"""
cloudwatch logs
"""

import click
import pandas as pd
import os

from logging import getLogger
from ..libs import cwl as cwl_lib
from datetime import datetime
from pathlib import Path
from functools import reduce
import operator

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
@click.option("--stream_count", "-c", default=50)
@click.option("--today", "-t", is_flag=True)
@click.option("--fetch", "-f", is_flag=True)
@click.option("--out", "-o", default=None)
@click.pass_context
def list_streams(ctx, log_group_name, stream_count, today, fetch, out):
    """ストリーム一覧"""
    client = cwl_lib.get_client()

    next_token = None
    log_stream_name_prefix = None
    limit = stream_count
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
    if today:
        df = df[df["lastEventTimestamp"].dt.date == datetime.now().date()]

    df = df[["logStreamName", "lastEventTimestamp"]]

    def _do_fetch(row):
        name = row["logStreamName"].split("/")[-1]
        path = Path(out or "/tmp") / f"{name}.csv"
        fetch_stream(log_group_name, row["logStreamName"], str(path))
        row["path"] = path
        return row

    if fetch:
        df = df.apply(_do_fetch, axis=1)

    print(df.to_csv(index=False))


def fetch_stream(log_group_name, log_stream_name, out):
    events = cwl_lib.fech_stream_events(log_group_name, log_stream_name)
    df = pd.DataFrame(events)
    for i in ["timestamp", "ingestionTime"]:
        df[i] = (
            pd.to_datetime(df[i], unit="ms", errors="coerce")
            .dt.tz_localize("UTC")
            .dt.tz_convert("Asia/Tokyo")
        )
    df.to_csv(out, index=False)


@cwl.command()
@click.argument("log_group_name")
@click.argument("log_stream_name")
@click.option("--out", "-o", default=None)
@click.pass_context
def fetch_streams(ctx, log_group_name, log_stream_name, out):
    """ストリームダウンロード"""
    out = out or "/tmp/event.csv"
    fetch_stream(log_group_name, log_stream_name, out)


@cwl.command()
@click.argument("csv_file")
@click.option("--exclude_file", "-x", default=None)
@click.pass_context
def report_error(ctx, csv_file, exclude_file):
    """エラーレポート"""
    exclude_file = exclude_file or os.environ.get("CWL_EXCLUDES", "")
    if not exclude_file:
        print("no excludes specified")
        return

    with open(exclude_file, "r") as err:
        excludes = [i.rstrip() for i in err.readlines()]

    if not excludes:
        print("no excludes")
        return

    df = pd.read_csv(csv_file)

    conditions = [
        ~df["message"].str.contains(keyword, na=False) for keyword in excludes
    ]

    filtered_df = df[reduce(operator.and_, conditions)]
    if filtered_df.shape[0] < 1:
        print("no errors")
        return

    filtered_df.to_csv(f"{csv_file}.report.csv", index=False)
