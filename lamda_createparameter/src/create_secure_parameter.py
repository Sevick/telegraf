import json
import logging
import boto3
import os

logger = logging.getLogger()

def create_secure_parameter(event, context):
    logger.info(f"create_secure_parameter invoked")
    paramName = event.get("parameterName")
    parameterValue = event.get("parameterValue")
    parameterDescr = event.get("parameterDescr")

    
    boto3.client('ssm').put_parameter(
        Name=paramName,
        Value=parameterValue,
        Description=parameterDescr,
        Type='SecureString'
    )

    logger.info(f"cteated parameter: {paramName}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Parameter created')
    }