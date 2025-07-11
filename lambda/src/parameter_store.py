import logging
import os
import boto3

logger = logging.getLogger()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logger.setLevel(LOGLEVEL)

class ParameterStore:
    def __init__(self):
        self.ssm_client = boto3.client('ssm')

    def retrieveParameterValue(self, parameter_arn):
        try:
            response = self.ssm_client.get_parameter(
                Name=parameter_arn,
                WithDecryption=True
            )
            return response['Parameter']['Value']
        except Exception as e:
            logger.error(f"Failed to retrieve parameter value: {e}")
            raise