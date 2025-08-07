import os
from aws_lambda_powertools import Logger

from Sender import Sender
from formater import format_telegram_message

logger = Logger(level=os.getenv("LOG_LEVEL", "INFO"))


class Processor:
    def __init__(self):
        self.sender = Sender()
        logger.debug("Processor initialized")

    def process_message(self, subject, message):
        logger.info(f"Processing message with subject: {subject}")
        formatted_message = format_telegram_message(subject, message)
        self.sender.send_message(formatted_message)
