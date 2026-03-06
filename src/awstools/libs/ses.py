import logging
import boto3
from botocore.exceptions import ClientError
import os


logger = logging.getLogger()


def get_all_suppressed_destinations(region_name=None):
    """
    SESv2のアカウントレベルのサプレッションリストから全ての宛先を取得します。

    Args:
        region_name (str): SESを使用しているAWSリージョン名。

    Returns:
        list: サプレッションリストに登録されているメールアドレスのリスト。 エラーが発生した場合は空のリスト。
    """
    region_name = region_name or os.environ.get("AWS_REGION", "ap-northeast-1")

    # SESv2クライアントの初期化
    # SESV2はリージョンに依存します
    try:
        client = boto3.client("sesv2", region_name=region_name)
    except Exception as e:
        print(f"Boto3クライアントの初期化に失敗しました: {e}")
        return []

    suppressed_emails = []
    next_token = None

    # NextTokenを使ってページングしながら全てのリストを取得
    logger.info("サプレッションリストの取得を開始します...")
    while True:
        try:
            # list_suppressed_destinationsの呼び出し
            if next_token:
                response = client.list_suppressed_destinations(
                    NextToken=next_token,
                    PageSize=1000,  # 最大値 (デフォルトも1000)
                )
            else:
                response = client.list_suppressed_destinations(PageSize=1000)

            # 結果からメールアドレスを抽出
            summaries = response.get("SuppressedDestinationSummaries", [])
            for summary in summaries:
                email = summary.get("EmailAddress")
                reason = summary.get("Reason")
                last_update = summary.get("LastUpdateTime")

                # 必要に応じて、詳細情報も保存
                suppressed_emails.append(
                    {
                        "EmailAddress": email,
                        "Reason": reason,
                        "LastUpdateTime": last_update,
                    }
                )

            logger.info(f"  - 現在までに {len(suppressed_emails)} 件の宛先を取得しました。")

            # 次のページがあるか確認
            next_token = response.get("NextToken")
            if not next_token:
                # NextTokenがない場合は終了
                break

        except ClientError as e:
            logger.error(f"SES API呼び出し中にエラーが発生しました: {e}")
            break
        except Exception as e:
            logger.error(f"予期せぬエラーが発生しました: {e}")
            break

    logger.info(f"リストの取得が完了しました。合計 {len(suppressed_emails)} 件。")
    return suppressed_emails


def get_suppressed_destination_details(email_address, region_name=None):
    """
    特定のメールアドレスがサプレッションリストに存在するか、およびその詳細を取得します。

    Args:
        email_address (str): 検索したいメールアドレス。
        region_name (str): SESを使用しているAWSリージョン名。

    Returns:
        dict: 登録情報（存在する場合）。存在しない場合はNone。
    """
    region_name = region_name or os.environ.get("AWS_REGION", "ap-northeast-1")

    try:
        client = boto3.client("sesv2", region_name=region_name)
        response = client.get_suppressed_destination(EmailAddress=email_address)
        return response.get("SuppressedDestination")
    except ClientError as e:
        # NotFoundException はリストに存在しないことを意味します
        if e.response["Error"]["Code"] == "NotFoundException":
            logger.error(f"メールアドレス '{email_address}' はサプレッションリストに存在しません。")
            return None
        else:
            logger.error(f"SES API呼び出し中にエラーが発生しました: {e}")
            return None
    except Exception as e:
        logger.error(f"予期せぬエラーが発生しました: {e}")
        return None


def delete_email_from_suppression_list(email_address: str, region_name: str = None) -> bool:
    """
    SESv2のアカウントレベルのサプレッションリストから指定されたメールアドレスを削除します。

    Args:
        email_address (str): 削除したいメールアドレス。
        region_name (str): SESを使用しているAWSリージョン名。

    Returns:
        bool: 削除が成功したか（または既に存在しなかったか）どうか。
    """
    try:
        region_name = region_name or os.environ.get("AWS_REGION", "ap-northeast-1")
        # SESv2クライアントの初期化
        client = boto3.client("sesv2", region_name=region_name)

        logger.info(f"'{email_address}' のサプレッションリストからの削除を試みます...")

        # delete_suppressed_destinationの呼び出し
        response = client.delete_suppressed_destination(EmailAddress=email_address)

        # 成功すると、レスポンスボディは空（HTTP 200）ですが、
        # Boto3のレスポンスにはメタデータが含まれます。
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info(
                f"✅ 削除リクエストが正常に受け付けられました。メールアドレス '{email_address}' はリストから削除されました。"
            )
            return True
        else:
            # 200以外の場合はエラーとして扱う
            logger.info(
                f"⚠️ 削除リクエストは正常に処理されませんでしたが、APIエラーはありませんでした: {response['ResponseMetadata']['HTTPStatusCode']}"
            )
            return False

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        # NotFoundException: 削除対象のアドレスが既にリストにない場合
        if error_code == "NotFoundException":
            logger.error(
                f"🔔 メールアドレス '{email_address}' はサプレッションリストに存在しませんでした。削除は不要です。"
            )
            return True
        else:
            # その他のAPIエラー（権限不足、不正な形式など）
            logger.error(f"❌ SES API呼び出し中にエラーが発生しました ({error_code}): {e}")
            return False
    except Exception as e:
        logger.error(f"❌ 予期せぬエラーが発生しました: {e}")
        return False
