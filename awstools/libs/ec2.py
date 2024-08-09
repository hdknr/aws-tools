import boto3
from itertools import chain

from logging import getLogger

logger = getLogger()


def stop(instance_id, obj=None, force=False):
    """
    stop:
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/stop.html
    """
    resource = boto3.resource("ec2")
    instance = obj or resource.Instance(instance_id)
    instance.stop(Force=force)


def start(instance_id, obj=None):
    """
    start:
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/start.html
    """
    resource = boto3.resource("ec2")
    instance = obj or resource.Instance(instance_id)
    instance.start()


def force_restart_instance_status(instance_id):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_status.html
    """
    client = boto3.client("ec2")
    response = client.describe_instance_status(
        InstanceIds=[instance_id],
    )
    status = response["InstanceStatuses"]
    if len(status) != 1:
        return False

    instance_status = status[0]["InstanceStatus"]
    if instance_status["Status"] != "ok":
        logger.error("force_restart_instance_status: " + str(instance_status))
        resource = boto3.resource("ec2")
        instance = resource.Instance(instance_id)
        instance.stop(force=True)
        instance.wait_until_stopped()
        instance.start()


def restart(instance_id, obj=None, force=False, dry_run=False):
    """
    state:
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/state.html
    """
    logger.info(f"restaring {instance_id}")

    resource = boto3.resource("ec2")
    instance = obj or resource.Instance(instance_id)

    state = instance.state

    if not force:
        if state["Code"] == 16:  # running
            message = f"{instance_id} is running: do nothing"
            logger.info(message)
            if force_restart_instance_status(instance_id):
                message = f"{instance_id} was forced to restart"
            return dict(id=instance_id, state=state["Code"], message=message)

        if state["Code"] == 48:  # terminated
            # AMIから起動
            message = f"{instance_id} is terminated: you must create instance from AMI)"
            logger.info(message)
            return dict(id=instance_id, state=state["Code"], message=message)

    message = ""
    if not state["Code"] == 80:  # stopped
        message = f"{instance_id} is not stop: stop this before starting..."
        logger.info(message)
        if not dry_run:
            stop(instance_id, obj=obj, force=force)
            instance.wait_until_stopped()

    message += f"{instance_id} stopped: start this"
    if not dry_run:
        logger.info(message)
        start(instance_id, obj=instance)
        return dict(id=instance_id, state=state["Code"], message=message)

    return dict(id=instance_id, state=state["Code"], message="skipped")


def filter_from_tags(tags):
    tagtuples = map(lambda i: i.split("="), tags)
    return list(map(lambda i: {"Name": f"tag:{i[0]}", "Values": [i[1]]}, tagtuples))


def get_instances_tags(tags):
    client = boto3.client("ec2")
    res = client.describe_instances(Filters=filter_from_tags(tags))
    return res


def restart_instances_all(instances, force=False, dry_run=False):
    """再起動"""
    instances = chain.from_iterable(
        map(lambda i: i["Instances"], instances["Reservations"])
    )
    return list(
        map(lambda i: restart(i["InstanceId"], force=force, dry_run=dry_run), instances)
    )
