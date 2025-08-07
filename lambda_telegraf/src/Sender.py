import json
import os
import urllib.parse
import urllib.request

from aws_lambda_powertools import Metrics, Logger
from aws_lambda_powertools.metrics import MetricUnit

from ParameterStore import ParameterStore

logger = Logger(level=os.getenv("LOG_LEVEL", "INFO"))

TELEGRAM_API_URL = f"https://api.telegram.org/bot"


class Sender:
    def __init__(self):
        self.TELEGRAMBOTTOKEN_PARAMETER_NAME = os.environ.get('TELEGRAMBOTTOKEN_PARAMETER_NAME')
        if not self.TELEGRAMBOTTOKEN_PARAMETER_NAME:
            logger.error("TELEGRAMBOTTOKEN_PARAMETER_NAME environment variable is not set")
            raise ValueError("TELEGRAMBOTTOKEN_PARAMETER_NAME environment variable is not set")
        self.TELEGRAMCHANNEL_PARAMETER_NAME = os.environ.get('TELEGRAMCHANNEL_PARAMETER_NAME')
        if not self.TELEGRAMCHANNEL_PARAMETER_NAME:
            logger.error("TELEGRAMCHANNEL_PARAMETER_NAME environment variable is not set")
            raise ValueError("TELEGRAMCHANNEL_PARAMETER_NAME environment variable is not set")

        self.paramter_store = ParameterStore()
        self.metrics = Metrics()
        logger.debug("Sender initialized")

    def send_payload(self, payload):
        bot = self.paramter_store.retrieveParameterValue(self.TELEGRAMBOTTOKEN_PARAMETER_NAME)
        datajson = json.dumps(payload).encode('utf-8')
        logger.debug(f"Sending payload: {datajson}")
        req = urllib.request.Request(
            f"{TELEGRAM_API_URL}{bot}/sendMessage",
            data=datajson,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        try:
            with urllib.request.urlopen(req) as response:
                logger.debug(f"Telegram API response: {response.read().decode('utf-8')}")
                # if response.status == 429:
                #     buffer_message(bot, payload)
                if response.status != 200:
                    logger.error(f"Telegram API error: {response.status} {response.body}")
                    raise Exception(f"Telegram API error: {response.status} {response.body}")
                self.metrics.add_metric(name="telegram_messages_send_success_counter", unit=MetricUnit.Count,
                                        value=1)
        except Exception as e:
            self.metrics.add_metric(name="telegram_messages_send_failure_counter", unit=MetricUnit.Count,
                                    value=1)
            logger.exception(f"Failed to send payload: {req}")
            raise

    def send_message(self, text):
        chat_id = self.paramter_store.retrieveParameterValue(self.TELEGRAMCHANNEL_PARAMETER_NAME)
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': "MarkdownV2",
            'disable_web_page_preview': True
        }
        self.send_payload(payload)
