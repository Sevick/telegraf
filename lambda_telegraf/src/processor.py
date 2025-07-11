import logging
import os

logger = logging.getLogger()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logger.setLevel(LOGLEVEL)

from sender import Sender
from formater import format_telegram_message

class Processor:
    def __init__(self):
        self.sender = Sender()

    def process_message(self, subject, message):
        logger.info(f"Processing message with subject: {subject}")
        formatted_message = format_telegram_message(subject, message)
        self.sender.send_message(formatted_message)
        return True