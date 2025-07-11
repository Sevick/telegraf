import logging
import os

from processor import Processor

logger = logging.getLogger()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logger.setLevel(LOGLEVEL)

class SnsHandler:
    def __init__(self):
        self._processor = Processor()


    def sns_handler(self, event, context):
        records = event.get("Records", [])
        if not records:
            logger.debug("No Records in event — nothing to process.")
            return

        logger.debug(f"Received {len(records)} record(s)")
        try:
            # Process each message in the event
            for record in records:
                if record.get("EventSource") != "aws:sns":
                    logger.debug(f"Skipping non-SNS record")
                    continue

                subject = ""
                message_raw = ""
                try:
                    sns = record.get("Sns", {})
                    message_id = sns.get("MessageId", "N/A")
                    subject = sns.get("Subject", "N/A")
                    message_raw = sns.get("Message")

                    logger.info(f"Message ID: {message_id}")
                    logger.info(f"Subject: {subject}")
                    logger.info(f"Raw Message: {message_raw}")
                    # Log message

                    logger.debug(f"Received message: {record}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    # Skip deletion to allow message to be retried
                    continue

                self._processor.process_message(subject, message_raw)
            return

        except Exception as e:
            logger.error(f"Lambda execution failed: {e}")
            return
