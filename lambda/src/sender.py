import json
import logging
import urllib.request
import urllib.parse
import os

logger = logging.getLogger()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logger.setLevel(LOGLEVEL)


# Telegram API base URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot"


TELEGRAMBOTTOKEN_PARAMETER_ARN = os.environ.get('TELEGRAMBOTTOKEN_PARAMETER_ARN')
if not TELEGRAMBOTTOKEN_PARAMETER_ARN:
    logger.error("TELEGRAMBOTTOKEN_PARAMETER_ARN environment variable is not set")
    raise ValueError("TELEGRAMBOTTOKEN_PARAMETER_ARN environment variable is not set")

TELEGRAMCHANNEL_PARAMETER_ARN = os.environ.get('TELEGRAMCHANNEL_PARAMETER_ARN')
if not TELEGRAMCHANNEL_PARAMETER_ARN:
    logger.error("TELEGRAMCHANNEL_PARAMETER_ARN environment variable is not set")
    raise ValueError("TELEGRAMCHANNEL_PARAMETER_ARN environment variable is not set")


def send_payload(bot, chat_id, payload):
    datajson = json.dumps(payload).encode('utf-8')
    logger.debug(f"Sending payload to chat {chat_id}: {datajson}")
    req = urllib.request.Request(
        f"{TELEGRAM_API_URL}{bot}/sendMessage",
        data=datajson,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as response:
            logger.info(f"Telegram API response: {response.read().decode('utf-8')}")
            if response.status != 200:
                logger.error(f"Telegram API error: {response.status} {response.body}")
                raise Exception(f"Telegram API error: {response.status} {response.body}")
    except urllib.error.URLError as e:
        raise Exception(f"Failed to send payload: {str(e)}")


def send_message(bot, chat_id, text):
    """Send a message to the specified chat ID."""
    logger.debug(f"Sending message to chat {chat_id}: {text}")    
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': "MarkdownV2",
        'disable_web_page_preview': True
    }
    send_payload(bot, chat_id, payload)
