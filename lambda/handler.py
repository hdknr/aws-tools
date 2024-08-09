import logging
from awstools.commands import main
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    for key in [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION",
        "AWS_DEFAULT_REGION",
    ]:
        conf_key = f"CONF_{key}"
        if conf_key in os.environ:
            os.environ[key] = os.environ[conf_key]

    args = event.get("args", [])
    logger.info(str(args))
    main(args, standalone_mode=False)
