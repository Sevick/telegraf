import os

from aws_lambda_powertools import Logger
from Processor import Processor

logger = Logger(level=os.getenv("LOG_LEVEL", "INFO"))

class SnsHandler:
    def __init__(self):
        self.processor = Processor()


    def sns_handler(self, event, context):
        records = event.get("Records", [])
        if not records:
            logger.info("No Records in event — nothing to process.")
            return
        logger.info(f"Received {len(records)} record(s)")
        try:
            # Process each message in the event
            for record in records:
                if record.get("EventSource") != "aws:sns":
                    logger.debug(f"Skipping non-SNS record")
                    continue
                try:
                    logger.debug(f"Received SNS message: {record}")
                    sns = record.get("Sns", {})
                    message_id = sns.get("MessageId", "N/A")
                    subject = sns.get("Subject", "N/A")
                    message_raw = sns.get("Message")
                    logger.debug(f"Message ID: {message_id}, Subject: {subject}, Raw Message: {message_raw}")
                    self.processor.process_message(subject, message_raw)
                except Exception as e:
                    logger.exception(f"Error processing message: {e}")
                    # Skip deletion to allow message to be retried
                    continue
            return

        except Exception as e:
            logger.exception(f"Lambda execution failed: {e}")
            return
