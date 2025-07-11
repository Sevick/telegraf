import unittest
from unittest.mock import patch, MagicMock
from processor import Processor


class TestProcessor(unittest.TestCase):
    @patch('processor.format_telegram_message')  # Mock the formatter
    @patch('processor.Sender')  # Mock the Sender class
    def test_process_message_sends_formatted_message(self, mock_sender_class, mock_formatter):
        # Prepare
        mock_sender_instance = MagicMock()
        mock_sender_class.return_value = mock_sender_instance
        mock_formatter.return_value = "formatted message"
        processor = Processor()
        subject = "Test Subject"
        message = "Test Message"

        # Act
        result = processor.process_message(subject, message)

        # Assert
        mock_formatter.assert_called_once_with(subject, message)
        mock_sender_instance.send_message.assert_called_once_with("formatted message")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
