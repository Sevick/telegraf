import unittest
from unittest.mock import patch, MagicMock
from parameter_store import ParameterStore


class TestParameterStore(unittest.TestCase):

    @patch('parameter_store.boto3.client')
    def test_retrieve_parameter_value_success(self, mock_boto_client):
        # Prepare
        mock_ssm = MagicMock()
        mock_boto_client.return_value = mock_ssm
        mock_ssm.get_parameter.return_value = {
            'Parameter': {'Value': 'mocked-secret-value'}
        }

        parameter_store = ParameterStore()

        # Act
        result = parameter_store.retrieveParameterValue('mock-arn')

        # Assert
        self.assertEqual(result, 'mocked-secret-value')
        mock_ssm.get_parameter.assert_called_once_with(
            Name='mock-arn',
            WithDecryption=True
        )

    @patch('parameter_store.boto3.client')
    def test_retrieve_parameter_value_failure(self, mock_boto_client):
        # Prepare
        mock_ssm = MagicMock()
        mock_boto_client.return_value = mock_ssm
        mock_ssm.get_parameter.side_effect = Exception('SSM failure')

        parameter_store = ParameterStore()

        # Act & Assert
        with self.assertRaises(Exception) as context:
            parameter_store.retrieveParameterValue('mock-arn')

        self.assertIn('SSM failure', str(context.exception))
        mock_ssm.get_parameter.assert_called_once()


if __name__ == '__main__':
    unittest.main()
