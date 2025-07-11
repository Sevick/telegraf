from telegraf_sns_consumer import SnsHandler

_sns_handler = SnsHandler()

def lambda_handler(event, context):
    return _sns_handler.sns_handler(event, context)