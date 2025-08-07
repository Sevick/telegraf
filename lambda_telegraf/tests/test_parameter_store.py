import json
import os
import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import quote

from ParameterStore import ParameterStore


class TestParameterStore(unittest.TestCase):
    def setUp(self):
        # Set up common mocks and test data
        self.param_name = "/test/param"
        self.encoded_param_name = quote(self.param_name, safe='')
        self.aws_session_token = "test-session-token"
        self.port = "2773"
        self.metrics_namespace = "TelefrafTestSpace"
        self.mock_response_data = {
            'Parameter': {
                'Value': 'test-value'
            }
        }
        self.url = f"http://localhost:{self.port}/systemsmanager/parameters/get/?name={self.encoded_param_name}&withDecryption=true"

        # Patch environment variables
        self.patcher_os = patch.dict(os.environ, {
            'AWS_SESSION_TOKEN': self.aws_session_token,
            'PARAMETERS_SECRETS_EXTENSION_HTTP_PORT': self.port
        })
        self.patcher_os.start()

        # Patch urllib3.PoolManager
        self.patcher_urllib3 = patch('urllib3.PoolManager')
        self.mock_pool_manager = self.patcher_urllib3.start()
        self.mock_http = MagicMock()
        self.mock_pool_manager.return_value = self.mock_http

        # Patch logger
        self.patcher_logger = patch('ParameterStore.logger')
        self.mock_logger = self.patcher_logger.start()

    def tearDown(self):
        # Stop all patchers
        self.patcher_os.stop()
        self.patcher_urllib3.stop()
        self.patcher_logger.stop()

    def test_init(self):
        # Test initialization of ParameterStore
        param_store = ParameterStore()

        self.assertEqual(param_store.port, self.port)
        self.assertEqual(param_store.aws_session_token, self.aws_session_token)
        self.assertIsInstance(param_store.http, MagicMock)

    def test_retrieve_parameter_value_success(self):
        # Test successful parameter retrieval through retrieveParameterValue
        mock_response = MagicMock()
        mock_response.data = json.dumps(self.mock_response_data).encode('utf-8')
        self.mock_http.request.return_value = mock_response

        param_store = ParameterStore()
        result = param_store.retrieveParameterValue(self.param_name)

        self.mock_http.request.assert_called_once_with(
            "GET",
            self.url,
            headers={"X-Aws-Parameters-Secrets-Token": self.aws_session_token}
        )
        self.assertEqual(result, 'test-value')

    def test_retrieve_parameter_value_failure(self):
        # Test error handling in retrieveParameterValue
        mock_response = MagicMock()
        mock_response.data = b"invalid json"
        self.mock_http.request.return_value = mock_response

        param_store = ParameterStore()
        with self.assertRaises(json.JSONDecodeError):
            param_store.retrieveParameterValue(self.param_name)

        self.mock_logger.exception.assert_called_once()
        self.assertTrue(
            self.mock_logger.exception.call_args[0][0].startswith(
                "Failed to retrieve parameter value:"
            )
        )


if __name__ == '__main__':
    unittest.main()
