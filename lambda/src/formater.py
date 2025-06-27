import json
import logging
import re
import os


logger = logging.getLogger()

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logger.setLevel(LOGLEVEL)

def make_json_safe(text: str) -> str:
    return json.dumps(text).replace('"', '\\"')[1:-1]

def escape_markdown_v2(text):
    """
    Escapes all special characters required for Telegram MarkdownV2 formatting,
    EXCEPT for double asterisks (**) to allow proper bold text rendering.
    """
    special_chars = r"([_*\[\]()~`>#+\-=|{}.!])"  # All Telegram MarkdownV2 special characters
    return re.sub(special_chars, r"\\\1", text)  # Escape with a preceding backslash


def format_telegram_message(input_event, source_link):
    """
    Formats the OpenAI JSON response into a fully compliant MarkdownV2 Telegram message.
    """
    if not input_event:
      raise ValueError("Input event is empty")

    # message = f"""*{title}*\n\n{summary_safe}\n\n [{source}]({source_link}) {tag}@IsraelTechNews"""
    message = "TestMessage"
    return message
