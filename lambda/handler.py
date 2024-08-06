import logging
from awstools.commands import main

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    args = event.get("args", [])
    logger.info(str(args))
    main(args, standalone_mode=False)
