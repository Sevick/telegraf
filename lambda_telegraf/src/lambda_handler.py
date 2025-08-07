import os

from aws_lambda_powertools import Logger
from SnsHandler import SnsHandler

_sns_handler = SnsHandler()

logger = Logger(level=os.getenv("LOG_LEVEL", "INFO"))


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    return _sns_handler.sns_handler(event, context)
