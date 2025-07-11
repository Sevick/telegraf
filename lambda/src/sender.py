import json
import logging
import urllib.request
import urllib.parse
import os
import boto3

from parameter_store import ParameterStore

ssm_client = boto3.client('ssm')

logger = logging.getLogger()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logger.setLevel(LOGLEVEL)


# Telegram API base URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot"

class Sender:
    def __init__(self):
        self.TELEGRAMBOTTOKEN_PARAMETER_ARN = os.environ.get('TELEGRAMBOTTOKEN_PARAMETER_ARN')
        if not self.TELEGRAMBOTTOKEN_PARAMETER_ARN:
            logger.error("TELEGRAMBOTTOKEN_PARAMETER_ARN environment variable is not set")
            raise ValueError("TELEGRAMBOTTOKEN_PARAMETER_ARN environment variable is not set")

        self.TELEGRAMCHANNEL_PARAMETER_ARN = os.environ.get('TELEGRAMCHANNEL_PARAMETER_ARN')
        if not self.TELEGRAMCHANNEL_PARAMETER_ARN:
            logger.error("TELEGRAMCHANNEL_PARAMETER_ARN environment variable is not set")
            raise ValueError("TELEGRAMCHANNEL_PARAMETER_ARN environment variable is not set")

        self.paramter_store = ParameterStore()
        self.chat_id = self.paramter_store.retrieveParameterValue(self.TELEGRAMCHANNEL_PARAMETER_ARN)
        self.bot = self.paramter_store.retrieveParameterValue(self.TELEGRAMBOTTOKEN_PARAMETER_ARN)



    def send_payload(self, payload):
        datajson = json.dumps(payload).encode('utf-8')
        logger.debug(f"Sending payload: {datajson}")
        req = urllib.request.Request(
            f"{TELEGRAM_API_URL}{self.bot}/sendMessage",
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
        except Exception as e:
            logger.error(f"Failed to send payload: {response.status} - {str(e)}")
            raise


    def send_message(self, text):
        """Send a message to the specified chat ID."""
        logger.debug(f"Sending message to chat {self.chat_id}: {text}")
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': "MarkdownV2",
            'disable_web_page_preview': True
        }
        self.send_payload(payload)
