import logging
import boto3


logger = logging.getLogger()


def create_client(region_name=None):
    return boto3.client("rds")


def start(instance_id, client=None):
    # Start
    # https://boto3.amazonaws.com/v1/documentation/api/1.26.86/reference/services/rds/client/start_db_cluster.html
    client = client or create_client()
    client.start_db_instance(DBInstanceIdentifier=instance_id)


def stop(instance_id, client=None):
    # Stop
    # https://boto3.amazonaws.com/v1/documentation/api/1.26.86/reference/services/rds/client/stop_db_cluster.html

    client = client or create_client()
    client.stop_db_instance(DBInstanceIdentifier=instance_id)


def start_cluster(cluster_id, client=None):
    # Start
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/start_db_instance.html
    client = client or create_client()
    client.start_db_cluster(DBClusterIdentifier=cluster_id)


def stop_cluster(cluster_id, client=None):
    # https://boto3.amazonaws.com/v1/documentation/api/1.26.86/reference/services/rds/client/stop_db_instance.html

    client = client or create_client()
    client.stop_db_cluster(DBClusterIdentifier=cluster_id)
