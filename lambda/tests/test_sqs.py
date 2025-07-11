import unittest
import json
from unittest.mock import patch
from telegraf_sqs_consumer import sqs_handler


class TestSqsConsumer(unittest.TestCase):
    @patch('telegraf_sqs_consumer.sqs_handler')
    def test_lambda_handler_batch_success(self, mock_sqs_client):
        # Mock SQS client delete_message_batch
        mock_sqs_client.delete_message_batch.return_value = {
            'Successful': [{'Id': '0'}, {'Id': '1'}],
            'Failed': []
        }

        # Load test event
        with open('tests/events/sqs_event.json') as f:
            event = json.load(f)

        # Call Lambda handler
        response = sqs_handler(event, None)

        # Assertions
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Successfully processed 2 messages', response['body'])
        mock_sqs_client.delete_message_batch.assert_called_once()


if __name__ == '__main__':
    unittest.main()