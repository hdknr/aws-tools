import boto3

from logging import getLogger
from datetime import datetime, timezone

logger = getLogger()


def get_client():
    client = boto3.client("logs")
    return client


def _fetch_stream_events_recursive(
    client,
    log_group_name,
    log_stream_name,
    start_time_ms,
    end_time_ms,
    next_token=None,
    accumulated_events=None,
):
    """
    get_log_events API を再帰的に呼び出し、すべてのログイベントを取得するヘルパー関数。
    """
    if accumulated_events is None:
        accumulated_events = []

    params = {
        "logGroupName": log_group_name,
        "logStreamName": log_stream_name,
        "startTime": start_time_ms,
        "endTime": end_time_ms,
        "limit": 10000,  # 1回の呼び出しで取得する最大イベント数
        "startFromHead": True,  # 古いイベントから取得することで、nextTokenで順方向へ進む
    }
    if next_token:
        params["nextToken"] = next_token

    response = client.get_log_events(**params)

    accumulated_events.extend(response["events"])

    # nextForwardToken を使用して次のページをチェック
    # nextForwardToken が存在し、かつ前回の next_token と異なる場合のみ再帰呼び出し
    if "nextForwardToken" in response and response["nextForwardToken"] != next_token:
        return _fetch_stream_events_recursive(
            client,
            log_group_name,
            log_stream_name,
            start_time_ms,
            end_time_ms,
            response["nextForwardToken"],
            accumulated_events,
        )
    else:
        return accumulated_events


def fech_stream_events(log_group_name, log_stream_name, start_time_ms=None, end_time_ms=None):
    """
    指定されたCloudWatch Logsのログストリームからログイベントをダウンロードします。
    再帰的に全てのページを処理します。
    """
    client = get_client()

    # デフォルトの時間範囲を設定（過去24時間）
    if end_time_ms is None:
        end_time_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    if start_time_ms is None:
        start_time_ms = end_time_ms - (24 * 60 * 60 * 1000)  # 24時間前

    try:
        # 再帰ヘルパー関数を呼び出してすべてのイベントを取得
        all_events = _fetch_stream_events_recursive(client, log_group_name, log_stream_name, start_time_ms, end_time_ms)
        return all_events
    except client.exceptions.ResourceNotFoundException:
        return []
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return []
