import json
import re
import os

from aws_lambda_powertools import Logger

logger = Logger(level=os.getenv("LOG_LEVEL", "INFO"))


def make_json_safe(text: str) -> str:
    return json.dumps(text).replace('"', '\\"')[1:-1]


def escape_markdown_v2(text):
    """
    Escapes all special characters required for Telegram MarkdownV2 formatting,
    EXCEPT for double asterisks (**) to allow proper bold text rendering.
    """
    special_chars = r"([_*\[\]()~`>#+\-=|{}.!])"  # All Telegram MarkdownV2 special characters
    return re.sub(special_chars, r"\\\1", text)  # Escape with a preceding backslash


def format_telegram_message(subject, message):
    subject = escape_markdown_v2(subject)
    message = escape_markdown_v2(message)
    messageText = f"""*{subject}*\n{message}"""
    return messageText
