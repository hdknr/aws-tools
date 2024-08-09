import logging
import boto3


logger = logging.getLogger()


def get_client():
    client = boto3.client("ecs")
    return client


def update_desired_count(cluster, service, desired_count, client=None):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/update_service.html

    client = client or get_client()

    params = dict(
        cluster=cluster,
        service=service,
        desiredCount=int(desired_count),
    )
    try:
        response = client.update_service(**params)
        message = "ECSタスク数更新:" + str(params)
        logger.info(f"update_desired_count: {message}")
    except Exception as e:
        logger.error(f"update_desired_count: {e}")
        pass

    return response
