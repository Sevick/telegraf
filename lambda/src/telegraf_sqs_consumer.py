import json
import logging
import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SQS client
sqs_client = boto3.client('sqs')


def lambda_handler(event, context):
    """
    AWS Lambda function to consume and process SQS messages.

    Args:
        event: SQS event containing messages
        context: Lambda execution context

    Returns:
        dict: Response indicating success or failure
    """
    try:
        # Process each message in the event
        for record in event['Records']:
            # Extract message body and receipt handle
            message_body = record['body']
            receipt_handle = record['receiptHandle']

            # Log message
            logger.debug(f"Received message: {message_body}")

            # Parse message body (assuming JSON)
            try:
                message_data = json.loads(message_body)

                process_message(message_data)

                # Delete message from queue after successful processing
                logger.info(f"Deletingd message with receipt handle: {receipt_handle}")
                queue_url = record['eventSourceARN'].split(':')[-1]
                sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )

                logger.info(f"Processed message data: {message_data}")

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse message body: {e}")
                # Skip deletion to allow message to be retried
                continue
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                # Skip deletion to allow message to be retried
                continue

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully processed messages')
        }

    except Exception as e:
        logger.error(f"Lambda execution failed: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }


def process_message(message_data):
    """
    Placeholder function to process message data.
    Replace with your business logic.

    Args:
        message_data: Parsed message content
    """
    # Example: Log the message content
    logger.info(f"Processing message: {message_data}")
    # Add your processing logic here