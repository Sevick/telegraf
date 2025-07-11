import unittest
from unittest.mock import patch, MagicMock
from telegraf_sns_consumer import SnsHandler

class TestTelegrafSnsConsumer(unittest.TestCase):

    @patch('telegraf_sns_consumer.Processor')
    def test_sns_handler_processes_message(self, MockProcessor):
        # Prepare
        mock_processor_instance = MagicMock()
        MockProcessor.return_value = mock_processor_instance
        event = {
            "Records": [{
                "EventSource": "aws:sns",
                "Sns": {
                    "MessageId": "test-id",
                    "Subject": "test-subject",
                    "Message": "test-message"
                }
            }]
        }
        sns_handler = SnsHandler()

        # Act
        sns_handler.sns_handler(event, {})

        # Assert
        mock_processor_instance.process_message.assert_called_once_with("test-subject", "test-message")


    @patch('telegraf_sns_consumer.Processor')
    def test_sns_handler_no_records(self, mock_processor):
        # Prepare
        mock_instance = MagicMock()
        mock_processor.return_value = mock_instance
        event = {"Records": []}
        sns_handler = SnsHandler()

        # Act
        sns_handler.sns_handler(event, {})

        # Assert
        mock_instance.process_message.assert_not_called()


if __name__ == '__main__':
    unittest.main()