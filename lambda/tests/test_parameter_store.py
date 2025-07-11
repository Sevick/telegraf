import os


os.environ["TELEGRAMBOTTOKEN_PARAMETER_ARN"] = "arn:aws:ssm:us-east-1:286005182102:parameter/Telegraf/t2/telegramToken"
os.environ["TELEGRAMCHANNEL_PARAMETER_ARN"] = "arn:aws:ssm:us-east-1:286005182102:parameter/Telegraf/t2/telegramChannel"