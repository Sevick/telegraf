import json
import logging
import boto3
import os

logger = logging.getLogger()

def delete_secure_parameter(event, context):
    logger.info(f"create_secure_parameter invoked")
    paramName = event.get("parameterName")
    boto3.client('ssm').delete_parameter(
        Name=paramName
    )
    logger.info(f"Deleted parameter: {paramName}")
    return {
        'statusCode': 200,
        'body': json.dumps('Parameter created')
    }