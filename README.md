# Telegraf

AWS Lambda function that sends SNS messages to Telegram group/channel.

You need to specify just 3 mandatory parameters to install the stack:

- SourceSNSTopic - ARN of the AWS SNS topic whose messages you want to send to Telegram
- TelegramChannel - ID of the telegram group or channel
- TelegramBotToken -  token for the bot (bot should be a member of the defined channel/group and have permissions to post messages)

(SourceSNSTopic=;TelegramChannel=;TelegramBotToken=)
JSON to use with CodeDeploy pipeline : {"SourceSNSTopic": "", "TelegramBotToken": "", "TelegramChannel": ""}

And number of optional parameters that allows you to configure logging, place all lambdas into VPC etc. - check the template's parameters section (or deploy from S3).

### Installation:

- Package
    ```bash
    sam package \
   --template-file template.yaml \
   --s3-bucket my-artifacts-bucket \
   --output-template-file telegraf-packaged.yaml
    ```
- Deploy
    ```bash
    aws cloudformation deploy 
   --template-file telegraf-packaged.yaml 
   --stack-name my-stack-name 
   --capabilities CAPABILITY_IAM
  ```
  


- ## Functions

### TelegrafFunction

The `SnsHandler` function:
- Receives SNS messages
- Extracts message subject and content from each SNS record
- Calls `process_message()` to format Telegram message and send it to configured channel


#### Parameters storage
[AWS caching layer](https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html#arm64) is used to retrieve Telegram bot token and channel ID from AWS Parameter Store (stored as SecureString).

#### Logging and metrics
[AWSLambdaPowertoolsPython](https://docs.powertools.aws.dev/lambda/python/latest/core/logger/) extension is used for embedding mitrics within logs.
Metrics exposed in namespace - {APP_NAME}/{STACK_NAME}:
   - telegram_messages_send_success_counter - successful Telegram API calls
   - telegram_messages_send_failure_counter - failed Telegram API calls


### CreateParameterFunction, DeleteParameterFunction

Functions used during stack installation and removal to manipulate parameters in the Parameter Store (because SecureString is not supported in CF templates)

- ## Configuration
### Environment Variables

- `LOGLEVEL`: Set logging level (default: INFO)

### Subscribe to Additional SNS Topic

1. Add SNS topic ARN to Lambda function trigger configuration
2. Grant SNS permission to invoke the Lambda:
   ```bash
   aws lambda add-permission \
     --function-name <TelegrafFunction> \
     --statement-id sns-invoke \
     --action lambda:InvokeFunction \
     --principal sns.amazonaws.com \
     --source-arn arn:aws:sns:region:account:topic-name
   ```
3. Subscribe Lambda to the topic:
   ```bash
   aws sns subscribe \
     --topic-arn arn:aws:sns:region:account:topic-name \
     --protocol lambda \
     --notification-endpoint arn:aws:lambda:region:account:function:<TelegrafFunction>
   ```
