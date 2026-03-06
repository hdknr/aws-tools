import boto3

from logging import getLogger
from datetime import datetime, timezone

logger = getLogger()


def get_client():
    client = boto3.client("logs")
    return client


def _fetch_all_events(client, log_group_name, log_stream_name, start_time_ms, end_time_ms):
    """get_log_events API をページネーションで呼び出し、すべてのログイベントを取得する。"""
    all_events = []
    next_token = None

    while True:
        params = {
            "logGroupName": log_group_name,
            "logStreamName": log_stream_name,
            "startTime": start_time_ms,
            "endTime": end_time_ms,
            "limit": 10000,
            "startFromHead": True,
        }
        if next_token:
            params["nextToken"] = next_token

        response = client.get_log_events(**params)
        all_events.extend(response["events"])

        new_token = response.get("nextForwardToken")
        if not new_token or new_token == next_token:
            break
        next_token = new_token

    return all_events


def fetch_stream_events(log_group_name, log_stream_name, start_time_ms=None, end_time_ms=None):
    """指定されたCloudWatch Logsのログストリームからログイベントをダウンロードします。"""
    client = get_client()

    if end_time_ms is None:
        end_time_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    if start_time_ms is None:
        start_time_ms = end_time_ms - (24 * 60 * 60 * 1000)

    try:
        return _fetch_all_events(client, log_group_name, log_stream_name, start_time_ms, end_time_ms)
    except client.exceptions.ResourceNotFoundException:
        return []
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        return []
