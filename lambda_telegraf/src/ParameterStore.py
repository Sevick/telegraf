import json
import os
import urllib.parse

import urllib3
from aws_lambda_powertools import Logger

logger = Logger(level=os.getenv("LOG_LEVEL", "INFO"))


class ParameterStore:
    def __init__(self):
        self.port = os.environ.get('PARAMETERS_SECRETS_EXTENSION_HTTP_PORT', 2773)
        self.aws_session_token = os.environ['AWS_SESSION_TOKEN']
        self.http = urllib3.PoolManager()
        logger.debug("ParameterStore initialized")

    def retrieve_extension_value(self, paramName):
        encoded_name = urllib.parse.quote(paramName, safe='')
        url = (f"http://localhost:{self.port}/systemsmanager/parameters/get/?name={encoded_name}&withDecryption=true")
        headers = {"X-Aws-Parameters-Secrets-Token": self.aws_session_token}
        response = self.http.request("GET", url, headers=headers)
        response = json.loads(response.data)
        config_values = response['Parameter']['Value']
        logger.debug(f"Parameter retrieved: {paramName}")
        return config_values

    def retrieveParameterValue(self, parameter_arn):
        try:
            config_values = self.retrieve_extension_value(parameter_arn)
            return config_values;
        except Exception as e:
            logger.exception(f"Failed to retrieve parameter value: {e}")
            raise
