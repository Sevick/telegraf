import unittest
from unittest.mock import patch, MagicMock
from SnsHandler import SnsHandler

class TestTelegrafSnsConsumer(unittest.TestCase):

    @patch('SnsHandler.Processor')
    def test_sns_handler_processes_message(self, mock_processor_class):

        # Mock Processor class
        mock_processor_instance = MagicMock()
        mock_processor_class.return_value = mock_processor_instance

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


    @patch('SnsHandler.Processor')
    def test_sns_handler_no_records(self, mock_processor_class):
        # Mock Processor class
        mock_processor_instance = MagicMock()
        mock_processor_class.return_value = ""

        event = {"Records": []}
        sns_handler = SnsHandler()

        # Act
        sns_handler.sns_handler(event, {})

        # Assert
        mock_processor_instance.process_message.assert_not_called()


if __name__ == '__main__':
    unittest.main()