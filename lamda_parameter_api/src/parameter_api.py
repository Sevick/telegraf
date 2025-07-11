import json
import logging
import boto3
import urllib3

logger = logging.getLogger()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logger.setLevel(LOGLEVEL)

http = urllib3.PoolManager()
ssm_client = boto3.client('ssm')

def send_response(event, context, status, reason=None):
    response_body = {
        "Status": status,
        "Reason": reason or f"See CloudWatch log stream: {context.log_stream_name}",
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"],
        "Data": {}
    }

    encoded_body = json.dumps(response_body).encode('utf-8')
    headers = {'content-type': '', 'content-length': str(len(encoded_body))}

    try:
        response = http.request("PUT", event["ResponseURL"], body=encoded_body, headers=headers)
        print(f"Sent response to CloudFormation: {response.status}")
    except Exception as e:
        print(f"Failed to send response: {e}")


def create_secure_parameter(event, context):
    logger.info(f"Create_secure_parameter invoked")
    paramName = event.get("parameterName")
    parameterValue = event.get("parameterValue")
    parameterDescr = event.get("parameterDescr")

    
    ssm_client.put_parameter(
        Name=paramName,
        Value=parameterValue,
        Description=parameterDescr,
        Type='SecureString'
    )

    logger.info(f"Created parameter: {paramName}")
    return {
        'statusCode': 200,
        'body': json.dumps(f"Created parameter: {paramName}")
    }


def delete_secure_parameter(event, context):
    if event.get("RequestType") != "Delete":
        send_response(event, context, "SUCCESS", {})
        return {
            'statusCode': 200,
            'body': json.dumps('Nothing to do')
        }
    logger.info(f"delete_secure_parameter invoked")
    paramName = event.get("ResourceProperties").get("parameterName")
    boto3.client('ssm').delete_parameter(
        Name=paramName
    )
    logger.info(f"Deleted parameter: {paramName}")
    send_response(event, context, "SUCCESS", {})
    return {
        'statusCode': 200,
        'body': json.dumps(f"Deleted parameter: {paramName}")
    }