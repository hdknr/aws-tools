import boto3

from logging import getLogger

logger = getLogger()


def get_client():
    client = boto3.client("cloudfront")
    return client


def get_dist(deploy, client=None):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_distributions.html
    client = client or get_client()
    res = client.list_distributions()
    items = res["DistributionList"]["Items"]
    item = next(filter(lambda i: i["Comment"] and i["Comment"].find(deploy) >= 0, items), None)
    return item


def get_dist_config(dist_id, client=None, dist=None):
    client = client or get_client()
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_distribution_config.html
    conf = client.get_distribution_config(Id=dist_id)
    return conf


def update_origin(dist_id, new_origin_id, *path_pats, client=None):
    client = client or get_client()
    conf = get_dist_config(dist_id, client=client)
    if not conf:
        return

    IfMatch = conf["ETag"]
    DistributionConfig = conf["DistributionConfig"]

    # 変更
    for item in DistributionConfig["CacheBehaviors"]["Items"]:
        if item["PathPattern"] in path_pats:
            item["TargetOriginId"] = new_origin_id

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_distribution.html
    res = client.update_distribution(
        DistributionConfig=DistributionConfig,
        Id=dist_id,
        IfMatch=IfMatch,
    )
    return res
