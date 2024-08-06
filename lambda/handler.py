import logging
from awstools.commands import main

logger = logging.getLogger()


def lambda_handler(event, context):
    args = event.get("args", [])
    main(args, standalone_mode=False)
